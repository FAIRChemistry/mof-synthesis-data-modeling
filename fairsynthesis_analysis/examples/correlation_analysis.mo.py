import marimo

__generated_with = "0.17.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import polars as pl
    return (pl,)


@app.cell
def _():
    import fairsynthesis_data_model.mofsy_api as api
    from fairsynthesis_data_model.generated.procedure_data_structure import (
        SynthesisProcedure,
    )
    from fairsynthesis_data_model.generated.characterization_data_structure import (
        ProductCharacterization,
        CharacterizationEntry,
    )
    return (api,)


@app.cell
def _():
    import altair as alt
    return (alt,)


@app.cell
def _(mo):
    procedure_file_path = (
        mo.notebook_dir() / "../../data/MOCOF-1/converted/procedure_from_sciformation.json"
    )
    characterization_file_path = (
        mo.notebook_dir()
        / "../../data/MOCOF-1/converted/characterization_from_sciformation.json"
    )
    return characterization_file_path, procedure_file_path


@app.cell
def _(api, characterization_file_path, procedure_file_path):
    procedure = api.load_procedure(procedure_file_path)
    characterization = api.load_characterization(characterization_file_path)
    return characterization, procedure


@app.cell(hide_code=True)
def _(pl):
    def flatten_nested(obj, prefix="", sep="_"):
        """Recursively flatten nested dicts/lists into a flat dict."""
        result = {}

        if isinstance(obj, dict):
            for k, v in obj.items():
                new_key = f"{prefix}{sep}{k}" if prefix else k
                result.update(flatten_nested(v, new_key, sep))
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                new_key = f"{prefix}{sep}{i}" if prefix else str(i)
                result.update(flatten_nested(v, new_key, sep))
        else:
            # Skalar: direkt zuweisen (prefix muss hier gesetzt sein)
            key = prefix if prefix else "value"
            result[key] = obj

        return result


    def dict_to_dataframe(data, sep="_"):
        """Convert nested dict to a Polars DataFrame.
        Zeilen = Länge der längsten Liste; Dicts/Skalare gelten in jeder Zeile.
        """
        # Nur Listen zählen für die Zeilenanzahl
        list_lengths = [len(v) for v in data.values() if isinstance(v, list)]
        max_rows = max(list_lengths) if list_lengths else 1

        rows = []
        for i in range(max_rows):
            row = {}
            for key, value in data.items():
                if isinstance(value, list):
                    item = value[i] if i < len(value) else None
                else:
                    # Dicts & Skalare nicht zeilenbildend: in jeder Zeile gleich
                    item = value

                if item is None:
                    # explizit Null setzen, damit Spalten konsistent sind
                    row[key] = None
                else:
                    row.update(flatten_nested(item, key, sep))

            rows.append(row)

        return pl.DataFrame(rows)
    return (dict_to_dataframe,)


@app.cell
def _(mo, pl):
    molar_fraction = pl.read_csv(
        mo.notebook_dir() / "data/pxrd_molar_fraction_overview.csv"
    )
    return (molar_fraction,)


@app.cell
def _(api, dict_to_dataframe, molar_fraction, pl, procedure):
    _df = []
    for _id in molar_fraction["id"]:
        _df.append(
            dict_to_dataframe(
                api.get_synthesis_by_experiment_id(procedure, _id).to_dict()
            ).with_columns(id=pl.lit(_id))
        )
    _df = pl.concat(_df, how="diagonal")
    _cols = _df.columns
    _cols.sort()
    _df = _df.select(_cols)
    df_procedure = molar_fraction.join(_df, on="id", how="left")
    return (df_procedure,)


@app.cell
def _(api, characterization, dict_to_dataframe, molar_fraction, pl):

    _df = []
    for _id in molar_fraction["id"]:
        _df.append(
            dict_to_dataframe(
                api.get_characterization_by_experiment_id(characterization, _id).to_dict()
            ).with_columns(id=pl.lit(_id))
        )
    df_characterization = pl.concat(_df, how="diagonal")
    return (df_characterization,)


@app.cell
def _():
    from molmass import Formula

    sum_formula = {
        "COF-366-Co": "C60H36CoN8",
        "MOCOF-1": "C52H33CoN8",
        "unknown": "C44H31CoN8",
    }
    formula_mass = {k: Formula(v).mass for k, v in sum_formula.items()}
    return (formula_mass,)


@app.cell
def _(df_characterization, df_procedure):
    df_all = df_procedure.join(df_characterization, on="id", how="left")
    return (df_all,)


@app.cell
def _(df_all, mo):
    df_all_refined = mo.ui.dataframe(df_all)
    df_all_refined
    return


@app.cell
def _(json, mo):
    with open(
        mo.notebook_dir() / "../../data/MOCOF-1/converted/params_from_sciformation.json"
    ) as f:
        params = json.load(f)
    return (params,)


@app.cell
def _():
    import json
    return (json,)


@app.cell
def _(molar_fraction, params, pl):
    nameset = set()
    for n, v in params.items():
        for k in v.keys():
            nameset.add(k)
    _dict = {n: [] for n in nameset}
    _dict["id"] = []
    for n, v in params.items():
        _dict["id"].append(n)
        for name in nameset:
            _dict[name].append(v.get(name, None))
    df_2 = molar_fraction.join(pl.DataFrame(_dict), on="id", how="inner")
    df_2
    return (df_2,)


@app.cell
def _(df_2, df_characterization, df_procedure, formula_mass, pl):
    df3 = (
        df_2.select(
            pl.col("*")
        )
        .join(
            df_characterization.select(
                "id",
                (pl.col("Characterization_weight_0__weight_Value") * 1e-3).alias(
                    "product_weight_g"
                ),
            ),
            on="id",
        )
        .join(
            df_procedure.select(
                "id",
                (pl.col("Procedure_Prep_Step_0__amount_Value") * 1e-6).alias(
                    "precursor_amount_mol"
                ),
            ),
            on="id",
        )
        .with_columns(
            (
                pl.col("COF-366-Co")
                * pl.col("product_weight_g")
                / (
                    pl.col("COF-366-Co") * formula_mass["COF-366-Co"]
                    + pl.col("MOCOF-1") * formula_mass["MOCOF-1"]
                    + pl.col("unknown") * formula_mass["unknown"]
                )
                / pl.col("precursor_amount_mol")
            ).clip(upper_bound=1).alias("yield_COF-366-Co"),
            (
                pl.col("MOCOF-1")
                * pl.col("product_weight_g")
                / (
                    pl.col("COF-366-Co") * formula_mass["COF-366-Co"]
                    + pl.col("MOCOF-1") * formula_mass["MOCOF-1"]
                    + pl.col("unknown") * formula_mass["unknown"]
                )
                / pl.col("precursor_amount_mol")
            ).clip(upper_bound=1).alias("yield_MOCOF-1"),
        )
        .with_columns(
            pl.col("COF-366-Co").alias("mol_fraction_COF-366-Co"),
            pl.col("MOCOF-1").alias("mol_fraction_MOCOF-1"),
            pl.col("unknown").alias("mol_fraction_unknown"),
        )
        .select(
            pl.col("*").exclude(
                [
                    "product_weight_g",
                    "precursor_amount_mol",
                    "COF-366-Co",
                    "MOCOF-1",
                    "unknown",
                ]
            )
        )
    )
    df3
    return (df3,)


@app.cell
def _(df3, mo, pl):
    df_selected = mo.ui.table(
        df3.with_columns(
            ald_per_amino=(
                pl.col("aldehyde_monomer_amount_umol")
                / pl.col("aminoporphyrin_monomer_amount_umol")
            ),
            water_per_amino=(
                pl.col("water_amount_umol") / pl.col("aminoporphyrin_monomer_amount_umol")
            ).clip(lower_bound=10),
            water_per_aldeyde=(
                pl.col("water_amount_umol") / pl.col("aldehyde_monomer_amount_umol")
            ),
        ),
        initial_selection=range(len(df3)),
    )
    df_selected
    return (df_selected,)


@app.cell
def _():
    import plotly.express as px
    return (px,)


@app.cell
def _(df_selected, px):
    _df = df_selected.value
    _fig = px.scatter_3d(_df, x="ald_per_amino", y="water_per_amino", z="yield_MOCOF-1", log_x=True, log_y=True)
    _fig.update_layout(scene_aspectmode="cube")
    _fig.show()
    return


@app.cell
def _(alt, df_selected, pl):
    # replace _df with your data source
    _df = df_selected.value.with_columns(
        ald_per_amino=(
            pl.col("aldehyde_monomer_amount_umol")
            / pl.col("aminoporphyrin_monomer_amount_umol")
        ),
        water_per_amino=(
            pl.col("water_amount_umol") / pl.col("aminoporphyrin_monomer_amount_umol")
        ),
        water_per_aldeyde=(
            pl.col("water_amount_umol") / pl.col("aldehyde_monomer_amount_umol")
        ),
    )

    _chart = (
        alt.Chart(_df)
        .mark_point()
        .encode(
            x=alt.X(field="ald_per_amino", type="quantitative"),
            y=alt.Y(field="water_per_amino", type="quantitative"),
            color=alt.Color(field="yield_MOCOF-1", type="quantitative"),
            tooltip=[
                alt.Tooltip(field="ald_per_amino", format=",.2f"),
                alt.Tooltip(field="water_per_amino", format=",.2f"),
                alt.Tooltip(field="yield_MOCOF-1", format=",.2f"),
            ],
        )
        .properties(height=290, width="container", config={"axis": {"grid": True}})
    )
    _chart
    return


@app.cell
def _(alt, df3, pl):
    # replace _df with your data source
    _df = df3.with_columns(
        ald_per_amino=(
            pl.col("aldehyde_monomer_amount_umol")
            / pl.col("aminoporphyrin_monomer_amount_umol")
        ),
        water_per_amino=(
            pl.col("water_amount_umol") / pl.col("aminoporphyrin_monomer_amount_umol")
        ),
        water_per_aldeyde=(
            pl.col("water_amount_umol") / pl.col("aldehyde_monomer_amount_umol")
        ),
    )

    _chart = (
        alt.Chart(_df)
        .mark_point()
        .encode(
            x=alt.X(field="water_per_aldeyde", type="quantitative"),
            y=alt.Y(field="mol_fraction_MOCOF-1", type="quantitative"),
            # color=alt.Color(field="yield_MOCOF-1", type="quantitative"),
            tooltip=[
                alt.Tooltip(field="water_per_aldeyde", format=",.2f"),
                alt.Tooltip(field="mol_fraction_MOCOF-1", format=",.2f"),
                alt.Tooltip(field="yield_MOCOF-1", format=",.2f"),
            ],
        )
        .properties(height=290, width="container", config={"axis": {"grid": True}})
    )
    _chart
    return


@app.cell
def _(alt, df_selected):
    _chart = (
        alt.Chart(df_selected.value)
        .mark_point()
        .encode(
            x=alt.X(field="water_per_aldeyde", type="quantitative"),
            y=alt.Y(field="yield_MOCOF-1", type="quantitative"),
            # color=alt.Color(field="yield_MOCOF-1", type="quantitative"),
            tooltip=[
                alt.Tooltip(field="water_per_aldeyde", format=",.2f"),
                alt.Tooltip(field="mol_fraction_MOCOF-1", format=",.2f"),
                alt.Tooltip(field="yield_MOCOF-1", format=",.2f"),
            ],
        )
        .properties(height=290, width="container", config={"axis": {"grid": True}})
    )
    _chart
    return


@app.cell
def _(df3):
    df3["acid_structure"].unique().to_list()
    return


@app.cell
def _(alt, df_selected, pl):
    # replace _df with your data source
    _df = df_selected.value.with_columns(
        order=pl.col("acid_structure").replace_strict(
            {
                "C6H4ClNO3": 0,
                "C2H4O2": 0,
                "C2HF3O2": 0,
                "C5H10O2": 0,
                "C6H5NO3": 0,
                "unknown": 0,
                "C6H4N2O5": 0,
                "C7H5NO": 0,
                "C7H4N2O6": 0,
                "C7H6O2": 0,
                "C6H5BrO": 0,
                "C6HF5O": 0,
            }
        )
    ).sort("order", "id")

    _chart = (
        alt.Chart(_df)
        .mark_point()
        .encode(
            x=alt.X(field="acid_structure", type="nominal"),
            y=alt.Y(field="yield_MOCOF-1", type="quantitative"),
            # color=alt.Color(field="yield_MOCOF-1", type="quantitative"),
            # opacity=alt.Opacity(field="yield_MOCOF-1", type="quantitative").scale(
            #    domain=[0.5, 0.8]
            # ),
            tooltip=[
                alt.Tooltip(field="acid_structure"),
                alt.Tooltip(field="water_per_aldeyde", format=",.2f"),
                alt.Tooltip(field="MOCOF-1", format=",.2f"),
            ],
        )
        .properties(height=290, width="container", config={"axis": {"grid": True}})
        .interactive()
    )
    _chart
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
