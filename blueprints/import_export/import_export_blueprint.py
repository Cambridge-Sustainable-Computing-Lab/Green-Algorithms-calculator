"""
Implements the import-export blueprint.
"""

import pandas as pd
import datetime

from dash import ctx, dcc, html
import dash_bootstrap_components as dbc
from dash_extensions.enrich import (
    DashBlueprint,
    PrefixIdTransform,
    Output,
    Input,
    State,
)
from dash.exceptions import PreventUpdate

from utils.utils import custom_prefix_escape
from blueprints.translation.translatable_div_text_blueprint import translatable_div_text
from blueprints.translation.translatable_markdown_text_blueprint import (
    translatable_markdown_text,
)


class ImportExportBlueprint(DashBlueprint):
    """
    When a csv is uploaded, the `dcc.Upload` component (id=upload-data) is
    automatically flushed after few seconds to let the user upload the same file again.
    Otherwise, the callbacks with Input upload-data would not trigger because upload-data
    actually remained the same.
    """

    def __init__(self, id_prefix: str, csv_flushing_delay: int = 1500):
        """
        Args:
            id_prefix (str): id prefix automatically applied to all components.
            csv_flushing_delay (int, optional): time delay between csv upload and csv flushing.
            Given in milliseconds. Defaults to 1500.
        """
        super().__init__(
            transforms=[
                PrefixIdTransform(prefix=id_prefix, escape=custom_prefix_escape)
            ]
        )
        self.layout = self._get_layout(csv_flushing_delay)
        self._define_callbacks()

    def _get_layout(self, csv_flushing_delay: int):
        return html.Div(
            [
                #### BACKEND DATA ####
                # Intermediate variable used to read the uploaded data only once
                # Its is then forwarded to the target form(s) depending on the page
                dcc.Store(id="import-content"),
                # Intermediate variable that is updated only when the user want to export data as csv.
                # It is useful as it allows to run the callback only once per export, not after each form modification.
                dcc.Store(id="export-content"),
                html.Div(
                    [
                        #### EXPORT DATA ####
                        html.Div(
                            [
                                html.Button(
                                    translatable_div_text("Share_your_results").embed(
                                        self
                                    ),
                                    id="btn-download_csv",
                                    className="btn-download_csv",
                                    type="button",
                                ),
                                dcc.Download(id="aggregate-data-csv"),
                            ],
                            # className="container footer import-export",
                            id="export-result",
                        ),
                        #### IMPORT DATA ####
                        html.Div(
                            dcc.Upload(
                                html.Div(
                                    [
                                        html.P(
                                            translatable_markdown_text(
                                                "Import_results"
                                            ).embed(self)
                                        ),
                                        html.Div(
                                            [
                                                html.A(
                                                    translatable_div_text(
                                                        "drag_and_drop"
                                                    ).embed(self),
                                                    style={
                                                        "font-size": "12px",
                                                        "margin-top": "3px",
                                                        "text-decoration": "underline",
                                                    },
                                                )
                                            ],
                                        ),
                                    ],
                                    role="button",
                                    tabIndex=0,
                                ),
                                id="upload-data",
                                className="upload-data",
                            ),
                            id="import-result",
                        ),
                    ],
                    className="import-export-buttons",
                ),
                #### ERROR MESSAGE ####
                dbc.Alert(
                    [
                        html.H3(
                            translatable_div_text("error_message_header").embed(self),
                            id="error-message-title",
                            className="error-message-title",
                        ),
                        dcc.Markdown(
                            id="log-error-subtitle", className="log-error-subtitle"
                        ),
                        dcc.Markdown(
                            id="log-error-content", className="log-error-content"
                        ),
                    ],
                    className="container footer import-error-message",
                    id="import-error-message",
                    is_open=False,
                    duration=60000,
                ),
                dcc.Interval(
                    id="csv-input-timer",
                    interval=csv_flushing_delay,
                    # in milliseconds, should not be lower than 1000
                    # otherwise the update of the upload csv content is done too soon
                    # and there is not consistency between the state of the form and
                    # the content  of the csv
                    disabled=True,
                ),
            ],
            id="import-export",
            className="import-export-container",
        )

    def _define_callbacks(self):
        """
        Embeds all the internal callbacks to the blueprint
        """
        ################## EXPORT DATA

        @self.callback(
            Output("aggregate-data-csv", "data"),
            Input("export-content", "data"),
            prevent_initial_call=True,
        )
        def export_as_csv(aggregate_data):
            """
            Exports the aggregate_data.
            TODO: modify the suffix strategy because not robust with respect to the prefix of the AI page's components
            """
            file_suffixe = ""
            if ctx.triggered_id is not None and "ai-" in ctx.triggered_id:
                file_suffixe = "AI"
            now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            to_export = pd.DataFrame.from_dict(aggregate_data, orient="columns")
            return dcc.send_data_frame(
                to_export.to_csv,
                f"GreenAlgorithms_results_{file_suffixe}_{now}.csv",
                index=False,
                sep=";",
            )

        ################## IMPORT DATA

        @self.callback(
            Output("import-content", "data"),
            Input("upload-data", "contents"),
            State("import-content", "data"),
        )
        def read_input(upload_content: dict, current_import_data: dict):
            """
            Open input file and extract data from csv if possible.
            Does not process the content, just proceeds to raw extraction.
            """
            # NOTE this callback fires for no reason (ctx.triggered_id is None) which happens after each regular trigger of the callback
            # this is also the case for most of the callbacks taking the csv upload content as input, and was already the case when using
            # the url instead of csv files for sharing the results
            # TODO understand this behaviour
            if ctx.triggered_id is None:
                raise PreventUpdate

            # The following case only happens when the upload-data is automatically flushed
            # Therefore, we want to return the data that was previously uploaded
            if upload_content is None:
                return current_import_data

            return upload_content

        @self.callback(
            Output("upload-data", "contents"),
            Input("csv-input-timer", "n_intervals"),
            prevent_initial_call=True,
        )
        def flush_input_csv_content(n):
            """
            Flushes the input csv.
            This is required if we want to enable the user to load the same csv again.
            Otherwise, if not flushed, the csv content does not change so it does not trigger
            the reading of its content.
            """
            return None

        @self.callback(
            Output("csv-input-timer", "disabled"),
            Input("upload-data", "contents"),
            prevent_initial_call=True,
        )
        def trigger_timer_to_flush_input_csv(input_csv):
            """
            When a csv is dropped, triggers a timer that allows to flush this csv.
            If the input is none, this means that we just flushed it so we do not
            trigger the timer again.
            """
            return input_csv is None
