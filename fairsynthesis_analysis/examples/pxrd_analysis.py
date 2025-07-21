import marimo

__generated_with = "0.14.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from fairsynthesis_data_model.fairsynthesis_data_model import mofsy_api as api
    from fairsynthesis_data_model.fairsynthesis_data_model.generated.mofsy_data_structure import Mofsy
    return api, mo


@app.cell
def _():
    from fairsynthesis_analysis import PXRDAnalysis as _PXRDAnalysis


    class PXRDAnalysis(_PXRDAnalysis):
        """
        PXRDAnalysis is a class for analyzing powder X-ray diffraction (PXRD) data.

        It provides methods to load, process, and visualize PXRD data.
        """

        def blank_measurement_selector(pxrd_file):
            print("Selecting blank measurement for sample:", pxrd_file)

        def pure_measurement_selector(pxrd_file):
            print("Selecting pure measurement for sample:", pxrd_file)
    return (PXRDAnalysis,)


@app.cell
def _(api, mo):
    jxdl = api.load_jxdl(
        mo.notebook_dir() / "../../data/generated/jxdl_from_sciformation.json"
    )
    return (jxdl,)


@app.cell
def _(mo):
    starting_point_for_relative_file_path = mo.notebook_dir() / "../../data"
    return


@app.cell
def _(api, jxdl, mo):
    _synthesis_list = api.get_synthesis_list(jxdl)
    _synthesis_names = [
        synthesis.metadata.description for synthesis in _synthesis_list
    ]
    ui_synthesis_selector = mo.ui.dropdown(_synthesis_names, label="Select Synthesis")
    pxrd_file = api.find_corresponding_pxrd_files(api.get_synthesis_list(jxdl)[0])[0]
    return


@app.cell
def _():
    return


@app.cell
def _(api, jxdl):
    api.get_synthesis_list(jxdl)[0].metadata.description
    return


@app.cell
def _(PXRDAnalysis, jxdl):
    PXRDAnalysis(jxdl)
    return


if __name__ == "__main__":
    app.run()
