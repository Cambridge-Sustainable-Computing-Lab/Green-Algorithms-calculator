"""
The page itself is defined as a `DashBlueprint` that encompasses both layout and callbacks.

The layout is a combination Dash components directly implemented in this script and
modules' layout inserted as blueprints (the form, import-export section or results section).
Such modules also contain their own callbacks that will first be registered as page callbacks
and then, when the page is registered in the app, as app callbacks.
"""

import os
from types import SimpleNamespace

import plotly.graph_objects as go
from dash import Input, Output, State, dcc, html
from dash_extensions.enrich import DashBlueprint, html  # noqa: F811

from blueprints.form.form_blueprint import FormBlueprint
from blueprints.import_export.import_export_blueprint import ImportExportBlueprint
from blueprints.methodology.methodology_blueprint import MethodologyBlueprint
from blueprints.metrics.central_graphs_blueprint import CentralGraphsBlueprint
from blueprints.metrics.core_metrics_blueprint import CoreImpactsBlueprint
from blueprints.metrics.equivalent_metrics_blueprint import EquivalentsMetricsBlueprint
from blueprints.translation.translatable_div_text_blueprint import translatable_div_text
from blueprints.translation.translatable_markdown_text_blueprint import (
    translatable_markdown_text,
)
from blueprints.translation.translation_dicts import TRANSLATIONS_DICT
from utils.graphics import (
    BLANK_FIGURE,
    create_ci_bar_chart_graphic,
    create_cores_bar_chart_graphic,
    create_cores_memory_pie_graphic,
    loading_wrapper,
)
from utils.handle_inputs import (
    AGGREGATE_DATA_UNITS,
    clean_non_used_inputs_for_export,
    filter_wrong_inputs,
    open_input_csv_and_comment,
    read_base_form_inputs_from_csv,
)
from utils.utils import write_error_message

###################################################
# PAGE CREATION

HOME_PAGE = DashBlueprint()

HOME_PAGE_ID_PREFIX = "main"


###################################################
# MODULES CREATION

# TODO add a "help" tab on the home form as well (similar to the AI one)
form = FormBlueprint(
    id_prefix=HOME_PAGE_ID_PREFIX,
    title="Details about your algorithm",
    subtitle="Home_form_subtitle",
)

methodology_content = MethodologyBlueprint(id_prefix=HOME_PAGE_ID_PREFIX)

# metrics = MetricsBlueprint(id_prefix=HOME_PAGE_ID_PREFIX)
core_metrics = CoreImpactsBlueprint(id_prefix=f"{HOME_PAGE_ID_PREFIX}")
equivalents_metrics = EquivalentsMetricsBlueprint(id_prefix=f"{HOME_PAGE_ID_PREFIX}")

import_export = ImportExportBlueprint(id_prefix=HOME_PAGE_ID_PREFIX)
central_graphs = CentralGraphsBlueprint(id_prefix=HOME_PAGE_ID_PREFIX)


###################################################
# DEFINE PAGE LAYOUT


def get_home_page_layout():
    page_layout = html.Div(
        [
            #### INPUT FORM ####
            form.embed(HOME_PAGE),
            #### IMPORT-EXPORT AND FIRST OUTPUTS ####
            html.Div(
                [
                    html.Div(
                        [
                            core_metrics.embed(HOME_PAGE),
                            html.Div(
                                [
                                    import_export.embed(HOME_PAGE),
                                    #### DYNAMIC GRAPHS ####
                                    central_graphs.embed(HOME_PAGE),
                                ],
                                className="container metrics-output",
                            ),
                        ],
                        className="super-section metrics-output",
                    ),
                    html.Div(
                        [
                            equivalents_metrics.embed(HOME_PAGE),
                            html.Div(
                                [
                                    html.H3(
                                        translatable_div_text(
                                            "Questions_suggestions"
                                        ).embed(HOME_PAGE)
                                    ),
                                    html.P(
                                        translatable_markdown_text("Questions_suggestions_text").embed(
                                            HOME_PAGE
                                        )
                                    ),
                                ],
                                className="suggestions-container",
                            ),
                        ],
                        className="super-section mini-boxes",
                    ),
                ],
                className="super-section first-output",
            ),
            #### METHODOLOGY CONTENT ####
            methodology_content.embed(HOME_PAGE),
            #### HOW TO REPORT ####
            html.Div(
                [
                    html.H2(
                        translatable_div_text("How_to_report_it?").embed(HOME_PAGE)
                    ),
                    html.Div(
                        translatable_markdown_text("Report_text_header").embed(
                            HOME_PAGE
                        )
                    ),
                    dcc.Markdown(id="report_markdown"),
                    html.Div(
                        translatable_markdown_text("Report_text_reference").embed(
                            HOME_PAGE
                        ),
                        className="footnote citation-report",
                    ),
                    html.Div(
                        translatable_markdown_text("Report_text_footer").embed(
                            HOME_PAGE
                        ),
                        className="footnote-authorship",
                    ),
                ],
                className="container report",
            ),
            #### CORES COMPARISON ####
            html.Div(
                [
                    html.H2(
                        translatable_div_text(
                            "Power_draw_of_different_processors"
                        ).embed(HOME_PAGE)
                    ),
                    html.Div(
                        [
                            loading_wrapper(
                                dcc.Graph(
                                    id="barPlotComparison_cores",
                                    config={"displaylogo": False},
                                    figure=BLANK_FIGURE,
                                ),
                            ),
                        ],
                        className="graph-container",
                    ),
                ],
                className="container core-comparison",
            ),
        ],
        className="page_content",
    )

    return page_layout


HOME_PAGE.layout = get_home_page_layout()


###################################################
# DEFINE CALLBACKS

################## LOAD PAGE AND INPUTS


@HOME_PAGE.callback(
    [
        Output(f"{HOME_PAGE_ID_PREFIX}-form_data_imported_from_csv", "data"),
        Output(f"{HOME_PAGE_ID_PREFIX}-import-error-message", "is_open"),
        Output(f"{HOME_PAGE_ID_PREFIX}-log-error-subtitle", "children"),
        Output(f"{HOME_PAGE_ID_PREFIX}-log-error-content", "children"),
        Output(f"{HOME_PAGE_ID_PREFIX}-version_from_input", "data"),
    ],
    [
        Input(f"{HOME_PAGE_ID_PREFIX}-import-content", "data"),
    ],
    [
        State(f"{HOME_PAGE_ID_PREFIX}-upload-data", "filename"),
        State(f"{HOME_PAGE_ID_PREFIX}-form_aggregate_data", "data"),
        State("app_versions_dropdown", "value"),
        State("language_dropdown", "value"),
        # the language should not be an input because must be triggered by imported csv only
    ],
)
def forward_imported_content_to_form(
    import_data: str,
    filename: str,
    current_form_data: dict,
    current_app_version: str,
    language_id: str,
):
    """
    Processes the raw input dictionary and checks content before
    forwarding it to fill the main page form in.
    Produces error messages depending on the csv content.

    The error message is designed so the user better knows what to do
    in order to fix its csv. Details are given regarding the nature of the error
    and the fields of the csv containing the error. However, there is a very
    wide range of error kinds and we do not pretend to cover all of them.
    We focus on the use cases that are more likely.
    TODO: create an 'unknown_inputs' category.
    """
    show_err_mess = False
    input_data, mess_subtitle, mess_content = open_input_csv_and_comment(
        import_data, filename, language_id
    )

    # The input file could not be opened correctly
    if not input_data:
        input_data = current_form_data
        show_err_mess = True

        return (
            input_data,
            show_err_mess,
            mess_subtitle,
            mess_content,
            current_app_version,
        )

    # If input data could be read, we check its validity and consistency
    else:
        clean_inputs, invalid_inputs, missing_inputs, app_version = (
            read_base_form_inputs_from_csv(input_data)
        )
        # We want to detect whether an imported csv has been produced before we implemented the manufacturing impacts
        # because at that time the fields 'TDPcpu' and 'TDPgpu' were actually per core values, which is not anymore
        # Thus, if someone uses a custom TDPcpu from a previous version, the tdp value will be wrong (and largely underestimated)
        if ("CPU_model_n_cores" in missing_inputs) and (
            "CPU_die_area" in missing_inputs
        ):
            mess_subtitle = TRANSLATIONS_DICT["old_version_error_subtitle"][language_id]
        else:
            mess_subtitle = mess_subtitle = TRANSLATIONS_DICT["default_error_subtitle"][
                language_id
            ]
        invalid_inputs = filter_wrong_inputs(clean_inputs, invalid_inputs)
        show_err_mess, mess_content = write_error_message(
            missing_inputs, list(invalid_inputs.keys()), language_id, show_err_mess
        )
        return clean_inputs, show_err_mess, mess_subtitle, mess_content, app_version


################## EXPORT DATA


@HOME_PAGE.callback(
    Output(f"{HOME_PAGE_ID_PREFIX}-export-content", "data"),
    Input(f"{HOME_PAGE_ID_PREFIX}-btn-download_csv", "n_clicks"),
    State(f"{HOME_PAGE_ID_PREFIX}-form_aggregate_data", "data"),
    State(f"{HOME_PAGE_ID_PREFIX}-form_output_metrics", "data"),
    prevent_initial_call=True,
)
def forward_form_input_to_export_module(_, form_aggregate_data, form_output_metrics):
    """
    Intermediate processing specific to the HOME page before exporting data.
    We forward the inputs of the form to the export file along with the main outputs.
    """
    to_export = {}
    # Raw inputs of the form
    form_aggregate_data = clean_non_used_inputs_for_export(form_aggregate_data)
    to_export.update(form_aggregate_data)
    # Outputs of the form
    to_export.update(form_output_metrics)
    # Adding units
    to_export = {
        key: [str(AGGREGATE_DATA_UNITS[key]), str(val)]
        for key, val in to_export.items()
    }
    return to_export


################## RESULTS AND METRICS


@HOME_PAGE.callback(
    Output(f"{HOME_PAGE_ID_PREFIX}-base_results", "data"),
    Input(f"{HOME_PAGE_ID_PREFIX}-form_output_metrics", "data"),
)
def forward_results_from_form_to_metrics(form_metrics):
    return {
        "energy_needed": form_metrics["energy_needed"],
        "carbonEmissions": form_metrics["carbonEmissions"],
    }


# ## OUTPUT GRAPHICS


@HOME_PAGE.callback(
    Output("barPlotComparison_cores", "figure"),
    [
        Input(f"{HOME_PAGE_ID_PREFIX}-form_aggregate_data", "data"),
        Input("versioned_data", "data"),
    ],
)
def create_bar_chart_cores(form_agg_data, versioned_data):
    if versioned_data is not None:
        versioned_data = SimpleNamespace(**versioned_data)
        if form_agg_data["coreType"] is None:
            return go.Figure()
        return create_cores_bar_chart_graphic(form_agg_data, versioned_data)
    return None


## OUTPUT SUMMARY


@HOME_PAGE.callback(
    Output("report_markdown", "children"),
    [
        Input(f"{HOME_PAGE_ID_PREFIX}-form_aggregate_data", "data"),
        Input("versioned_data", "data"),
        Input(f"{HOME_PAGE_ID_PREFIX}-carbonEmissions_text", "children"),
        Input(f"{HOME_PAGE_ID_PREFIX}-energy_text", "children"),
        Input(f"{HOME_PAGE_ID_PREFIX}-treeMonths_text", "children"),
    ],
)
def fillin_report_text(form_agg_data, versioned_data, text_CE, text_energy, text_ty):
    """
    Writes a summary text of the current computation that is shown as an example
    for the user on how to report its impact.
    """
    if (form_agg_data["numberCPUs"] is None) & (form_agg_data["numberGPUs"] is None):
        return ""
    elif versioned_data is None:
        return ""
    else:
        versioned_data = SimpleNamespace(**versioned_data)

        # Runtime text
        minutes = form_agg_data["runTime_min"]
        hours = form_agg_data["runTime_hour"]
        if (minutes > 0) & (hours > 0):
            textRuntime = "{}h and {}min".format(hours, minutes)
        elif hours > 0:
            textRuntime = "{}h".format(hours)
        else:
            textRuntime = "{}min".format(minutes)

        # Cores text
        textCores = ""
        if form_agg_data["coreType"] in ["GPU", "CPU + GPU"]:
            if form_agg_data["numberGPUs"] > 1:
                suffixProcessor = "s"
            else:
                suffixProcessor = ""
            textCores += f"{form_agg_data['numberGPUs']} GPU{suffixProcessor} {form_agg_data['GPUmodel']}"
        if form_agg_data["coreType"] == "CPU + GPU":
            textCores += " and "
        if form_agg_data["coreType"] in ["CPU", "CPU + GPU"]:
            if form_agg_data["numberCPUs"] > 1:
                suffixProcessor = "s"
            else:
                suffixProcessor = ""
            textCores += f"{form_agg_data['numberCPUs']} CPU{suffixProcessor} {form_agg_data['CPUmodel']}"

        # Memory text
        memory_in_GB = form_agg_data["memory"]

        # Location and carbon intensity
        if form_agg_data["location"] == "custom":
            location_text = f"Based on a custom carbon intensity of {form_agg_data['carbonIntensity']} gCO2e/kWh"

        else:
            location_text = "Based in "
            country = versioned_data.CI_dict_byLoc[form_agg_data["location"]][
                "countryName"
            ]
            region = versioned_data.CI_dict_byLoc[form_agg_data["location"]][
                "regionName"
            ]
            if region == "Any":
                textRegion = ""
            else:
                textRegion = " ({})".format(region)
            if country in ["United States of America", "United Kingdom"]:
                prefixCountry = "the "
            else:
                prefixCountry = ""
            location_text = location_text + prefixCountry + country + textRegion

        if form_agg_data["mult_factor"] > 1:
            text_mult_factor = " and ran {} times in total,".format(
                form_agg_data["mult_factor"]
            )
        else:
            text_mult_factor = ""

        # Final summary text
        myText = f"""
        > This algorithm runs in {textRuntime} on {textCores}, with {memory_in_GB} GB of allocated memory.
        > It draws {text_energy}. 
        > {location_text},{text_mult_factor} this has a carbon footprint of {text_CE}, which is equivalent to {text_ty}
        (calculated using green-algorithms.org {form_agg_data["appVersion"]} \[1\]).
        """

        return myText
