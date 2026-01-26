import marimo

__generated_with = "0.19.0"
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
    import fair_synthesis.formatting.mofsy_api as api
    from fair_synthesis.generated_apis.procedure_data_structure import (
        SynthesisProcedure,
    )
    from fair_synthesis.generated_apis.characterization_data_structure import (
        Characterization,
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
        mo.notebook_dir() /
        "../../data/MOCOF-1/converted/procedure_from_sciformation.json")
    characterization_file_path = (
        mo.notebook_dir() /
        "../../data/MOCOF-1/converted/characterization_from_sciformation.json")
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
                    # Dicts & Skalare nicht zeilenbildend: in jeder Zeile
                    # gleich
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
        mo.notebook_dir() / "data/phase_molar-fractions.csv"
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
                api.get_characterization_by_experiment_id(
                    characterization, _id).to_dict()
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
        "amorphous": "C44H31CoN8",
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
def _(df_characterization):
    df_characterization
    return


@app.cell
def _(df_2, df_characterization, df_procedure, formula_mass, pl):
    df3 = (
        df_2.select(
            pl.col("*")
        )
        .join(
            df_characterization.select(
                "id",
                (pl.col("Characterization_Weight_0_Weight_Value") * 1e-3).alias(
                    "product_mass_g"
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
                * pl.col("product_mass_g")
                / (
                    pl.col("COF-366-Co") * formula_mass["COF-366-Co"]
                    + pl.col("MOCOF-1") * formula_mass["MOCOF-1"]
                    + pl.col("amorphous") * formula_mass["amorphous"]
                )
                / pl.col("precursor_amount_mol")
            ).round(2).clip(upper_bound=1).alias("yield_COF-366-Co"),
            (
                pl.col("MOCOF-1")
                * pl.col("product_mass_g")
                / (
                    pl.col("COF-366-Co") * formula_mass["COF-366-Co"]
                    + pl.col("MOCOF-1") * formula_mass["MOCOF-1"]
                    + pl.col("amorphous") * formula_mass["amorphous"]
                )
                / pl.col("precursor_amount_mol")
            ).round(2).clip(upper_bound=1).alias("yield_MOCOF-1"),
        )
        .with_columns(
            pl.col("COF-366-Co").alias("mol_fraction_COF-366-Co"),
            pl.col("MOCOF-1").alias("mol_fraction_MOCOF-1"),
            pl.col("amorphous").alias("mol_fraction_amorphous"),
        )
        .select(
            pl.col("*").exclude(
                [
                    "product_mass_g",
                    "precursor_amount_mol",
                    "COF-366-Co",
                    "MOCOF-1",
                    "amorphous",
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
            ald_per_amine=(
                pl.col("aldehyde_monomer_amount_umol")
                / pl.col("aminoporphyrin_monomer_amount_umol")
            ).round(2),
            water_per_amine=(
                pl.col("water_amount_umol") /
                pl.col("aminoporphyrin_monomer_amount_umol")
            ).round(1).clip(lower_bound=10),
            water_per_aldeyde=(
                pl.col("water_amount_umol") /
                pl.col("aldehyde_monomer_amount_umol")
            ).round(1).clip(lower_bound=10),
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
    _fig = px.scatter_3d(
        _df,
        x="ald_per_amine",
        y="water_per_amine",
        z="yield_MOCOF-1",
        log_x=True,
        log_y=True,
        hover_data=[
            'id',
            'ald_per_amine',
            'water_per_amine',
            'yield_MOCOF-1'])
    _fig.update_traces(marker=dict(size=4))
    _fig.update_layout(scene_aspectmode="cube")
    _fig.show()
    return


@app.cell
def _(df_selected, px):
    _df = df_selected.value
    _fig = px.scatter_3d(
        _df,
        x="ald_per_amine",
        y="water_per_amine",
        z="yield_MOCOF-1",
        log_x=True,
        log_y=True,
        hover_data=['id', 'ald_per_amine', 'water_per_amine', 'yield_MOCOF-1']
    )

    _fig.update_traces(marker=dict(size=4))
    fontsize = 28
    _fig.update_layout(
        scene_aspectmode="cube",
        scene=dict(
            xaxis=dict(
                title=dict(text="Aldehyde equiv", font=dict(size=fontsize)),
                tickfont=dict(size=fontsize*0.6),
                type="log",
                nticks=3,
            ),
            yaxis=dict(
                title=dict(text="Water equiv", font=dict(size=fontsize)),
                tickfont=dict(size=fontsize*0.55),
                type="log",
                exponentformat="power",
                nticks=3,
                autorange=False,     # disable automatic range
                range=[0.9, 3]
            ),
            zaxis=dict(
                title=dict(text="MOCOF-1 yield", font=dict(size=fontsize)),
                tickfont=dict(size=fontsize*0.6),
                nticks=4
            )
        ),
        width=900,
        height=700,
    )

    from scipy.spatial import ConvexHull
    import numpy as np

    _points = _df.drop_nulls(["ald_per_amine",
                              "water_per_amine",
                              "yield_MOCOF-1"])[["ald_per_amine",
                                                 "water_per_amine",
                                                 "yield_MOCOF-1"]]
    _hull = ConvexHull(_points).simplices

    import plotly.graph_objects as go

    _mesh = go.Mesh3d(
        x=_points[:, 0], y=_points[:, 1], z=_points[:, 2],
        i=_hull[:, 0], j=_hull[:, 1], k=_hull[:, 2],
        opacity=0.5,
        color='lightblue',
        flatshading=True,
        lighting=dict(ambient=0.4, diffuse=0.7, specular=0.2,
                      roughness=0.7, fresnel=0.05),
        lightposition=dict(x=2, y=90, z=2),
        hoverinfo='skip'
    )

    _fig.add_trace(_mesh)

    _fig.show()
    return ConvexHull, np


@app.cell(hide_code=True)
def _():
    # 2D plot
    """_df = df_selected.value.with_columns(
        ald_per_amine=(
            pl.col("aldehyde_monomer_amount_umol")
            / pl.col("aminoporphyrin_monomer_amount_umol")
        ),
        water_per_amine=(
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
            x=alt.X(field="ald_per_amine", type="quantitative"),
            y=alt.Y(field="water_per_amine", type="quantitative"),
            color=alt.Color(field="yield_MOCOF-1", type="quantitative"),
            tooltip=[
                alt.Tooltip(field="ald_per_amine", format=",.2f"),
                alt.Tooltip(field="water_per_amine", format=",.2f"),
                alt.Tooltip(field="yield_MOCOF-1", format=",.2f"),
            ],
        )
        .properties(height=290, width="container", config={"axis": {"grid": True}})
    )
    _chart"""
    return


@app.cell
def _(alt, df_selected):
    _chart = (
        alt.Chart(df_selected.value)
        .mark_circle(   # use mark_circle for filled circles
            size=60,    # adjust size as needed
            opacity=1
        )
        .encode(
            x=alt.X(field="water_per_aldeyde", type="quantitative",
                    scale=alt.Scale(type="log")),
            y=alt.Y(field="yield_MOCOF-1", type="quantitative"),
            tooltip=[
                alt.Tooltip(field="id"),
                # alt.Tooltip(field="water_per_aldeyde", format=",.1f"),
                # alt.Tooltip(field="yield_MOCOF-1", format=",.2f"),
            ],
        )
        .properties(height=290, width="container",
                    config={"axis": {"grid": False}}
                    )
    )
    _chart
    return


@app.cell
def _(ConvexHull, alt, df_selected, np, pl):
    _df = df_selected.value.filter(
        pl.col("water_per_aldeyde").is_not_null() & pl.col(
            "yield_MOCOF-1").is_not_null()
    )
    _points = np.column_stack([
        _df["water_per_aldeyde"].to_numpy(),
        _df["yield_MOCOF-1"].to_numpy()
    ])

    _hull = ConvexHull(_points)
    _hull_points = _points[_hull.vertices]
    _hull_closed = np.append(_hull_points, [_hull_points[0]], axis=0)

    # Build hull DataFrame in Polars
    _hull_df = pl.DataFrame({
        "water_per_aldeyde": _hull_closed[:, 0],
        "yield_MOCOF-1": _hull_closed[:, 1],
    })

    # --- Scatter plot with log x-axis ---
    _chart = (
        alt.Chart(_df)
        .mark_circle(   # use mark_circle for filled circles
            size=60,    # adjust size as needed
            opacity=1
        )
        .encode(
            x=alt.X(field="water_per_aldeyde", type="quantitative",
                    scale=alt.Scale(type="log")),
            y=alt.Y(field="yield_MOCOF-1", type="quantitative"),
            tooltip=[
                alt.Tooltip(field="id"),
            ],
        )
        .properties(height=290, width="container")
    )

    # --- Convex hull line overlay ---
    _hull_line = (
        alt.Chart(_hull_df)
        .mark_line(color='lightblue')
        .encode(
            x="water_per_aldeyde",
            y="yield_MOCOF-1"
        )
    )

    # --- Combine plots ---
    _final_chart = (
        (_chart + _hull_line)
        .configure_axis(grid=False)  # for axis config
    )

    _final_chart
    return


@app.cell
def _(alt, df_selected):
    _df = df_selected.value
    # Sort your dataframe by the desired column
    sorted_df = _df.sort("acid_pKa_DMSO")

    # Extract your ordered acid names as a list
    acid_order = sorted_df["acid_name"].to_list()

    # Pass this order to Altair's sort argument
    _chart = (
        alt.Chart(_df)
        .mark_circle(   # use mark_circle for filled circles
            size=60,    # adjust size as needed
            opacity=1
        )
        .encode(
            x=alt.X(field="acid_name", type="nominal", sort=acid_order),
            y=alt.Y(field="yield_MOCOF-1", type="quantitative"),
            tooltip=[
                alt.Tooltip(field="id"),
            ],
        )
        .properties(height=290, width="container", config={"axis": {"grid": True}})
    )
    _chart
    return


@app.cell
def _(ConvexHull, alt, df_selected, np, pl):
    import pandas as pd

    # Convert Polars dataframe to pandas for calculation and Altair
    _df = df_selected.value.filter(pl.col("acid_name") != "Scandium triflate")
    _df_pd = _df.to_pandas().dropna(subset=["acid_pKa_DMSO", "yield_MOCOF-1"])

    # Get X and Y as arrays
    _x_vals = _df_pd["acid_pKa_DMSO"].values
    _y_vals = _df_pd["yield_MOCOF-1"].values

    # Compute hull
    _points = np.column_stack([_x_vals, _y_vals])
    _hull = ConvexHull(_points)
    _hull_vertices = np.append(_hull.vertices, _hull.vertices[0])  # Close path

    _hull_df = pd.DataFrame({
        "acid_pKa_DMSO": _x_vals[_hull_vertices],
        "yield_MOCOF-1": _y_vals[_hull_vertices]
    })

    _scatter = (
        alt.Chart(_df_pd)
        .mark_circle(   # use mark_circle for filled circles
            size=20,    # adjust size as needed
            opacity=1
        )
        .encode(
            x=alt.X('acid_pKa_DMSO', type='quantitative',
                    title='Acid pKa(DMSO)'),
            y=alt.Y('yield_MOCOF-1', type='quantitative',
                    title='MOCOF-1 yield'),
            tooltip=[
                alt.Tooltip('acid_name'),
                alt.Tooltip('id'),
            ]
        )
    )

    _hull_line = (
        alt.Chart(_hull_df)
        .mark_line(color='lightblue', strokeWidth=2)
        .encode(
            x='acid_pKa_DMSO',
            y='yield_MOCOF-1'
        )
    )

    _final_chart = (
        (_hull_line + _scatter)
        .properties(width=285, height=110)
        .configure_axis(labelFontSize=8, titleFontSize=10, titleFontWeight='normal')
    )
    _final_chart
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
