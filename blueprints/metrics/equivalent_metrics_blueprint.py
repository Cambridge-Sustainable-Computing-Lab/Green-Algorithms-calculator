import os
from types import SimpleNamespace

from dash import dcc, html
from dash_extensions.enrich import (
    DashBlueprint,
    Input,
    Output,
    PrefixIdTransform,
    State,
)

from blueprints.metrics import utils
from blueprints.translation.translatable_div_text_blueprint import translatable_div_text
from utils.graphics import loading_wrapper
from utils.utils import custom_prefix_escape

image_dir = os.path.join("assets", "images")


class EquivalentsMetricsBlueprint(DashBlueprint):
    """
    Blueprint for displaying environmental equivalencies (trees, car trips, plane trips).
    """

    def __init__(self, id_prefix: str):
        super().__init__(
            transforms=[
                PrefixIdTransform(prefix=id_prefix, escape=custom_prefix_escape)
            ]
        )
        self.layout = self._get_layout()
        self._define_callbacks()

    def _get_layout(self):
        return (
            html.Div(
                [
                    dcc.Store(id="base_results"),
                    html.H2(translatable_div_text("comparison_heading").embed(self)),
                    #### TREE ABSORPTION EQUIVALENT ####
                    html.Div(
                        [
                            html.Img(
                                src=os.path.join(image_dir, "logo_tree_1.svg"),
                                id="logo_tree",
                                className="style-icon",
                                style={"padding": "15px", "padding-bottom": "0px"},
                            ),
                            html.Div(
                                [
                                    loading_wrapper(html.Div(id="treeMonths_text")),
                                    html.P(
                                        translatable_div_text(
                                            "Carbon_sequestration"
                                        ).embed(self)
                                    ),
                                ],
                                className="caption-icons",
                            ),
                        ],
                    ),
                    #### CAR KILOMETERS EQUIVALENT ####
                    html.Div(
                        [
                            html.Img(
                                src=os.path.join(image_dir, "logo_car_3.svg"),
                                id="logo_car",
                                className="style-icon",
                                style={"padding": "13px", "padding-bottom": "0px"},
                            ),
                            html.Div(
                                [
                                    loading_wrapper(html.Div(id="driving_text")),
                                    html.P(
                                        [
                                            translatable_div_text(
                                                "in_a_passenger_car"
                                            ).embed(self),
                                            html.Span(
                                                [
                                                    html.Span(
                                                        "i",
                                                        className="tooltip-icon",
                                                    ),
                                                    html.Span(
                                                        translatable_div_text(
                                                            "in_a_passenger_car_tooltip"
                                                        ).embed(self),
                                                        className="tooltip-text",
                                                    ),
                                                ],
                                                className="tooltip",
                                            ),
                                        ]
                                    ),
                                ],
                                className="caption-icons",
                            ),
                        ],
                    ),
                    #### PLANE TRIPS EQUIVALENT ####
                    html.Div(
                        [
                            html.Img(
                                src=os.path.join(image_dir, "logo_plane_1.svg"),
                                id="logo_plane",
                                className="style-icon",
                                style={"padding": "4px", "padding-bottom": "0px"},
                            ),
                            html.Div(
                                [
                                    loading_wrapper(html.Div(id="flying_text")),
                                    html.P(id="flying_label"),
                                ],
                                className="caption-icons",
                            ),
                        ],
                    ),
                ],
                className="equivalent-metrics-container",
            )
        )

    def _define_callbacks(self):
        @self.callback(
            [
                Output("treeMonths_text", "children"),
                Output("driving_text", "children"),
                Output("flying_text", "children"),
                Output("flying_label", "children"),
            ],
            [
                Input("base_results", "data"),
                Input("language_dropdown", "value"),
            ],
            State("versioned_data", "data"),
        )
        def update_equivalents_results(
            results_dict: dict, language_id: str, versioned_data: dict
        ):
            if not results_dict or versioned_data is None:
                return "", "", "", ""

            carbon_emissions = results_dict.get("carbonEmissions", 0)  # in g CO2e
            v_data = SimpleNamespace(**versioned_data)

            text_ty = utils.write_tree_months_equivalent(
                carbon_emissions, v_data.refValues_dict
            )
            text_car = utils.write_driving_equivalent(
                carbon_emissions, v_data.refValues_dict
            )
            text_trip_proportion, flying_text = utils.write_plane_trip_equivalent(
                carbon_emissions, v_data.refValues_dict, language_id
            )

            return text_ty, text_car, text_trip_proportion, flying_text
