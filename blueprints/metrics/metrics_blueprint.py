import os

from types import SimpleNamespace
from dash_extensions.enrich import DashBlueprint, PrefixIdTransform, Output, Input, State
from dash import html, dcc

from utils.utils import custom_prefix_escape
from utils.graphics import loading_wrapper
import blueprints.metrics.utils as utils

from blueprints.translation.translatable_div_text_blueprint import translatable_div_text

image_dir = os.path.join('assets/images')

class MetricsBlueprint(DashBlueprint):
    '''
    The Metrics blueprint is used to update and display the impacts metrics.
    '''
    def __init__(
            self,
            id_prefix: str,
            to_add_metrics_details: bool = False,
            training_id_prefix: str = None,
            inference_id_prefix: str = None,
        ):
        '''
        Args:
            id_prefix (str): id prefix automatically applied to all components.
            to_add_metrics_details (bool, optional): whether to add the detailed metrics for training and inference.
            training_id_prefix (str): for training details, the id prefix.
            inference_id_prefix (str): for inference details, the id prefix.
        '''
        super().__init__(transforms = [PrefixIdTransform(prefix = id_prefix, escape = custom_prefix_escape)])
        self.energy_needed_details: html.Div = html.Div(style={"display": "none"})
        self.carbon_footprint_details: html.Div = html.Div(style={"display": "none"})
        if to_add_metrics_details:
            self.energy_needed_details = self._get_metric_per_form_layout(
                training_id=f'{training_id_prefix}-energy_needed',
                inference_id=f'{inference_id_prefix}-energy_needed',
            )
            self.carbon_footprint_details = self._get_metric_per_form_layout(
                training_id=f'{training_id_prefix}-carbon_emissions',
                inference_id=f'{inference_id_prefix}-carbon_emissions',
            )
        self.layout = self._get_layout()
        self._define_callbacks()

    def _get_metric_per_form_layout(self, training_id:str, inference_id:str):
        '''
        The detailed metrics for training and inference phases.
        They are shown as raw textual information below the total impact in the layout.
        It can be used for any impact category.

        Args:
            training_id (str): the id of the training metric text that will be created
            inference_id (str): the id of the inference metric text that will be created
        '''
        return html.P(
            [
                html.B('Training:'),
                html.B(id=training_id, className='metric-per-form-value training-metric'),
                html.B('Inference:', style={'padding-left': '10px'}),
                html.B(id=inference_id, className='metric-per-form-value'),
            ],
            className='detailed-metric-container'
        )

    def _get_layout(self):
        return html.Div(
        [
            #### BACKEND DATA ####

            dcc.Store(id='base_results'),

            #### CARBON EMISSIONS ####
            
            html.Div(
                [
                    html.Div(
                        [

                            html.Img(
                                src=os.path.join(image_dir, 'logo_co2.svg'),
                                id="logo_co2",
                                className="style-icon",
                                style={
                                    'margin-top': '-7px',
                                    'margin-bottom': '7px'
                                },
                            ),

                            html.Div(
                                [
                                    loading_wrapper(html.Div(
                                        id="carbonEmissions_text",
                                    )),

                                    html.P(translatable_div_text("Carbon_footprint").embed(self))
                                ],
                                className='caption-icons'
                            ),
                        ],
                        className='mini-box-main-content'

                    ),

                    self.carbon_footprint_details,

                    html.Div(
                        [
                            html.Img(
                                src=os.path.join(image_dir, 'logo_power_1.svg'),
                                id="logo_power",
                                className="style-icon",
                                style={
                                    'margin': '0px',
                                    'padding': '15px'
                                },
                            ),

                            html.Div(
                                [
                                    loading_wrapper(html.Div(
                                        id="energy_text",
                                    )),

                                    html.P((translatable_div_text("Energy_needed").embed(self)))
                                ],
                                className='caption-icons'
                            ),
                        ],
                        className='mini-box-main-content'
                    ),
                    
                    self.energy_needed_details,
                ],
                className="container mini-box"
            ),

            #### ELECTRICITY CONSUMPTION ####

            # html.Div(
            #     [
                    
            #     ],
            #     className="container mini-box"
            # ),

            #### TREE ABSOPRTION EQUIVALENT ####

            html.Div(
                [
                    html.Img(
                        src=os.path.join(image_dir, 'logo_tree_1.svg'),
                        id="logo_tree",
                        className="style-icon",
                        style={
                            'padding': '15px'
                        },
                    ),

                    html.Div(
                        [
                            loading_wrapper(html.Div(
                                id="treeMonths_text",
                            )),

                            html.P(translatable_div_text("Carbon_sequestration").embed(self))
                        ],
                        className='caption-icons'
                    )

                ],
                className="container mini-box"
            ),

            #### CAR KILOMETERS EQUIVALENT ####

            html.Div(
                [
                    html.Img(
                        src=os.path.join(image_dir, 'logo_car_3.svg'),
                        id="logo_car",
                        className="style-icon",
                        style={
                            'padding': '13px'
                        },
                    ),
                    html.Div(
                        [
                            loading_wrapper(html.Div(id="driving_text")),
                            html.P(
                                [
                                    translatable_div_text("in_a_passenger_car").embed(self),
                                    html.Span(
                                        [
                                            html.Span('i', className='tooltip-icon'),
                                            html.Span(
                                                translatable_div_text("in_a_passenger_car_tooltip").embed(self),
                                                className='tooltip-text'
                                            ),
                                        ],
                                        className='tooltip',
                                    ),
                                ]
                            ),
                        ],
                        className='caption-icons'
                    ),
                ],
                className="container mini-box"
            ),

            #### PLANE TRIPS EQUIVALENT ####

            html.Div(
                [
                    html.Img(
                        src=os.path.join(image_dir, 'logo_plane_1.svg'),
                        id="logo_plane",
                        className="style-icon",
                        style={
                            'padding': '4px'
                        },
                    ),

                    html.Div(
                        [
                            loading_wrapper(html.Div(id="flying_text")),

                            html.P(id="flying_label"),
                        ],
                        className='caption-icons'
                    )
                ],
                className="container mini-box"
            ),
        ],
        className='super-section mini-boxes'
    )

    def _define_callbacks(self): 
        ''' 
        Embeds all the internal callbacks to the blueprint
        '''
        
        @self.callback(
            [
                Output("carbonEmissions_text", "children"),
                Output("energy_text", "children"),
                Output("treeMonths_text", "children"),
                Output("driving_text", "children"),
                Output("flying_text", "children"),
                Output("flying_label", "children"),
            ],
            [
                Input(f'base_results', 'data'),
                Input('language_dropdown', 'value'),
            ],
            State('versioned_data', 'data'),
        )
        def update_results_and_texts(results_dict: dict, language_id: str, versioned_data: dict):
            '''
            Updated the metrics displayed and the corresponding label

            Args:
                results_dict (dict): the dictionary from the form results
                versioned_data (dict): the backend data
                language_id (dict): the language identifier for translation purpose
            '''
            # Retrieve base results
            energy_needed = results_dict['energy_needed']  # in kWh
            text_energy = utils.format_energy_text(energy_needed)
            carbon_emissions = results_dict['carbonEmissions']  # in g CO2e
            text_CE = utils.format_CE_text(carbon_emissions)
            # Compute corresponding metrics
            if versioned_data is not None: 
                versioned_data = SimpleNamespace(**versioned_data)
                text_ty = utils.write_tree_months_equivalent(carbon_emissions, versioned_data.refValues_dict)
                text_car = utils.write_driving_equivalent(carbon_emissions, versioned_data.refValues_dict)
                text_trip_proportion, flying_text = utils.write_plane_trip_equivalent(carbon_emissions, versioned_data.refValues_dict, language_id)
            else:
                text_ty, text_car, text_trip_proportion, flying_text = '', '', '', ''
            return text_CE, text_energy, text_ty, text_car, text_trip_proportion, flying_text