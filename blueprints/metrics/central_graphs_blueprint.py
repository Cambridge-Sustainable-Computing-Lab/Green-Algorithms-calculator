"""
Blueprint for the "Import-Export and First Outputs" section of the home page.

Bundles the core-metrics section, the import/export module, the three dynamic
graphs (cores/memory pie chart, manufacturing-vs-usage pie chart, and location
comparison bar chart), the equivalents-metrics section, and the suggestions
box. Owns the callbacks that produce the graph figures, since they're specific
to this section of the page.
"""

import os
from types import SimpleNamespace

from dash import Input, Output, dcc, html
from dash_extensions.enrich import DashBlueprint

from blueprints.import_export.import_export_blueprint import ImportExportBlueprint
from blueprints.metrics.core_metrics_blueprint import CoreImpactsBlueprint
from blueprints.metrics.equivalent_metrics_blueprint import EquivalentsMetricsBlueprint
from blueprints.translation.translatable_div_text_blueprint import translatable_div_text
from blueprints.translation.translatable_markdown_text_blueprint import (
    translatable_markdown_text,
)
from utils.graphics import (
    BLANK_FIGURE,
    create_ci_bar_chart_graphic,
    create_cores_memory_pie_graphic,
    create_manufacturing_carbon_pie_graphic,
    loading_wrapper,
)

image_dir = os.path.join("assets", "images")

class CentralGraphsBlueprint(DashBlueprint):
    def __init__(self, id_prefix: str):
        super().__init__()
        self.id_prefix = id_prefix

        #### SUB-MODULES ####
        self.core_metrics = CoreImpactsBlueprint(id_prefix=id_prefix)
        self.import_export = ImportExportBlueprint(id_prefix=id_prefix)
        self.equivalents_metrics = EquivalentsMetricsBlueprint(id_prefix=id_prefix)

        self.layout = self._get_layout()
        self._register_callbacks()

    ###################################################
    # LAYOUT

    def _get_layout(self):
        return html.Div(
            [
                # self.import_export.embed(self),
                #### DYNAMIC GRAPHS ####
                html.Div(
                    [
                        html.Div(
                            [
                                html.P(
                                    "What is included in the calculator?", style={"font-weight": "bold"}
                                ),
                                html.Img(
                                    src=os.path.join(image_dir, "inclusion_static_graph.png"),
                                    id="inclusion_graph",
                                    className="inclusion-graph",
                                    style={"width": "320px", "padding": "5px"},
                                )
                            ],
                            style={"width": "50%", "padding-right": "10px"}
                        ),
                        html.Div(
                            [
                                html.P("What the calculator does not include?", style={"font-weight": "bold"}),
                                html.P(
                                    "Other environmental impact such as water use, e-waste produced, changes to land use on site of the computing facilities that could impact biodiversity and local populations."
                                )
                            ],
                            style={"width": "50%", "padding-left": "10px"}
                        ),
                    ],
                    className="container inclusion-exclusion",
                    style={"display": "flex", "flex-direction": "row", "align-items": "flex-start"}
                ),
                html.Div(
                    [
                        # html.Div(
                        #     [
                                ## Manuacturing vs Usage Pie Chart
                                html.Div(
                                    [
                                        html.H3(
                                            translatable_div_text(
                                                "Manufacturing_impacts_vs_usage"
                                            ).embed(self)
                                        ),
                                        loading_wrapper(
                                            dcc.Graph(
                                                id="manufacturing_pie_graph",
                                                className="graph-container pie-graph",
                                                config={"displaylogo": False},
                                                figure=BLANK_FIGURE,
                                            )
                                        ),
                                    ],
                                    className="one-of-two-graphs",
                                ),
                                ## Computing Cores vs Memory Pie Chart
                                html.Div(
                                    [
                                        html.H3(
                                            translatable_div_text(
                                                "Computing_cores_VS_Memory"
                                            ).embed(self)
                                        ),
                                        loading_wrapper(
                                            dcc.Graph(
                                                id="pie_graph",
                                                className="graph-container pie-graph",
                                                config={"displaylogo": False},
                                                figure=BLANK_FIGURE,
                                            )
                                        ),
                                    ],
                                    className="one-of-two-graphs",
                                ),
                        #     ],
                        #     className="container pie-graphs-container",
                        # ),
                        ## Location impact bar chart
                        html.Div(
                            [
                                html.H3(
                                    translatable_div_text(
                                        "Location_impact_graphs_title"
                                    ).embed(self)
                                ),
                                loading_wrapper(
                                    dcc.Graph(
                                        id="barPlotComparison",
                                        className="graph-container",
                                        config={"displaylogo": False},
                                        figure=BLANK_FIGURE,
                                        style={"margin-top": "20px"},
                                    ),
                                ),
                            ],
                            className="one-of-two-graphs",
                        ),
                    ],
                    className="container central-graphs",
                ),
            ],
            className="container central-box",
        )

    ###################################################
    # CALLBACKS

    def _register_callbacks(self):
        @self.callback(
            Output("pie_graph", "figure"),
            [
                Input(f"{self.id_prefix}-form_aggregate_data", "data"),
                Input(f"{self.id_prefix}-form_output_metrics", "data"),
            ],
        )
        def create_pie_graph(form_agg_data, form_metrics):
            return create_cores_memory_pie_graphic(form_agg_data, form_metrics)

        @self.callback(
            Output("manufacturing_pie_graph", "figure"),
            Input(f"{self.id_prefix}-form_output_metrics", "data"),
        )
        def create_manufacturing_pie_graph(form_metrics):
            return create_manufacturing_carbon_pie_graphic(form_metrics)

        # FIXME: looks weird with 0 emissions
        @self.callback(
            Output("barPlotComparison", "figure"),
            [
                Input(f"{self.id_prefix}-form_output_metrics", "data"),
                Input("versioned_data", "data"),
            ],
        )
        def create_bar_chart(form_metrics, versioned_data):
            if versioned_data is not None:
                versioned_data_ns = SimpleNamespace(**versioned_data)
                return create_ci_bar_chart_graphic(form_metrics, versioned_data_ns)
            return None
