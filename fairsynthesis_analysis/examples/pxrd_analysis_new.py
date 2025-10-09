import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    from pathlib import Path
    return


@app.cell
def _():
    import fairsynthesis_data_model.mofsy_api as api
    from fairsynthesis_data_model.generated.procedure_data_structure import Procedure
    from fairsynthesis_data_model.generated.characterization_data_structure import (
        ProductCharacterization,
        CharacterizationEntry,
    )
    from fairsynthesis_data_model.pxrd_collector import PXRDFile
    return PXRDFile, Procedure, ProductCharacterization, api


@app.cell
def _():
    from fairsynthesis_analysis import PXRDSpectrum
    return (PXRDSpectrum,)


@app.cell
def _(mo):
    procedure_file_path = (
        mo.notebook_dir() / "../../data/MOCOF-1/generated/procedure_from_sciformation.json"
    )
    characterization_file_path = (
        mo.notebook_dir()
        / "../../data/MOCOF-1/generated/characterization_from_sciformation.json"
    )
    return characterization_file_path, procedure_file_path


@app.cell
def _(
    Procedure,
    ProductCharacterization,
    api,
    characterization_file_path,
    procedure_file_path,
):
    procedure: Procedure = api.load_mofsy(procedure_file_path)
    characterization: ProductCharacterization = api.load_characterization(
        characterization_file_path
    )
    return characterization, procedure


@app.cell
def _(PXRDFile, PXRDSpectrum):
    def load_pxrd_data(pxrd_file: PXRDFile) -> PXRDSpectrum | None:
        """Load PXRD data from a CharacterizationEntry if available.

        Args:
            characterization (CharacterizationEntry): The characterization entry to check.

        Returns:
            PXRDSpectrum | None: The loaded PXRD spectrum or None if not available.
        """
    return


@app.cell
def _(api, mo, procedure: "Procedure"):
    _list = []
    for _it in api.get_synthesis_list(procedure):
        try:
            _list.append(
                (
                    _it.metadata.description
                    # [
                    #    _i.xray_source
                    #    for _i in api.find_corresponding_pxrd_files(
                    #        api.get_characterization_by_experiment_id(
                    #            characterization, _it.metadata.description
                    #        ),
                    #    )
                    # ][0],
                )
            )
        except:
            continue
    selector = mo.ui.dropdown(_list)
    selector
    return (selector,)


@app.cell
def _():
    return


@app.cell
def _(
    PXRDSpectrum,
    api,
    characterization: "ProductCharacterization",
    selector,
):
    _c = api.get_characterization_by_experiment_id(characterization, selector.value)
    it = [PXRDSpectrum(it) for it in api.find_corresponding_pxrd_files(_c)]
    return (it,)


@app.cell
def _(it):
    it[0]
    return


@app.cell
def _(it):
    it[0].normalize()
    return


@app.cell
def _(it):
    it[0].subtract_background().normalize().correct_baseline()
    return


@app.cell
def _(
    PXRDSpectrum,
    api,
    characterization: "ProductCharacterization",
    cof366,
    mocof1,
    selector,
):
    di = {}
    for _s in selector.options:
        try:
            di[_s] = [
                PXRDSpectrum(it)
                .subtract_background()
                .normalize()
                .correct_baseline()
                .calc_yield({"COF-366": cof366, "MOCOF-1": mocof1})
                for it in api.find_corresponding_pxrd_files(
                    api.get_characterization_by_experiment_id(characterization, _s)
                )
            ][0]
        except:
            di[_s] = None
    return (di,)


@app.cell
def _():
    import polars as pl
    return (pl,)


@app.cell
def _(di, pl):
    pl.DataFrame(
        {
            "id": di.keys(),
            "yield": di.values(),
        }
    ).select(
        [
            pl.col("id"),
            pl.col("yield").struct.field("COF-366").alias("COF-366"),
            pl.col("yield").struct.field("MOCOF-1").alias("MOCOF-1"),
            pl.col("yield").struct.field("unknown").alias("unknown"),
        ]
    ).sort("id")
    return


@app.cell
def _(PXRDSpectrum, api, characterization: "ProductCharacterization"):
    cof366 = ["KE-132", "KE-207", "KE-286", "KE-328"]
    mocof1 = ["KE-228", "KE-254", "KE-301", "KE-326"]
    cof366 = [
        PXRDSpectrum(
            api.find_corresponding_pxrd_files(
                api.get_characterization_by_experiment_id(characterization, _s)
            )[0]
        )
        for _s in cof366
    ]
    mocof1 = [
        PXRDSpectrum(
            api.find_corresponding_pxrd_files(
                api.get_characterization_by_experiment_id(characterization, _s)
            )[0]
        )
        for _s in mocof1
    ]
    return cof366, mocof1


@app.cell
def _(cof366, di, mocof1):
    di["KE-036"][0].calc_yield({"COF-366": cof366, "MOCOF-1": mocof1})
    return


if __name__ == "__main__":
    app.run()
