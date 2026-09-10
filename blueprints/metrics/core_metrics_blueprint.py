import os

from dash import dcc, html
from dash_extensions.enrich import DashBlueprint, Input, Output, PrefixIdTransform

from blueprints.metrics import utils
from blueprints.translation.translatable_div_text_blueprint import translatable_div_text
from utils.graphics import loading_wrapper
from utils.utils import custom_prefix_escape

image_dir = os.path.join("assets", "images")


class CoreImpactsBlueprint(DashBlueprint):
    """
    Blueprint for displaying core impact metrics: Carbon Footprint and Electricity Consumption.
    """

    def __init__(
        self,
        id_prefix: str,
        to_add_metrics_details: bool = False,
        training_id_prefix: str = None,
        inference_id_prefix: str = None,
    ):
        super().__init__(
            transforms=[
                PrefixIdTransform(prefix=id_prefix, escape=custom_prefix_escape)
            ]
        )

        self.energy_needed_details: html.Div = html.Div(style={"display": "none"})
        self.carbon_footprint_details: html.Div = html.Div(style={"display": "none"})

        if to_add_metrics_details:
            self.energy_needed_details = self._get_metric_per_form_layout(
                training_id=f"{training_id_prefix}-energy_needed",
                inference_id=f"{inference_id_prefix}-energy_needed",
            )
            self.carbon_footprint_details = self._get_metric_per_form_layout(
                training_id=f"{training_id_prefix}-carbon_emissions",
                inference_id=f"{inference_id_prefix}-carbon_emissions",
            )

        self.layout = self._get_layout()
        self._define_callbacks()

    def _get_metric_per_form_layout(self, training_id: str, inference_id: str):
        return html.P(
            [
                html.B("Training:"),
                html.B(
                    id=training_id, className="metric-per-form-value training-metric"
                ),
                html.B("Inference:", style={"padding-left": "10px"}),
                html.B(id=inference_id, className="metric-per-form-value"),
            ],
            className="detailed-metric-container",
        )

    def _get_layout(self):
        return html.Div(
            [
                dcc.Store(id="base_results"),
                html.H3("Your computation results in approximately:"),
                html.Div(
                    [
                        #### ELECTRICITY CONSUMPTION ####
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Img(
                                            src=os.path.join(
                                                image_dir, "logo_power_1.svg"
                                            ),
                                            id="logo_power",
                                            className="style-icon",
                                            style={
                                                "margin": "0px",
                                                "padding": "10px",
                                                "margin-right": "4px",
                                            },
                                        ),
                                        html.Div(
                                            [
                                                loading_wrapper(
                                                    html.Div(id="energy_text")
                                                ),
                                                html.P(
                                                    translatable_div_text(
                                                        "Energy_needed"
                                                    ).embed(self)
                                                ),
                                            ],
                                            className="caption-icons",
                                        ),
                                    ],
                                    className="mini-box-main-content",
                                ),
                                self.energy_needed_details,
                            ],
                            # className="container mini-box",
                        ),
                        #### CARBON EMISSIONS ####
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Img(
                                            src=os.path.join(image_dir, "logo_co2.svg"),
                                            id="logo_co2",
                                            className="style-icon",
                                            style={
                                                "margin-top": "-7px",
                                                "margin-bottom": "7px",
                                                "margin-right": "4px",
                                            },
                                        ),
                                        html.Div(
                                            [
                                                loading_wrapper(
                                                    html.Div(id="carbonEmissions_text")
                                                ),
                                                html.P(
                                                    translatable_div_text(
                                                        "Carbon_footprint"
                                                    ).embed(self)
                                                ),
                                            ],
                                            className="caption-icons",
                                        ),
                                    ],
                                    className="mini-box-main-content",
                                ),
                                self.carbon_footprint_details,
                            ],
                        ),
                    ],
                    className="core-metrics-container"
                ),
            ],
            className="super-section mini-boxes-core",
        )

    def _define_callbacks(self):
        @self.callback(
            [
                Output("carbonEmissions_text", "children"),
                Output("energy_text", "children"),
            ],
            [
                Input("base_results", "data"),
            ],
        )
        def update_core_results(results_dict: dict):
            if not results_dict:
                return "", ""

            energy_needed = results_dict.get("energy_needed", 0)
            text_energy = utils.format_energy_text(energy_needed)

            carbon_emissions = results_dict.get("carbonEmissions", 0)
            text_CE = utils.format_CE_text(carbon_emissions)

            return text_CE, text_energy
