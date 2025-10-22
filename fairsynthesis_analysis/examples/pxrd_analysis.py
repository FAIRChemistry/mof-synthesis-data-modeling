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
    import json
    return (json,)


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
def _(mo):
    mo.md(r"""# Overview PXRD Analysis""")
    return


@app.cell
def _(mo):
    reload_button = mo.ui.run_button(label="Reload PXRD Data")
    reload_button
    return (reload_button,)


@app.cell
def _(di, mo, pl):
    _data = (
        pl.DataFrame(
            {
                "id": di.keys(),
                "yield": di.values(),
            }
        )
        .select(
            [
                pl.col("id"),
                pl.col("yield").struct.field("COF-366").alias("COF-366"),
                pl.col("yield").struct.field("MOCOF-1").alias("MOCOF-1"),
                pl.col("yield").struct.field("unknown").alias("unknown"),
            ]
        )
        .sort("id")
    )
    _data.write_csv(mo.notebook_dir() / "data/pxrd_yield_overview.csv")
    overview_selection = mo.ui.table(_data, selection="single")
    overview_selection
    return (overview_selection,)


@app.cell
def _(api, procedure: "Procedure"):
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
    all_synthesis = _list
    return (all_synthesis,)


@app.cell
def _(mo, overview_selection):
    mo.stop(len(overview_selection.value) < 1)
    selection = overview_selection.value["id"].first()
    mo.md(f"# Insight into {selection}")
    return (selection,)


@app.cell
def _(
    PXRDSpectrum,
    api,
    characterization: "ProductCharacterization",
    selection,
):
    _c = api.get_characterization_by_experiment_id(characterization, selection)
    it = [PXRDSpectrum(it) for it in api.find_corresponding_pxrd_files(_c)]
    return (it,)


@app.cell
def _(mo, settings):
    ui_settings_override = mo.md("""
    #### normalization
    - cu_range: ({cu1}, {cu2})
    - co_range: ({co1}, {co2})
    #### correct_baseline
    - max_half_window: {max_half_window}
    - smooth_half_window: {smooth_half_window}
    """).batch(
        cu1=mo.ui.number(value=settings["normalization"]["cu_range"][0], step=0.01),
        cu2=mo.ui.number(value=settings["normalization"]["cu_range"][1], step=0.01),
        co1=mo.ui.number(value=settings["normalization"]["co_range"][0], step=0.01),
        co2=mo.ui.number(value=settings["normalization"]["co_range"][1], step=0.01),
        max_half_window=mo.ui.number(value=settings["correct_baseline"]["max_half_window"]),
        smooth_half_window=mo.ui.number(
            value=settings["correct_baseline"]["smooth_half_window"]
        ),
    )
    ui_settings_override
    return (ui_settings_override,)


@app.cell
def _(mo):
    save_button = mo.ui.run_button(label="Save Settings")
    save_button
    return (save_button,)


@app.cell
def _(ui_settings_override):
    settings_override = {
        "normalization": {
            "cu_range": [
                ui_settings_override.value["cu1"],
                ui_settings_override.value["cu2"],
            ],
            "co_range": [
                ui_settings_override.value["co1"],
                ui_settings_override.value["co2"],
            ],
        },
        "correct_baseline": {
            "max_half_window": ui_settings_override.value["max_half_window"],
            "smooth_half_window": ui_settings_override.value["smooth_half_window"],
        },
    }
    return (settings_override,)


@app.cell
def _(id_settings, json, mo, save_button, selection, settings_override):
    _it = None
    if save_button.value:
        id_settings[selection] = settings_override
        with open(mo.notebook_dir() / "data/settings.json", "w") as _f:
            json.dump(id_settings, _f, indent=4)
        _it = mo.md("Settings saved!")
    _it
    return


@app.cell
def _(it, mo, settings_override):
    mo.md(
        f"""
    {
            mo.accordion(
                {
                    "Measurement": it[0]._display_(),
                    "Background subtracted": it[0].subtract_background()._display_(),
                    "Normalized": (
                        it[0]
                        .subtract_background()
                        .normalize(settings_override["normalization"])
                        ._display_()
                    ),
                    "Baseline Corrected": (
                        it[0]
                        .subtract_background()
                        .normalize(settings_override["normalization"])
                        .correct_baseline(settings_override["correct_baseline"])
                        ._display_()
                    ),
                }
            )
        }
    """
    )
    return


@app.cell
def _(cof366, it, mocof1, settings_override):
    (
        it[0]
        .subtract_background()
        .normalize(settings_override["normalization"])
        .correct_baseline(settings_override["correct_baseline"])
        .calc_yield({"COF-366": cof366, "MOCOF-1": mocof1})
    )
    return


@app.cell
def _():
    import polars as pl
    return (pl,)


@app.cell
def _(
    PXRDSpectrum,
    api,
    characterization: "ProductCharacterization",
    default_settings,
    id_settings,
):
    def get_pxrd_spectrum(
        experiment_id: str,
    ) -> PXRDSpectrum | None:
        """Retrieve the PXRD spectrum from a CharacterizationEntry.

        Args:
            characterization_entry (CharacterizationEntry): The characterization entry to check.

        Returns:
            PXRDSpectrum | None: The PXRD spectrum if available, otherwise None.
        """
        if experiment_id in id_settings:
            settings = id_settings[experiment_id]
        else:
            settings = default_settings
        characterization_entry = api.get_characterization_by_experiment_id(
            characterization, experiment_id
        )
        pxrd_files = api.find_corresponding_pxrd_files(characterization_entry)
        # if pxrd_files:
        return (
            PXRDSpectrum(pxrd_files[0])
            .subtract_background()
            .normalize(settings["normalization"])
            .correct_baseline(settings["correct_baseline"])
        )
        return None
    return (get_pxrd_spectrum,)


@app.cell
def _(get_pxrd_spectrum):
    cof366 = ["KE-132", "KE-207", "KE-286", "KE-328"]
    mocof1 = ["KE-228", "KE-254", "KE-301", "KE-326"]
    cof366 = [get_pxrd_spectrum(_s) for _s in cof366]
    mocof1 = [get_pxrd_spectrum(_s) for _s in mocof1]
    return cof366, mocof1


@app.cell
def _(json, mo):
    with open(mo.notebook_dir() / "data/default_settings.json") as _f:
        default_settings = json.load(_f)
    return (default_settings,)


@app.cell
def _(json, mo):
    with open(mo.notebook_dir() / "data/settings.json") as _f:
        id_settings = json.load(_f)
    return (id_settings,)


@app.cell
def _(default_settings, id_settings, selection):
    settings = id_settings[selection] if selection in id_settings else default_settings
    return (settings,)


@app.cell
def _(
    all_synthesis,
    cof366,
    get_pxrd_spectrum,
    json,
    mo,
    mocof1,
    reload_button,
):
    di = {}
    _ = reload_button.value
    with open(mo.notebook_dir() / "data/settings.json") as _f:
        _settings = json.load(_f)
    for _s in all_synthesis:
        try:
            di[_s] = (get_pxrd_spectrum(_s)).calc_yield({"COF-366": cof366, "MOCOF-1": mocof1})
        except:
            di[_s] = None
    return (di,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
