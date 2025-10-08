import marimo

__generated_with = "0.14.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from fairsynthesis_data_model import mofsy_api as api
    from fairsynthesis_data_model.generated.procedure_data_structure import Procedure
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
    mofsy = api.load_mofsy(
        mo.notebook_dir() / "../../data/MOCOF-1/generated/procedure_from_sciformation.json"
    )
    return (mofsy,)


@app.cell
def _(mo):
    starting_point_for_relative_file_path = mo.notebook_dir() / "../../data"
    return


@app.cell
def _(api, mo, mofsy):
    _synthesis_list = api.get_synthesis_list(mofsy)
    _synthesis_names = [
        synthesis.metadata.description for synthesis in _synthesis_list
    ]
    ui_synthesis_selector = mo.ui.dropdown(_synthesis_names, label="Select Synthesis")
    pxrd_file = api.find_corresponding_pxrd_files(api.get_synthesis_list(mofsy)[0])[0]
    return


@app.cell
def _():
    return


@app.cell
def _(api, mofsy):
    api.get_synthesis_list(mofsy)[0].metadata.description
    return


@app.cell
def _(PXRDAnalysis, mofsy):
    PXRDAnalysis(mofsy)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
