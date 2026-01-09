from dataclasses import dataclass
from pathlib import Path
import os
import numpy as np
import pybaselines as pb
from fair_synthesis.formatting.pxrd_collector import PXRDFile
from scipy.optimize import nnls as _nnls


def _extract_corresponding_reference(pxrd_file: PXRDFile, references: list[PXRDFile]) -> PXRDFile | None:
    """Extracts the corresponding reference PXRD file from a list of references.

    Args:
        pxrd_file (PXRDFile): The PXRD file for which to find the corresponding reference.
        references (list[PXRDFile]): A list of reference PXRD files.

    Returns:
        PXRDFile | None: The corresponding reference PXRD file, or None if not found.
    """
    _filtered = [f for f in references if f.xray_source == pxrd_file.xray_source]
    if len(_filtered) > 0:
        references = _filtered
    _filtered = [f for f in references if f.sample_holder_shape == pxrd_file.sample_holder_shape]
    if len(_filtered) > 0:
        references = _filtered
    #_filtered = [f for f in references if f.sample_holder_diameter == pxrd_file.sample_holder_diameter]
    #if len(_filtered) > 0:
    #    references = _filtered
    #_filtered = [f for f in references if f.other_metadata == pxrd_file.other_metadata]
    #if len(_filtered) > 0:
    #    references = _filtered
    if len(references) == 0:
        return None
    return references[0]


@dataclass
class PXRDPattern(PXRDFile):
    """Class representing a PXRD spectrum."""

    def __init__(
        self,
        pxrd_file: PXRDFile,
        two_theta: np.ndarray | None = None,
        intensity: np.ndarray | None = None,
    ):
        self.experiment_id = pxrd_file.experiment_id
        self.xray_source = pxrd_file.xray_source
        self.sample_holder_shape = pxrd_file.sample_holder_shape
        self.sample_holder_diameter = pxrd_file.sample_holder_diameter
        self.other_metadata = pxrd_file.other_metadata
        self.path = pxrd_file.path

        repo_root = Path(__file__).parent.parent.parent.parent

        # --- Load data if not passed manually ---
        if two_theta is None or intensity is None:
            pxrd_path = os.path.join(repo_root, self.path)
            pxrd_data = np.loadtxt(pxrd_path)

            #def _convert_Co_to_Cu(two_theta: np.ndarray) -> np.ndarray:
            #    """Convert 2θ from Co-Kα1 to Cu-Kα1."""
            #    λ_Cu = 1.540562  # Å
            #    λ_Co = 1.788965  # Å
            #    return np.degrees(2 * np.arcsin(λ_Cu / λ_Co * np.sin(np.radians(two_theta) / 2)))

            #if pxrd_file.xray_source == "Co-Kα1":
            #    two_theta = _convert_Co_to_Cu(pxrd_data[:, 0])
            #elif pxrd_file.xray_source == "Cu-Kα1":
            #    two_theta = pxrd_data[:, 0]
            #else:
            #    raise ValueError(f"Unsupported X-ray source: {pxrd_file.xray_source}")
            two_theta = pxrd_data[:, 0]
            intensity = pxrd_data[:, 1]
        else:
            two_theta = two_theta.copy()
            intensity = intensity.copy()

        self.two_theta = np.asarray(two_theta)
        self.intensity = np.asarray(intensity)

    def subtract_background(self, background=None, normalize=False) -> "PXRDPattern":
        """Subtracts a background from the intensity values.

        Args:
            background (PXRDPattern): The background spectrum to subtract.

        Returns:
            PXRDPattern: A new PXRDPattern instance with the background subtracted.
        """
        if background is None:

            def select_background_spectrum(pxrd_file: PXRDFile, background_files: list[str] | None = None) -> PXRDFile:
                if not background_files:
                    _dir = Path(pxrd_file.path).parent
                    _background_files = list(_dir.glob("*PXRD_Blank_*.xyd"))
                    _background_files = [PXRDFile(str(f)) for f in _background_files]
                else:
                    _background_files = [PXRDFile(f) for f in background_files]

                _background_file = _extract_corresponding_reference(pxrd_file, _background_files)
                if _background_file is None:
                    raise ValueError(f"No suitable background file found for PXRD file: {pxrd_file.path}")
                return _background_file

            background_file = select_background_spectrum(self)
            background = PXRDPattern(background_file)

        if normalize:
            background = background.normalize()

        intensity = self.intensity[self.two_theta >= background.two_theta.min()]
        two_theta = self.two_theta[self.two_theta <= background.two_theta.max()]

        intensity = intensity[self.two_theta <= background.two_theta.max()]
        two_theta = two_theta[self.two_theta >= background.two_theta.min()]

        return PXRDPattern(
            self,
            two_theta,
            intensity - np.interp(two_theta, background.two_theta, background.intensity),
        )

    def normalize(self, settings=None) -> "PXRDPattern":
        """Normalizes the intensity values to a range of 0 to 1.

        Returns:
            PXRDPattern: A new PXRDPattern instance with normalized intensity values.
        """
        if settings is None:
            settings = {}
        if type(settings) is not dict:
            raise ValueError("Settings must be a dictionary.")

        if self.xray_source == "Co-Kα1":
            reference_range = settings.get("co_range", (1.5, 1.8))
        elif self.xray_source == "Cu-Kα1":
            reference_range = settings.get("cu_range", (38, 40))
        else:
            raise ValueError(f"Unsupported X-ray source: {self.xray_source}")

        mean_in_range = np.mean(
            self.intensity[(self.two_theta >= reference_range[0]) & (self.two_theta <= reference_range[1])]
        )

        return PXRDPattern(self, self.two_theta, self.intensity / mean_in_range)

    def correct_baseline(self, settings=None) -> "PXRDPattern":
        """Corrects the baseline of the intensity values.

        Returns:
            PXRDPattern: A new PXRDPattern instance with baseline-corrected intensity values.
        """
        if settings is None:
            settings = {}
        if type(settings) is not dict:
            raise ValueError("Settings must be a dictionary.")

        def _baseline_correction(x, y):
            _bool = np.isnan(y)
            y = y[~np.isnan(y)].copy()
            baseline_fitter = pb.Baseline(x_data=x[~_bool])
            base, _ = baseline_fitter.snip(
                y,
                max_half_window=settings.get("max_half_window", 40),
                decreasing=True,
                smooth_half_window=settings.get("smooth_half_window", 3),
            )
            y_detrend = np.ones_like(x) * np.nan
            y_detrend[~_bool] = y - base
            return y_detrend

        return PXRDPattern(self, self.two_theta, _baseline_correction(self.two_theta, self.intensity))

    def calc_molar_fraction(
        self, products: dict[str, "PXRDPattern"] | dict[str, list["PXRDPattern"]]
    ) -> dict[str, float]:
        """Calculates the molar fraction of each product based on the intensity values.

        Args:
            products (dict[str, PXRDPattern | list[PXRDPattern]]):
                A dictionary of product names and their corresponding PXRD files.
        Returns:
            dict[str, float]: A dictionary of product names and their corresponding molar fractions (2 digits after decimal).
        """

        def _linear_combination_shortening(x, y, components):
            phase_keys = list(components)
            if not phase_keys:
                return {"amorphous": 1.0}

            phase_arrays = [np.asarray(components[name], dtype=float) for name in phase_keys]
            target = np.asarray(y, dtype=float)

            min_len = min(target.size, *[arr.size for arr in phase_arrays])
            target = target[:min_len]
            phase_arrays = [arr[:min_len] for arr in phase_arrays]

            design_matrix = np.column_stack(phase_arrays)
            weights, _ = _nnls(design_matrix, target)
            # weights = np.minimum(weights, 1.0)

            labels = []
            for name in phase_keys:
                if "MOCOF-1" in name:
                    labels.append("MOCOF-1")
                elif "COF-366-Co" in name:
                    labels.append("COF-366-Co")
                else:
                    labels.append(name)

            contributions = {label: value for label, value in zip(labels, weights)}
            contributions["amorphous"] = max(0.0, 1.0 - weights.sum())
            if sum(contributions.values()) > 0:
                total = 1 #sum(contributions.values())
                contributions = {k: v / total for k, v in contributions.items()}
            return contributions

        _products = {
            k: _extract_corresponding_reference(self, v) if isinstance(v, list) else v  # type: ignore
            for k, v in products.items()
        }
        for k, v in _products.items():
            if v is None:
                raise ValueError(f"No suitable product file found for PXRD file: {self.path}")

        intensities = _linear_combination_shortening(
            self.two_theta,
            self.intensity,
            {
                k: np.interp(self.two_theta, v.two_theta, v.intensity)  # type: ignore
                for k, v in _products.items()
            },
        )
        return {k: round(v, 2) for k, v in intensities.items()}

    def _display_(self):
        import altair as alt
        import marimo as mo
        import polars as pl

        chart = (
            alt.Chart(
                pl.DataFrame(
                    {
                        "two_theta": self.two_theta,
                        "intensity": self.intensity,
                    }
                )
            )
            .mark_line()
            .encode(
                x=alt.X("two_theta", title="2θ (degrees)"),
                y=alt.Y("intensity", title="Intensity (a.u.)"),
            )
            .properties(
                title=f"PXRD Spectrum: {self.path}",
                width=600,
                height=400,
            )
        )
        metadata = self.__dict__.copy()
        metadata.pop("two_theta")
        metadata.pop("intensity")
        return mo.hstack([chart, metadata])