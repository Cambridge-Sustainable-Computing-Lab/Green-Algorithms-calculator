'''
Implements the form blueprint.
'''

import pandas as pd
import dash_mantine_components as dmc

from dash import html, dcc
from dash_extensions.enrich import DashBlueprint, Output, Input, State, PrefixIdTransform, ctx, html
from types import SimpleNamespace

from utils.utils import get_yes_or_no_options, put_value_first, is_shown, custom_prefix_escape
from utils.handle_inputs import get_available_versions,  availableLocations_continent, availableOptions_servers, availableOptions_country, availableOptions_region, DEFAULT_VALUES_FOR_PAGE_LOAD
from utils.graphics import MY_COLORS

from blueprints.translation.translatable_div_text_blueprint import translatable_div_text
from blueprints.translation.translatable_markdown_text_blueprint import translatable_markdown_text
from blueprints.translation.translation_dicts import TRANSLATIONS_DICT

appVersions_options = get_available_versions()

custom_core_box_style = {'padding': '6px 24px', 'border': 'rgb(220, 220, 220)', 'border-radius': '10px', 'border-style': 'dashed', 'border-width': '2px'}
use_case_options = ["calculate the emissions of my algorithm", "play around and explore computation's carbon footprint", "learn about carbon footprint of compute", "plan around possible carbon footprint of compute"]

class FormBlueprint(DashBlueprint):
    '''
    The calculator form blueprint.
    The class constructor builds the blueprint layout and the associated callbacks. So,
    when calling an instance of this class, one gest a fully functional form blueprint.
    
    TODO: remove the continuous inference section from the form blueprint,
    as it should not belong to the base Form module. Instead, the right 
    way to embed the continuous inference section in the inference form should 
    be to pass it as an argument to this function.
    '''

    def __init__(
        self,
        id_prefix: str,
        title: str,
        subtitle: str,
        continuous_inf_scheme_properties: dict = {'display': 'none'},
        mult_factor_properties: dict = {},
        to_add_bottom_training_fields: bool = False,
    ):
        '''
        Args:
            id_prefix (str): id prefix automatically applied to all HTML components and callbacks.
            title (str): form title (at the top of the layout)
            subtitle (html.P): form subtitle (below the title)
            continuous_inf_scheme_properties (_type_, optional): used to hide the continuous inference scheme for the main form and the training form. Defaults to {'display': 'none'}.
            mult_factor_properties (dict, optional): used to hide the MF fields. Defaults to {}.
            to_add_bottom_training_fields (bool, optional): whether to add the additional training fields (retrainings and R&D). Defaults to False.
        '''
        super().__init__(transforms = [PrefixIdTransform(prefix = id_prefix, escape = custom_prefix_escape)])
        self.additional_bottom_fields: html.Div = html.Div()
        if to_add_bottom_training_fields:
            self.additional_bottom_fields = self._get_additional_training_fields_layout()
        self.layout = self._get_layout(
            title = title,
            subtitle= subtitle,
            continuous_inf_scheme_properties=continuous_inf_scheme_properties,
            mult_factor_properties=mult_factor_properties
        )
        self._define_callbacks()
        if to_add_bottom_training_fields:
            self._define_training_fields_callbacks()

    def _get_additional_training_fields_layout(self):
        '''
        Defines the layout of the additional training form.
        '''
        return html.Div(
            [
                html.Div(
                    [
                        html.Hr(),
                    ],
                    className='Hr_div'
                ),

                #### R&D TRAININGS ####

                html.H3(
                    translatable_div_text("R&D_TRAINING_header").embed(self),
                    id='title_RandD_trainings',
                ),
                
                html.Div(
                    [
                        html.Label(translatable_div_text("R&D_training_label").embed(self)),
                        html.Div(
                            [
                                dcc.RadioItems(
                                    id='RandD_radio',
                                    options=get_yes_or_no_options(),
                                    className="radio-input",
                                ),

                                dcc.Input(
                                    min=0,
                                    type='number',
                                    id='RandD_MF_input',
                                    style=dict(display='none'),
                                ),
                            ],
                            className='radio-and-field',
                        ),

                        html.Div(
                            [
                                html.Div('i', className='tooltip-icon'),
                                html.P(
                                    translatable_div_text("R&D_training_tooltip").embed(self),
                                    className='tooltip-text'
                                ),
                            ],
                            className='tooltip',
                        ),

                    ],
                    className='form-row radio-row',
                ),

                #### RETRAININGS ####

                html.Div(
                    [
                        html.Hr(),
                    ],
                    className='Hr_div',
                ),

                html.H3(
                    translatable_div_text("RETRAINING_header").embed(self),
                    id='title_RandD_trainings',
                ),

                html.Div(
                    [
                        html.Div(
                            [
                                html.Label(translatable_div_text("retraining_label").embed(self)),

                                html.Div(
                                    [
                                        dcc.RadioItems(
                                            id='retrainings_radio',
                                            options=get_yes_or_no_options(),
                                            className="radio-input",
                                        ),
                                    ],
                                    className='radio-and-field',
                                ),

                                html.Div(
                                    [
                                        html.Div('i', className='tooltip-icon'),
                                        html.P(
                                            translatable_div_text("retraining_tooltip").embed(self),
                                            className='tooltip-text'
                                        ),
                                    ],
                                    className='tooltip',
                                ),
                            ],
                            className='form-row radio-row',
                        ),

                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Label(translatable_div_text("Number_of_runs_label").embed(self)),

                                        dcc.Input(
                                            min=0,
                                            step=1,
                                            type='number',
                                            id='retrainings_number_input',
                                        ),

                                        
                                        html.Div(
                                            [
                                                html.Div('i', className='tooltip-icon'),
                                                html.P(
                                                    translatable_div_text("Number_of_runs_tooltip").embed(self),
                                                    className='tooltip-text'
                                                ),
                                            ],
                                            className='tooltip',
                                        ),
                                    ],
                                    className='form-row short-input'
                                ),

                                html.Div(
                                    [
                                        html.Label(translatable_div_text("Running_time_label").embed(self)),

                                        dcc.Input(
                                            min=0,
                                            type='number',
                                            id='retrainings_MF_input',
                                        ),

                                        html.Div(
                                            [
                                                html.Div('i', className='tooltip-icon'),
                                                html.P(
                                                    "If retraining takes on average 10% of the "
                                                    "runtime of the main training, input '0.1'.",
                                                    className='tooltip-text'
                                                ),
                                            ],
                                            className='tooltip',
                                        ),
                                    ],
                                    className='form-row short-input'
                                ),
                            ],
                            id='retraining-additional-inputs',
                            style=dict(display='none'),
                        )
                    ],
                ),
            ]
        )

    def _get_layout(
            self,
            title: str,
            subtitle: dict[str, html.P],
            continuous_inf_scheme_properties: dict = {'display': 'none'},
            mult_factor_properties: dict = {},
        ):
            '''
            Implements the layout of the Form module
            FIXME the margins on the tooltips are a bit tight
            '''
            return html.Form(
                [
                    #### BACKEND DATA ####

                    # Obtained through intermediate processing applied to the import-content of a page
                    # Once it is updated, it is used to spread uploaded data to the corresponding form fields
                    dcc.Store(id='form_data_imported_from_csv'),

                    # The following two components are form outputs: form_aggregate_data is the collection
                    # of all fields required to replicate the whole form, form_output_metrics is the collection
                    # of raw metrics (electricity consumption, carbon emissions...) that will be forwarded
                    # to the results section
                    dcc.Store(id='form_aggregate_data'),
                    dcc.Store(id='form_output_metrics'),

                    html.Div(
                        [
                            html.P("I want to "),
                            dcc.Dropdown(
                                id="use_case_dropdown",
                                options=use_case_options,
                                className='bottom-dropdown',
                                clearable=False,
                                value=use_case_options[0],
                            ),
                        ],
                        className='use_case_dropdown_container',
                    ),

                    #### FORM HEADER ####

                    html.H3(translatable_div_text(title).embed(self)),
                    html.Div(translatable_markdown_text(subtitle).embed(self)),

                    #### CONTINUOUS INFERENCE SCHEME ####

                    html.Div(
                        [
                            html.Div(
                                [
                                    dmc.Switch(
                                        size="lg",
                                        radius="xl",
                                        label=translatable_div_text("Apply_continuous_inference_scheme").embed(self),
                                        checked=False,
                                        id='continuous_inference_scheme_switcher',
                                        className = 'continuous-switcher'
                                    ),

                                    html.Div(
                                        [
                                            html.Div('i', className='tooltip-icon'),
                                            html.P(translatable_div_text("continuous_inference_tooltip").embed(self), className='tooltip-text'),
                                        ],
                                        className='tooltip',
                                    ),
                                ],
                                className='switcher-section'
                            ),

                            html.Div(
                                [
                                    html.Label(translatable_div_text("Input_data_time_span").embed(self)),

                                    dcc.Input(
                                        type='number',
                                        id='input_data_time_scope_input',
                                        min=0.5,
                                        value=1,
                                        step=0.5,
                                    ),

                                    html.Div(
                                        [
                                            dcc.Dropdown(
                                                id='input_data_time_scope_dropdown',
                                                options=[
                                                        {'label': 'Day(s)', 'value': 'day'},
                                                        {'label': 'Week(s)', 'value': 'week'},
                                                        {'label': 'Month(s)', 'value': 'month'},
                                                        {'label': 'Year(s)', 'value': 'year'},
                                                    ],
                                                value='year',
                                                className='dropdown',
                                                clearable=False,
                                            ),
                                        ],
                                        className='box-fields'
                                    ),

                                    html.Div(
                                        [
                                            html.Div('i', className='tooltip-icon'),
                                            html.P(translatable_div_text("input_data_time_span_tooltip").embed(self), className='tooltip-text'),
                                        ],
                                        className='tooltip',
                                    ),
                                ],
                        className="input_data_time-section form-row short-input",
                        id='input_data_time_scope_section'
                    ),

                    html.Div(
                        [
                            html.Hr(),
                        ],
                        className='Hr_div'
                    ),
                ],
                style=continuous_inf_scheme_properties,
            ),

            #### RUN TIME ####

            html.Div(
                [
                    html.Label(translatable_div_text("Runtime_label").embed(self)),

                    html.Div(
                        [
                            dcc.Input(
                                type='number',
                                id='runTime_hour_input',
                                min=0,
                            ),

                            dcc.Input(
                                type='number',
                                id='runTime_min_input',
                                min=0,
                                max=59,
                            )
                        ],
                        className="box-runtime box-fields"
                    ),
                ],
                className='form-row short-input'
            ),

            html.Div(
                [
                    html.Hr(),
                ],
                className='Hr_div'
            ),

            #### TYPE OF CORES ####

            html.Div(
                [
                    html.Label(translatable_div_text("Type_of_cores_label").embed(self)),

                    html.Div(
                        [
                            dcc.Dropdown(
                                id='coreType_dropdown',
                                clearable=False,
                            ),
                        ],
                        className="box-fields"
                    ),

                    html.Div(
                        [
                            html.Div('i', className='tooltip-icon'),
                            html.P(
                                translatable_div_text("Type_of_cores_tooltip").embed(self),
                                className='tooltip-text'
                            ),
                        ],
                        className='tooltip',
                    ),
                ],
                className='form-row short-input'
            ),

            #### CPUs ####

            html.Div(
                [
                    html.H3("CPUs", id='title_CPU'),

                    html.Div(
                        [
                            html.Label(translatable_div_text("Number_of_cores_used_CPU").embed(self)),

                            dcc.Input(
                                type='number',
                                id='numberCPUs_input',
                                min=0,
                            ),

                            html.Div(
                                [
                                    html.Div('i', className='tooltip-icon'),
                                    html.P(
                                        translatable_div_text("CPU_number_used_tooltip").embed(self),
                                        className='tooltip-text'
                                    ),
                                ],
                                className='tooltip',
                            ),
                        ],
                        className='form-row short-input'
                    ),

                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Label(translatable_div_text("CPU_Model").embed(self)),

                                    html.Div(
                                        [
                                            dcc.Dropdown(
                                                id='CPUmodel_dropdown',
                                                className='bottom-dropdown',
                                                clearable=False,
                                            ),
                                        ],
                                        className="box-fields"
                                    ),

                                    html.Div(
                                        [
                                            html.Div('i', className='tooltip-icon'),
                                            html.P(translatable_div_text('cpu_model_tooltip').embed(self), className='tooltip-text'),
                                        ],
                                        className='tooltip',
                                    ),
                                    
                                ],
                                className='form-row short-input'
                            ),

                            #### CUSTOM CPU INPUTS

                            html.Div(
                                [
                                    html.P(translatable_markdown_text('custom_cpu_title').embed(self),
                                        style={'font-size': '0.9em'}
                                    ),

                                    html.Div(
                                        [
                                            html.Label(translatable_div_text('Number_of_cores').embed(self)),

                                            dcc.Input(
                                                type='number',
                                                id='CPU_model_n_cores_input',
                                                min=0,
                                            ),

                                            html.Div(
                                                [
                                                    html.Div('i', className='tooltip-icon'),
                                                    html.P(translatable_div_text("Number_of_cores_tooltip").embed(self),
                                                        className='tooltip-text'
                                                    ),
                                                ],
                                                className='tooltip',
                                            ),
                                        ],
                                        className='form-row short-input subform-input',
                                        id='CPU_model_n_cores_div',
                                    ),

                                    html.Div(
                                        [
                                            html.Label(translatable_div_text('CPU_TDP_(in_Watt)').embed(self)),

                                            dcc.Input(
                                                type='number',
                                                id='tdpCPU_input',
                                                min=0,
                                            ),

                                            html.Div(
                                                [
                                                    html.Div('i', className='tooltip-icon'),
                                                    html.P(translatable_div_text("CPU_TDP_tooltip").embed(self),  className='tooltip-text'),
                                                ],
                                                className='tooltip',
                                            ),
                                        ],
                                        className='form-row short-input subform-input',
                                        id='tdpCPU_div',
                                    ),

                                    html.Div(
                                        [
                                            html.Label(translatable_div_text('CPU_Die_area_(in_cm2)').embed(self)),

                                            dcc.Input(
                                                type='number',
                                                id='CPU_die_area_input',
                                                min=0,
                                            ),

                                            html.Div(
                                                [
                                                    html.Div('i', className='tooltip-icon'),
                                                    html.P(translatable_div_text('CPU_die_area_tooltip').embed(self), className='tooltip-text'),
                                                ],
                                                className='tooltip',
                                            ),
                                        ],
                                        className='form-row short-input subform-input',
                                        id='CPU_die_area_div',
                                    ),
                                ],
                                style=dict(display='none'),
                                id='custom_CPU_inputs_div',
                                className="subform-div",
                            )
                        ],
                        id='CPU-model-and-custom-inputs'
                    ),
                ],
                className="group-of-rows",
                id='CPU_div',
            ),

            #### GPUs ####

            html.Div(
                [
                    html.H3("GPUs", id='title_GPU'),

                    html.Div(
                        [
                            html.Label(translatable_div_text("Number_of_GPUs_used").embed(self)),

                            dcc.Input(
                                type='number',
                                id='numberGPUs_input',
                                min=0,
                            ),

                            html.Div(
                                [
                                    html.Div('i', className='tooltip-icon'),
                                    html.P(translatable_div_text("Number_of_GPUs_used_tooltip").embed(self), className='tooltip-text'),
                                ],
                                className='tooltip',
                            ),
                        ],
                        className='form-row short-input'
                    ),

                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Label(translatable_div_text("GPU_Model").embed(self)),

                                    html.Div(
                                        [
                                            dcc.Dropdown(
                                                id='GPUmodel_dropdown',
                                                className='bottom-dropdown',
                                                clearable=False,
                                            ),
                                        ],
                                        className="box-fields"
                                    ),

                                    html.Div(
                                        [
                                            html.Div('i', className='tooltip-icon'),
                                            html.P(translatable_div_text('gpu_model_tooltip').embed(self), className='tooltip-text'
                                            ),
                                        ],
                                        className='tooltip',
                                    ),
                                ],
                                className='form-row short-input'
                            ),

                            #### CUSTOM GPU INPUTS

                            html.Div(
                                [
                                    html.P(translatable_markdown_text('custom_gpu_title').embed(self), style={'font-size': '0.9em'}),

                                    html.Div(
                                        [
                                            html.Label(translatable_div_text('GPU_TDP_(in_Watt)').embed(self)),

                                            dcc.Input(
                                                type='number',
                                                id='tdpGPU_input',
                                                min=0,
                                            ),

                                            html.Div(
                                                [
                                                    html.Div('i', className='tooltip-icon'),
                                                    html.P(translatable_div_text("GPU_TDP_tooltip").embed(self) , className='tooltip-text'),
                                                ],
                                                className='tooltip',
                                            ),
                                        ],
                                        className='form-row short-input subform-input',
                                        id='tdpGPU_div',
                                    ),

                                    html.Div(
                                        [
                                            html.Label(translatable_div_text('GPU_Die_area_(in_cm2)').embed(self)),

                                            dcc.Input(
                                                type='number',
                                                id='GPU_die_area_input',
                                                min=0,
                                            ),

                                            html.Div(
                                                [
                                                    html.Div('i', className='tooltip-icon'),
                                                    html.P(translatable_div_text("GPU_die_area_tooltip").embed(self), className='tooltip-text'),
                                                ],
                                                className='tooltip',
                                            ),
                                        ],
                                        className='form-row short-input subform-input',
                                        id='GPU_die_area_div',
                                    ),

                                    html.Div(
                                        [
                                            html.Label(translatable_div_text('GPU_memory_(in_GB)').embed(self)),

                                            dcc.Input(
                                                type='number',
                                                id='GPU_memory_input',
                                                min=0,
                                            ),

                                            html.Div(
                                                [
                                                    html.Div('i', className='tooltip-icon'),
                                                    html.P(translatable_div_text("Memory_gpu_tooltip").embed(self), className='tooltip-text'),
                                                ],
                                                className='tooltip',
                                            ),
                                        ],
                                        className='form-row short-input subform-input',
                                        id='GPU_memory_div',
                                    ),
                                ],
                                style=dict(display='none'),
                                id='custom_GPU_inputs_div',
                                className="subform-div",
                            )
                        ],
                        id='GPU-model-and-custom-inputs'
                    ),
                ],
                className="group-of-rows",
                id='GPU_div',
            ),

            html.Div(
                [
                    html.Hr(),
                ],
                className='Hr_div'
            ),

            #### MEMORY ####

            html.Div(
                [
                    html.Label(translatable_div_text("Memory_available").embed(self)),

                    dcc.Input(
                        type='number',
                        id='memory_input',
                        min=0,
                    ),

                    html.Div(
                        [
                            html.Div('i', className='tooltip-icon'),
                            html.P(translatable_div_text("Memory_tooltip").embed(self), className='tooltip-text'),
                        ],
                        className='tooltip',
                    ),
                ],
                className='form-row short-input',
                id='div_memory',
            ),

            html.Div(
                [
                    html.Hr(),
                ],
                className='Hr_div'
            ),

            #### SELECT COMPUTING PLATFORM ####

            html.Div(
                [
                    html.Label(translatable_div_text("Select_the_platform_used").embed(self)),

                    html.Div(
                        [
                            dcc.Dropdown(
                                id='platformType_dropdown',
                                clearable=False,
                            ),
                        ],
                        className='box-fields',
                    ),

                    html.Div(
                        [
                            html.Div('i', className='tooltip-icon'),
                            html.P(translatable_div_text("Select_the_platform_tooltip").embed(self), className='tooltip-text'),
                        ],
                        className='tooltip',
                    ),    

                    #### SELECT PROVIDER, FOR CLOUD COMPUTING ONLY

                    html.Div(
                        [
                            dcc.Dropdown(
                                id='provider_dropdown',
                                clearable=False,
                                className='bottom-dropdown',
                            ),
                        ],
                        className="box-fields",
                        id='provider_dropdown_div',
                    ),
                ],
                className='form-row long-input'
            ),


            #### SERVER (for cloud computing) ####

            html.Div(
                [
                    html.Label(translatable_div_text("Select_server").embed(self)),

                    html.Div(
                        [
                            dcc.Dropdown(
                                id='server_continent_dropdown',
                                clearable=False,
                            ),

                            dcc.Dropdown(
                                id='server_dropdown',
                                clearable=False,
                                className='bottom-dropdown',
                            ),
                        ],
                        className="box-fields"
                    )
                ],
                id='server_div',
                className='form-row long-input',
                style={'display': 'none'}
            ),

            #### LOCATION ####

            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Label(translatable_div_text("Select_location").embed(self)),

                                    html.Div(
                                        [
                                            dcc.Dropdown(
                                                id='location_continent_dropdown',
                                                clearable=False,
                                            ),
                                        ],
                                        className="box-fields",
                                    ),

                                    html.Div(
                                        [
                                            html.Div('i', className='tooltip-icon'),
                                            html.P(
                                                translatable_div_text("Select_location_tooltip").embed(self),
                                                className='tooltip-text'
                                            ),
                                        ],
                                        className='tooltip',
                                    ),
                                ],
                                className='location-head-row'
                            ),

                            html.Div(
                                [
                                    html.P(
                                        translatable_markdown_text("Custom_carbon_intensity_header").embed(self),
                                        style={'font-size': '0.9em', 'margin-top': '20px'}
                                    ),

                                    html.Div(
                                        [
                                            html.Label(translatable_div_text('Carbon_intensity_title').embed(self)),

                                            dcc.Input(
                                                type='number',
                                                id='custom_carbon_intensity_input',
                                                min=0
                                            ),

                                            html.Div(
                                                [
                                                    html.Div('i', className='tooltip-icon'),
                                                    html.P(
                                                        translatable_div_text("Carbon_intensity_tooltip").embed(self),
                                                        className='tooltip-text'
                                                    ),
                                                ],
                                                className='tooltip',
                                            ),
                                        ],
                                        className='form-row short-input subform-input'
                                    )
                                ],
                                style=dict(display='none'),
                                id='custom_carbon_intensity_div',
                                className="subform-div",
                            ),
                        ],
                        id='location-and-custom-carbon-intensity',
                        className='location-and-custom-carbon-intensity'
                    ),

                    html.Div(
                        [
                            dcc.Dropdown(
                                id='location_country_dropdown',
                                className='bottom-dropdown',
                                clearable=False,
                            ),
                        ],
                        className="box-fields",
                        id='location_country_dropdown_div',
                    ),

                    html.Div(
                        [
                            dcc.Dropdown(
                                id='location_region_dropdown',
                                className='bottom-dropdown',
                                clearable=False,
                            ),
                        ],
                        className="box-fields",
                        id='location_region_dropdown_div',
                    ),
                    html.Div(
                        [
                            html.Span(
                                translatable_div_text("Carbon_intensity_used_label").embed(self),
                                style={'font-size': '0.85em', 'color': '#555'},
                            ),
                            html.Span(
                                id='carbon_intensity_display_value',
                                style={'font-weight': 'bold', 'margin-left': '6px', 'font-size': '0.85em'},
                            ),
                            html.Span(
                                " gCO₂eq/kWh",
                                style={'font-size': '0.85em', 'color': '#555', 'margin-left': '4px'},
                            ),
                            html.Span(" — ", style={'font-size': '0.85em', 'color': '#555', 'margin-left': '4px'}),
                            html.A(id='carbon_intensity_display_source', target='_blank', style={'font-size': '0.8em', 'color': '#888'}),
                        ],
                        id='carbon_intensity_display',
                        style={'display': 'none', 'align-items': 'center', 'margin-top': '8px', 'flex-wrap': 'wrap'},
                    ),
                ],
                id='location_div',
                className='form-row long-input',
                style={'display': 'flex'}
            ),

            #### CORE USAGE (CPU and GPU) ####

            html.Div(
                [
                    html.Label(translatable_div_text("CPU_usage_factor_label").embed(self)),
                    
                    html.Div(
                        [
                            dcc.RadioItems(
                                id='usageCPU_radio',
                                options=get_yes_or_no_options(),
                                className="radio-input",
                            ),
                            dcc.Input(
                                min=0,
                                max=1,
                                type='number',
                                id='usageCPU_input',
                                style=dict(display='none'),
                            )
                        ],
                        className='radio-and-field'
                    ),

                    html.Div(
                        [
                            html.Div('i', className='tooltip-icon'),
                            html.P(
                                translatable_div_text("CPU_usage_factor_tooltip").embed(self),
                                className='tooltip-text'
                            ),
                        ],
                        className='tooltip',
                    ),
                ],
                className='form-row radio-row',
                id='usageCPU_div',
            ),

            html.Div(
                [
                    html.Label(translatable_div_text("GPU_usage_factor_label").embed(self)),
                    html.Div(
                        [
                            dcc.RadioItems(
                                id='usageGPU_radio',
                                options=get_yes_or_no_options(),
                                className="radio-input",
                            ),

                            dcc.Input(
                                min=0,
                                max=1,
                                type='number',
                                id='usageGPU_input',
                                style=dict(display='none'),
                            ),
                        ],
                        className='radio-and-field'
                    ),

                    html.Div(
                        [
                            html.Div('i', className='tooltip-icon'),
                            html.P(
                                translatable_div_text("GPU_usage_factor_tooltip").embed(self),
                                className='tooltip-text'
                            ),
                        ],
                        className='tooltip',
                    ),                            
                ],
                className='form-row radio-row',
                id='usageGPU_div',
            ),

            #### PUE ####

            html.Div(
                [
                    html.Label(translatable_div_text("PUE_label").embed(self)),
                    html.Div(
                        [
                            dcc.RadioItems(
                                id='pue_radio',
                                options=get_yes_or_no_options(),
                                className='radio-input',
                            ),

                            dcc.Input(
                                min=1,
                                type='number',
                                id='PUE_input',
                                style=dict(display='none'),
                            ),
                        ],
                        className='radio-and-field'
                    ),

                    html.Div(
                        [
                            html.Div('i', className='tooltip-icon'),
                            html.P(
                                translatable_div_text("PUE_tooltip").embed(self),
                                className='tooltip-text'
                            ),
                        ],
                        className='tooltip',
                    ),

                ],
                className='form-row radio-row',
                id='PUEquestion_div',
                style=dict(display='none'),
            ),

            #### MULTIPLICATIVE FACTOR ####

            html.Div(
                [
                    html.Label(translatable_div_text("MF_label").embed(self)),
                    html.Div(
                        [
                            dcc.RadioItems(
                                id='mult_factor_radio',
                                options=get_yes_or_no_options(),
                                className="radio-input",
                            ),

                            dcc.Input(
                                min=1,
                                type='number',
                                id='mult_factor_input',
                                style=dict(display='none'),
                            ),
                        ],
                        className='radio-and-field',
                    ),

                    html.Div(
                        [
                            html.Div('i', className='tooltip-icon'),
                            html.P(
                                translatable_div_text("MF_tooltip").embed(self),
                                className='tooltip-text'
                            ),
                        ],
                        className='tooltip',
                    ),

                ],
                className='form-row radio-row',
                style=mult_factor_properties,
                id='mult_factor_div'
            ),

            dcc.ConfirmDialog(
                id='confirm_reset',
                message='This will reset all the values you have entered so far!\n' \
                'Are you sure you want to continue?',
            ),

            self.additional_bottom_fields,

            html.P(
                id="placeholder",
                style={"display": "none"}
            ),

        ],
        className='container input-form'
    )

    def _define_callbacks(self):
        '''
        Embeds all the internal callbacks to the blueprint
        '''
        ##################### INITIALIZATION ###

        @self.callback(
            [
                ##################################################################
                ## WARNING: do not modify the order, unless modifying the order
                ## of the DEFAULT_VALUES_FOR_PAGE_LOAD accordingly. The issue is the strong 
                # dependency between the order of the keys in the utils/handle_inputs.py/DEFAULT_VALUES_FOR_PAGE_LOAD 
                # and the order of the Outputs of this callback.
                ## TODO: make it more robust.
                Output('runTime_hour_input', 'value'),
                Output('runTime_min_input', 'value'),
                Output('coreType_dropdown', 'value'),
                Output('numberCPUs_input', 'value'),
                Output('CPU_model_n_cores_input', 'value'),
                Output('tdpCPU_input', 'value'),
                Output('CPU_die_area_input', 'value'),
                Output('numberGPUs_input', 'value'),
                Output('tdpGPU_input', 'value'),
                Output('GPU_die_area_input', "value"),
                Output('GPU_memory_input', "value"),
                Output('memory_input', 'value'),
                Output('platformType_dropdown', 'value'),
                Output('custom_carbon_intensity_input', 'value'),
                Output('usageCPU_radio', 'value'),
                Output('usageCPU_input', 'value'),
                Output('usageGPU_radio', 'value'),
                Output('usageGPU_input', 'value'),
                Output('pue_radio', 'value'),
                Output('mult_factor_radio', 'value'),
                Output('mult_factor_input', 'value'),
            ],
            [
                # To force initial triggering
                Input('url_content', 'search'),
                Input('form_data_imported_from_csv', 'data'),
            ],
        )
        def filling_form(_, upload_content: dict): 
            if ctx.triggered_id is not None and 'form_data_imported_from_csv' in ctx.triggered_id:
                to_return = {k: upload_content[k] for k in DEFAULT_VALUES_FOR_PAGE_LOAD.keys()}
                return tuple(to_return.values())
            return tuple(DEFAULT_VALUES_FOR_PAGE_LOAD.values())
        

        ##################### LOCATION AND SERVER ###

        ###########################################
        ### TODO: platform, location and server inputs sometimes do not render when uploaded from csv on AI page.
        # Particularly frequent for server.
        #  
        # The first callback range (the one directly triggered by the upload) is almost
        # always not enough to render all inputs, and most of the time it is the 
        # second callback range (the one triggered by csv flushing) that allows to complete
        # the csv inputs rendering.
        #
        # The current workaround consists in applying a higher csv_flushing_delay for the
        # AI Page, so the second callback range almost always completes the inputs rendering.
        # With a flushing delay of 2 seconds, inputs are correctly rendered after the second
        # callback range when the app is run locally.  
        #
        # My best guess is that it is due to the callback chain being
        # congested or not correctly organised by Dash because of the number of callbacks 
        # that are triggered at upload time: both location(s)
        # (continent, country, region) options and value, provider options and value,
        # server continent options and value as well as server options and value callbacks.
        # 
        # Possible fix include : 
        #   - remove default values for location and server fields 
        #       ~ (maybe not very user compliant)
        #   - refactor the callback chain by implementing step by step callback chain:
        #       ~ if the server div is not rendered, never apply callback related to server
        #       (could be done by passing 'form_data_imported_from_csv' as a State, not as an Input)  
        ###########################################
            

        @self.callback(
            Output('platformType_dropdown', 'options'),
            Input('versioned_data', 'data'),
            Input('language_dropdown', 'value'),
        )
        def set_platform(data, language):
            """
            Loads platform options based on backend data.

            WARNING: the translation of the options label fails. Translating the label raises a KeyError when calling 
            `'label': TRANSLATIONS_DICT[k][language], 'value': v} for v, k in list(data_dict.providersTypes.items())`.
            The key that is not recognized is the translation of 'Personal laptop', 'Desktop computer' or 'Local server'.
            Printing the above does not raise the error, which is strange.

            Current workaround: the translation dict contains the english words for all languages.
            """
            if data is not None:
                data_dict = SimpleNamespace(**data)
                ################## WARNING:
                # See the docstring for translation bug.
                platformType_options = [
                    {'label': TRANSLATIONS_DICT[k][language], 'value': v} for v, k in list(data_dict.providersTypes.items()) +
                                            [('personal_laptop', TRANSLATIONS_DICT['Personal laptop'][language])] +
                                            [('desktop_computer', TRANSLATIONS_DICT['Desktop computer'][language])] +
                                            [('localServer', TRANSLATIONS_DICT['Local server'][language])]
                ]
                return platformType_options
            else:
                return []

        @self.callback(
            [
                Output('location_div', 'style'),
                Output('server_div', 'style'),
            ],
            [
                Input('platformType_dropdown', 'value'),
                Input('provider_dropdown', 'value'),
                Input('server_dropdown', 'value'),
                Input('versioned_data', 'data'),
                Input('form_data_imported_from_csv', 'data'),
            ]
        )
        def display_location(selected_platform, selected_provider, selected_server, data, upload_content):
            '''
            Shows either LOCATION or SERVER depending on the platform.

            NOTE: the input Input('form_data_imported_from_csv', 'data') should not be necessary because, when a csv is uploaded,
            this callback would be triggered by the other Inputs. However, because of the issue documented in 
            the above TO DO (~ line 108), I have been thinking that adding Input('form_data_imported_from_csv', 'data') as
            an Input would help organizing the callback chain.
            '''
            if data is not None:
                data_dict = SimpleNamespace(**data)
                providers_withoutDC = data_dict.providers_withoutDC
            else:
                providers_withoutDC = []

            show = {'display': 'flex'}
            hide = {'display': 'none'}

            # The following is a kind of duplicate from the lines below,
            # should help to better take into account inputs uploaded from csv
            # TODO: should be removed when the callback chain is made simpler.
            # This simplification refers to the above TO DO as well. In simple terms
            # it would be worth trying to refactor the callback chain using intermediate bottlenecks. 
            # For instance, if the server div is not rendered, never apply callback related to server
            # (could be done by passing 'form_data_imported_from_csv' as a State, not as an Input)
            if 'form_data_imported_from_csv' in ctx.triggered_id:
                if upload_content['platformType'] == 'cloudComputing':
                    if upload_content['provider'] in ['other'] + providers_withoutDC:
                        return show, hide
                    elif selected_server == 'other':
                        return show, show
                    else:
                        return hide, show
                else:
                    return show, hide

            if selected_platform == 'cloudComputing':
                if selected_provider in ['other'] + providers_withoutDC:
                    return show, hide
                elif selected_server == 'other':
                    return show, show
                else:
                    return hide, show
            else:
                return show, hide
            
        ### Server (only for Cloud computing for now)
        
        @self.callback(
            Output('server_dropdown','style'),
            Input('server_continent_dropdown', 'value'),
        )
        def set_server_style(selected_continent):
            """
            Show or not the choice of servers, don't if continent is on "Other"
            """
            if selected_continent == 'other':
                return {'display': 'none'}

            else:
                return {'display': 'block'}
    
        @self.callback(
            Output('provider_dropdown_div', 'style'),
            Input('platformType_dropdown', 'value'),
        )
        def show_provider_field(selected_platform):
            """
            Shows or hide the "providers" box, based on the platform selected.
            """
            if selected_platform in ['cloudComputing']:
                # Only Cloud Computing need the providers box
                outputStyle = {'display': 'block'}
            else:
                outputStyle = {'display': 'none'}
            return outputStyle
        
        @self.callback(
            Output('provider_dropdown', 'options'),
            [
                Input('platformType_dropdown', 'value'),
                Input('versioned_data','data')
            ],
        )
        def set_provider_options(selected_platform, data):
            """
            List options for the "provider" box.
            """
            if data is not None:
                data_dict = SimpleNamespace(**data)

                providers_dict = data_dict.platformName_byType.get(selected_platform)
                if providers_dict is not None:
                    availableOptions = list(providers_dict.items())
                else:
                    availableOptions = []

                listOptions = [
                    {'label': v, 'value': k} for k, v in availableOptions + [("other","Other")]
                ]
                return listOptions
            else:
                return []
            
        @self.callback(
            Output('provider_dropdown','value'),
            [
                Input('platformType_dropdown', 'value'),
                Input('versioned_data','data'),
                Input('form_data_imported_from_csv', 'data'),
            ],
            [
                State('provider_dropdown', 'value'),
            ],
        )
        def set_provider_value(platform_type, versioned_data, upload_content, prev_provider):
            """
            Sets the provider value, either from the csv content of as a default value.
            """
            # reads data from input
            if ctx.triggered_id is not None:
                if 'form_data_imported_from_csv' in ctx.triggered_id:
                    return upload_content['provider']
            
                # by default, when changing the platform type, we return the previously selected
                # provider, because it properly handles the case when 'Cloud Computing' is selected 
                if 'platformType_dropdown' in ctx.triggered_id and prev_provider is not None:
                    return prev_provider
                        
            return 'gcp'

        @self.callback(
            Output('server_continent_dropdown','options'),
            [
                Input('provider_dropdown', 'value'),
                Input('versioned_data','data')
            ]
        )
        def set_server_continents_options(selected_provider, data):
            """
            List of options and default value for server's continent, based on the provider
            """
            availableOptions = availableLocations_continent(selected_provider, versioned_data=data)
            listOptions = [{'label': k, 'value': k} for k in sorted(availableOptions)] + [{'label': 'Other', 'value': 'other'}]
            return listOptions

        @self.callback(
            Output('server_dropdown','options'),
            [
                Input('provider_dropdown', 'value'),
                Input('server_continent_dropdown', 'value'),
                Input('versioned_data','data')
            ]
        )
        def set_server_options(selected_provider, selected_continent, data):
            """
            List of options for servers, based on provider and continent
            """
            availableOptions = availableOptions_servers(selected_provider,selected_continent,versioned_data=data)
            listOptions = [{'label': k['Name'], 'value': k['name_unique']} for k in availableOptions + [{'Name':"other", 'name_unique':'other'}]]
            return listOptions  
        
        @self.callback(
            Output('server_continent_dropdown','value'),
            [
                Input('provider_dropdown', 'value'),
                Input('versioned_data','data'),
                Input('form_data_imported_from_csv', 'data'),
            ],
            [
                State('server_continent_dropdown', 'value'),
            ]
        )
        def set_serverContinents_value(selected_provider, versioned_data, upload_content, prev_server_continent):
            '''
            Sets the value for server's continent, depending on the provider.
            We want to fetch the value based on csv input but also to display 
            a value selcted previously by the user.
            '''
            # reads data from input
            if ctx.triggered_id is not None and 'form_data_imported_from_csv' in ctx.triggered_id:
                return upload_content['serverContinent']

            # otherwise we return a suitable default value
            availableOptions = availableLocations_continent(selected_provider, versioned_data=versioned_data)
            if prev_server_continent in availableOptions:
                defaultValue = prev_server_continent
            else:
                try: 
                    defaultValue = availableOptions[0]
                except:
                    defaultValue = None
            return defaultValue
        
        @self.callback(
            Output('server_dropdown','value'),
            [
                Input('server_continent_dropdown', 'value'),
                Input('versioned_data','data'),
                Input('form_data_imported_from_csv', 'data'),
            ],
            [
                State('provider_dropdown', 'value'),
                State('server_dropdown','value'),
            ]
        )
        def set_server_value(selected_continent, versioned_data, upload_content, selected_provider, prev_server_value):
            """
            Sets the value for servers, based on provider and continent.
            Here again we want to display a default value, to
            fetch the value from a csv or to show a value previously selected by the user.
            """
            # reads data from input
            if ctx.triggered_id is not None and 'form_data_imported_from_csv' in ctx.triggered_id:
                return upload_content['server']
            
            # handles special case
            if selected_continent == 'other':
                return 'other'

            # Otherwise we return a suitable default value
            availableOptions = availableOptions_servers(selected_provider, selected_continent, versioned_data=versioned_data)
            try:
                # when the server continent value had previously been set by the user
                if prev_server_value in [server['name_unique'] for server in availableOptions]:
                    defaultValue = prev_server_value
                else :
                    defaultValue = availableOptions[0]['name_unique']
            except:
                defaultValue = None
            return defaultValue

        ## Location (only for local server, personal device or "other" cloud server)

        @self.callback(
            Output('location_continent_dropdown', 'options'),
            Input('versioned_data','data')
        )
        def set_continentOptions(versioned_data):
            if versioned_data is not None:
                data_dict = SimpleNamespace(**versioned_data)
                continentsList = list(data_dict.CI_dict_byName.keys())
                continentsDict = [{'label': 'Use a custom carbon intensity', 'value': 'custom'}] + [{'label': k, 'value': k} for k in sorted(continentsList)]
                return continentsDict
            else:
                return []
            
        @self.callback(
            Output('location_continent_dropdown', 'value'),
            [
                Input('server_div', 'style'),
                Input('form_data_imported_from_csv', 'data'),
            ],
            [
                State('server_continent_dropdown','value'),
                State('location_continent_dropdown', 'value'),
            ]
        )
        def set_continent_value(display_server, upload_content, selected_serverContinent, prev_locationContinent):
            """
            Sets the value for location continent.
            Same as for server and server continent regarding the different inputs.
            """
            # reads data from input
            if ctx.triggered_id is not None and 'form_data_imported_from_csv' in ctx.triggered_id:
                return upload_content['locationContinent']
            
            # when the continent value had previously been set by the user
            if prev_locationContinent is not None :
                return prev_locationContinent
            
            # the server div is shown, so we pull the continent from there
            if (display_server['display'] != 'none') & (selected_serverContinent != 'other'):
                return selected_serverContinent
            
            return 'Europe'

        @self.callback(
            [
                Output('custom_carbon_intensity_div', 'style'),
                Output('location-and-custom-carbon-intensity', 'style'),
            ],
            Input(f'location_continent_dropdown', 'value'),
        )
        def display_custom_carbon_intensity(selected_continent):
            '''
            Shows the custom carbon intensity box and adapts border attributes.
            '''
            if selected_continent == 'custom':
                return {'display': 'flex'}, custom_core_box_style
            else:
                return {'display': 'none'}, {'border': 'none'}
        
        @self.callback(
            [
                Output(f'location_country_dropdown', 'options'),
                Output(f'location_country_dropdown', 'value'),
                Output(f'location_country_dropdown_div', 'style'),
            ],
            [
                Input(f'location_continent_dropdown', 'value'),
                Input('versioned_data','data'),
                Input('form_data_imported_from_csv', 'data'),
            ],
            [
                State(f'location_country_dropdown', 'value')
            ]
        )
        def set_countries_options(selected_continent, versioned_data, upload_content, prev_selectedCountry):
            """
            List of options and value for countries.
            Hides country dropdown if continent=World or if a custom carbon intensity is selected.
            Must fetch the value from a csv as well.
            """
            availableOptions = availableOptions_country(selected_continent, versioned_data=versioned_data)
            listOptions = [{'label': k, 'value': k} for k in availableOptions]
            defaultValue = None

            # reads data from input
            if ctx.triggered_id is not None and 'form_data_imported_from_csv' in ctx.triggered_id:
                defaultValue = upload_content['locationCountry']

            # otherwise we get a suitable default value    
            if defaultValue is None:
                # NOTE The following handles two cases: 
                if prev_selectedCountry in availableOptions :
                    defaultValue = prev_selectedCountry
                else:
                    try:
                        defaultValue = availableOptions[0]
                    except:
                        defaultValue = None

            if (selected_continent == 'World') or (selected_continent == 'custom'):
                country_style = {'display': 'none'}
            else:
                country_style = {'display': 'block'}

            return listOptions, defaultValue, country_style
        
        @self.callback(
            [
                Output(f'location_region_dropdown', 'options'),
                Output(f'location_region_dropdown', 'value'),
                Output(f'location_region_dropdown_div', 'style'),
            ],
            [
                Input(f'location_continent_dropdown', 'value'),
                Input(f'location_country_dropdown', 'value'),
                Input('versioned_data','data'),
                Input('form_data_imported_from_csv', 'data'),
            ],
            [
                State(f'location_region_dropdown', 'value'),
            ]

        )
        def set_regions_options(selected_continent, selected_country, versioned_data, upload_content, prev_selectedRegion):
            """
            List of options and value for regions.
            Hides region dropdown if only one possible region or
            if continent=World or custom carbon intensity are selected
            """
            locs = availableOptions_region(selected_continent, selected_country, data=versioned_data)
            if versioned_data is not None:
                listOptions = [{'label': versioned_data['CI_dict_byLoc'][loc]['regionName'], 'value': loc} for loc in locs]
            else:
                listOptions = []
            defaultValue = None

            # reads data from input
            if ctx.triggered_id is not None and 'form_data_imported_from_csv' in ctx.triggered_id:
                defaultValue = upload_content['locationRegion']

            # otherwise we get a suitable default value  
            if defaultValue is None:
                # when the region value had previously been set by the user
                if prev_selectedRegion in locs:
                    defaultValue = prev_selectedRegion
                else:
                    try:
                            defaultValue = locs[0]
                    except:
                        defaultValue = None

            if (selected_continent == 'World') or (len(listOptions) == 1) or (selected_continent == 'custom'):
                region_style = {'display': 'none'}
            else:
                region_style = {'display': 'block'}

            return listOptions, defaultValue, region_style
            

        ##################### COMPUTING CORES ###

        @self.callback(
            Output('coreType_dropdown', 'options'),
            [
                Input('provider_dropdown', 'value'),
                Input('platformType_dropdown', 'value'),
                Input('versioned_data','data')
            ]
        )
        def set_coreType_options(_, __, data):
            '''
            List of options for coreType (CPU or GPU), based on the platform/provider selected.
            Not really useful so far because we have no specific core types for a given provider.
            '''
            if data is not None:
                data_dict = SimpleNamespace(**data)

                availableOptions = data_dict.cores_dict.keys()
                listOptions = [{'label': k, 'value': k} for k in list(sorted(availableOptions)) + ['CPU + GPU']]

                return listOptions
            else:
                return []
            
        @self.callback(
            [
                Output('CPUmodel_dropdown', 'options'),
                Output('GPUmodel_dropdown', 'options')
            ],
            [Input('versioned_data','data')]
        )
        def set_coreOptions(data):
            """
            List of options for core models.
            """
            if data is not None:
                data_dict = SimpleNamespace(**data)

                coreModels_options = dict()
                for coreType in ['CPU', 'GPU']:
                    availableOptions = sorted(list(data_dict.cores_dict[coreType].keys()))
                    availableOptions = put_value_first(availableOptions, 'Average')
                    coreModels_options[coreType] = [
                        {'label': k, 'value': v} for k, v in [(f"I can't find my {coreType}", "other")] + 
                        list(zip(availableOptions, availableOptions))
                    ]

                return coreModels_options['CPU'], coreModels_options['GPU']

            else:
                return [],[]
            
        @self.callback(
            [
                Output('CPUmodel_dropdown', 'value'),
            ],
            [
                Input('form_data_imported_from_csv', 'data'),
                Input('CPUmodel_dropdown', 'options'),
            ],
        )
        def set_CPU_model_value(upload_content: dict, cpu_options: list[dict]):
            """
            When a csv is loaded with a proper cpu model, it is filled in the form.
            Otherwise we select the first available model in the current data version.
            """
            if ctx.triggered_id is not None and 'form_data_imported_from_csv' in ctx.triggered_id:
                if 'CPUmodel' in upload_content.keys():
                    return upload_content['CPUmodel']
            # The fist two items of the cpu options are the Average and Custom (I can't find my cpu)
            # so we select the next one
            return cpu_options[2]['label']
        
        @self.callback(
            [
                Output('GPUmodel_dropdown', 'value'),
            ],
            [
                Input('form_data_imported_from_csv', 'data'),
                Input('GPUmodel_dropdown', 'options'),
            ],
        )
        def set_GPU_model_value(upload_content: dict, gpu_options: list[dict]):
            """
            When a csv is loaded with a proper gpu model, it is filled in the form.
            Otherwise we select the first available model in the current data version.
            """
            if ctx.triggered_id is not None and 'form_data_imported_from_csv' in ctx.triggered_id:
                if 'GPUmodel' in upload_content.keys():
                    return upload_content['GPUmodel']
            # The fist two items of the gpu options are the Average and Custom (I can't find my gpu)
            # so we select the next one
            return gpu_options[2]['label']
            
            
        @self.callback(
            [
                Output('CPU_div', 'style'),
                Output('title_CPU', 'style'),
                Output('usageCPU_div', 'style'),
                Output('GPU_div', 'style'),
                Output('title_GPU', 'style'),
                Output('usageGPU_div', 'style'),
            ],
            [
                Input('coreType_dropdown', 'value')
            ]
        )
        def show_CPUGPUdiv(selected_coreType):
            """
            Shows or hides the CPU/GPU input blocks (and the titles) based on the selected core type.
            """
            show = {'display': 'block'}
            showFlex = {'display': 'flex'}
            hide = {'display': 'none'}
            if selected_coreType == 'CPU':
                return show, hide, showFlex, hide, hide, hide
            elif selected_coreType == 'GPU':
                return hide, hide, hide, show, hide, showFlex
            else:
                return show, show, showFlex, show, show, showFlex
            
        @self.callback(
            [       
                Output('custom_CPU_inputs_div', 'style'),
                Output('CPU-model-and-custom-inputs', 'style'),
            ],
            [
                Input('CPUmodel_dropdown', 'value'),
            ]
        )
        def display_custom_cpu_inputs(selected_coreModel):
            '''
            Shows or hides the boxes for custom CPU specs and adapts border attributes.
            '''
            if selected_coreModel == "other":
                return {'display': 'flex'}, custom_core_box_style
            else:
                return {'display': 'none'}, {'border': 'none'}
            
        @self.callback(
            [
                Output('custom_GPU_inputs_div', 'style'),
                Output('GPU-model-and-custom-inputs', 'style'),
            ],
            [
                Input('GPUmodel_dropdown', 'value'),
            ]
        )
        def display_custom_GPU_inputs(selected_coreModel):
            """
            Shows or hides the boxes for custom GPU specs and adapts the border attributes.
            """
            if selected_coreModel == "other":
                return {'display': 'flex'}, custom_core_box_style
            else:
                return {'display': 'none'}, {'border': 'none'}
            
        ##################### USAGE FACTORS ###

        @self.callback(
            Output('usageCPU_input','style'),
            [
                Input('usageCPU_radio', 'value'),
                Input('usageCPU_input', 'disabled')
            ]
        )
        def display_usage_input(answer_usage, disabled):
            """
            Show or hide the usage factor input box, based on Yes/No input
            """
            if answer_usage == 'No':
                out = {'display': 'none'}
            else:
                out = {'display': 'block'}

            if disabled:
                out['background-color'] = MY_COLORS['boxesColor']

            return out

        @self.callback(
            Output('usageGPU_input','style'),
            [
                Input('usageGPU_radio', 'value'),
                Input('usageGPU_input', 'disabled')
            ]
        )
        def display_usage_input(answer_usage, disabled):
            """
            Show or hide the usage factor input box, based on Yes/No input
            """
            if answer_usage == 'No':
                out = {'display': 'none'}
            else:
                out = {'display': 'block'}

            if disabled:
                out['background-color'] = MY_COLORS['boxesColor']

            return out
            
        ##################### PUE INPUTS ###

        @self.callback(
            Output('PUEquestion_div','style'),
            [
                Input('location_region_dropdown','value'),
                Input('platformType_dropdown', 'value'),
                Input('provider_dropdown', 'value'),
                Input('server_dropdown', 'value')
            ]
        )
        def display_pue_question(_, selected_platform, selected_provider, selected_server):
            """
            Shows or hides the PUE question depending on the platform
            """
            if selected_platform == 'localServer':
                return {'display': 'flex'}
            elif (selected_platform == 'cloudComputing')&((selected_provider == 'other')|(selected_server == 'other')):
                return {'display': 'flex'}
            else:
                return {'display': 'none'}

        @self.callback(
            Output('PUE_input','style'),
            [
                Input('pue_radio', 'value'),
                Input('PUE_input','disabled')
            ]
        )
        def display_pue_input(answer_pue, disabled):
            """
            Shows or hides the PUE input box
            """
            if answer_pue == 'No':
                out = {'display': 'none'}
            else:
                out = {'display': 'block'}

            if disabled:
                out['background-color'] = MY_COLORS['boxesColor']

            return out
        
        @self.callback(
            Output(f'PUE_input','value'),
            [
                Input(f'pue_radio', 'value'),
                Input('versioned_data','data'),
                Input('form_data_imported_from_csv', 'data'),
            ],
            [
                State(f'PUE_input','value'),
            ]
        )
        def set_PUE(radio, versioned_data, upload_content, prev_pue):
            """
            Sets the PUE value, either from csv input or as a default value.
            """
            if versioned_data is not None:
                data_dict = SimpleNamespace(**versioned_data)
                defaultPUE = data_dict.pueDefault_dict['Unknown']
            else:
                defaultPUE = 0

            if radio == 'No':
                return defaultPUE
            
            # reads data from input
            if ctx.triggered_id is not None and 'form_data_imported_from_csv' in ctx.triggered_id:
                return upload_content['PUE']

            return defaultPUE

        ##################### MULTIPLICATIVE FACTOR INPUTS ###

        @self.callback(
            Output('mult_factor_input','style'),
            [
                Input('mult_factor_radio', 'value'),
                Input('mult_factor_input', 'disabled')
            ]
        )
        def display_mult_factor_input(answer_mult_factor, disabled):
            """
            Shows or hides the MULTIPLICATIVE FACTOR input box
            """
            if answer_mult_factor == 'No':
                out = {'display': 'none'}
            else:
                out = {'display': 'block'}

            if disabled:
                out['background-color'] = MY_COLORS['boxesColor']

            return out

        ##################### PROCESS INPUTS ###
        
        @self.callback(
            [
                Output('form_aggregate_data', "data"),
                Output('form_output_metrics', "data"),
            ],
            [
                Input('versioned_data','data'),
                Input('coreType_dropdown', "value"),
                Input('numberCPUs_input', "value"),
                Input('CPUmodel_dropdown', "value"),
                Input('custom_CPU_inputs_div', "style"),
                Input('CPU_model_n_cores_input', "value"),
                Input('tdpCPU_input', "value"),
                Input('CPU_die_area_input', "value"),
                Input('numberGPUs_input', "value"),
                Input('GPUmodel_dropdown', "value"),
                Input('custom_GPU_inputs_div', "style"),
                Input('tdpGPU_input', "value"),
                Input('GPU_die_area_input', "value"),
                Input('GPU_memory_input', "value"),
                Input('memory_input', "value"),
                Input('runTime_hour_input', "value"),
                Input('runTime_min_input', "value"),
                Input('location_continent_dropdown', "value"),
                Input('location_country_dropdown', "value"),
                Input('location_region_dropdown', "value"),
                Input('custom_carbon_intensity_div', 'style'),
                Input('custom_carbon_intensity_input', 'value'),
                Input('server_continent_dropdown', "value"),
                Input('server_dropdown', "value"),
                Input('location_div', 'style'),
                Input('server_div','style'),
                Input('usageCPU_radio', "value"),
                Input('usageCPU_input', "value"),
                Input('usageGPU_radio', "value"),
                Input('usageGPU_input', "value"),
                Input('PUEquestion_div','style'),
                Input('pue_radio', "value"),
                Input('PUE_input', "value"),
                Input('mult_factor_radio', "value"),
                Input('mult_factor_input', "value"),
                Input('platformType_dropdown', 'value'),
                Input('provider_dropdown', 'value'),
                Input('provider_dropdown_div', 'style'),
            ],
        )
        def aggregate_input_values(data, coreType, n_CPUcores, CPUmodel, custom_CPu_inputs_style, CPU_model_n_cores_input, tdpCPU,
                                CPU_die_area_input, n_GPUs, GPUmodel, custom_GPu_inputs_style, tdpGPU, GPU_die_area_input, GPU_memory_input,
                                memory, runTime_hours, runTime_min, locationContinent, locationCountry, locationRegion, custom_carbon_intensity_style, custom_carbon_intensity_input,
                                serverContinent, server, locationStyle, serverStyle, usageCPUradio, usageCPU, usageGPUradio, usageGPU,
                                PUEdivStyle, PUEradio, PUE, mult_factor_radio, mult_factor, selected_platform, selected_provider, providerStyle):
            """
            Computes all the metrics and gathers the information provided by the inputs of the form.
            """
            output = {}
            metrics = {}

            #############################################
            ### PREPROCESS: check if computations can be performed

            notReady = False

            ### Runtime
            test_runTime = 0
            if runTime_hours is None:
                actual_runTime_hours = 0
                test_runTime += 1
            else:
                actual_runTime_hours = runTime_hours

            if runTime_min is None:
                actual_runTime_min = 0
                test_runTime += 1
            else:
                actual_runTime_min = runTime_min
            runTime = actual_runTime_hours + actual_runTime_min/60.

            ### Core type
            if coreType is None:
                notReady = True
            elif (coreType in ['CPU','CPU + GPU'])&((n_CPUcores is None)|(CPUmodel is None)):
                notReady = True
            elif (coreType in ['GPU','CPU + GPU'])&((n_GPUs is None)|(GPUmodel is None)):
                notReady = True

            ### Versioned data
            if data is not None:
                data_dict = SimpleNamespace(**data)
                version = data_dict.version
            else:
                version = None
                notReady = True

            ### Location
            # The locationVar is the most fine-grained data on location available through the form.
            if is_shown(locationStyle):
                # this means the "location" input is shown, so we use location instead of server
                locationVar = locationRegion
                if is_shown(custom_carbon_intensity_style):
                    locationVar ='custom'
            elif (server is None) | (server == 'other') | (data is None):
                locationVar = None
            else:
                locationVar = data_dict.datacenters_dict_byName[server]['location']

            ### Platform
            if selected_platform is None:
                notReady = True
            elif (selected_platform == 'cloudComputing')&(selected_provider is None):
                notReady = True

            ### Other required inputs
            if (memory is None) | (tdpCPU is None) | (tdpGPU is None) | (locationVar is None) | \
                    (usageCPU is None) | (usageGPU is None) | (PUE is None) | (mult_factor is None):
                notReady = True

            ### If any of the required inputs is note ready: do not compute
            if notReady:
                output['coreType'] = None
                output['CPUmodel'] = None
                output['numberCPUs'] = None
                output['usageCPU'] = None
                output['usageCPUradio'] = None
                output['CPU_model_n_cores'] = None
                output['tdpCPU'] = None
                output['CPU_die_area'] = None
                output['GPUmodel'] = None
                output['numberGPUs'] = None
                output['tdpGPU'] = None
                output['GPU_die_area'] = None
                output['GPU_memory'] = None
                output['usageGPU'] = None
                output['usageGPUradio'] = None
                output['GPUpower'] = None
                output['memory'] = None
                output['runTime_hour'] = None
                output['runTime_min'] = None
                output['platformType'] = None
                output['location'] = None
                output['carbonIntensity'] = None
                output['PUE'] = None
                output['PUEradio'] = None
                output['mult_factor'] = None
                output['mult_factor_radio'] = None
                output['appVersion'] = version
                metrics['energy_needed'] = 0
                metrics['carbonEmissions'] = 0
                metrics['manufacturing_carbonEmissions'] = 0
                metrics['manufacturing_abiotic_resources'] = 0
                metrics['runTime'] = None
                metrics['power_needed'] = 0
                metrics['CE_CPU'] = 0
                metrics['CE_GPU'] = 0
                metrics['CE_core'] = 0
                metrics['CE_memory'] = 0
                metrics['manufacturing_CE_CPU'] = 0
                metrics['manufacturing_CE_GPU'] = 0
                metrics['manufacturing_CE_memory'] = 0
                metrics['manufacturing_CE_other'] = 0
                metrics['manufacturing_ADP_CPU'] = 0
                metrics['manufacturing_ADP_GPU'] = 0
                metrics['manufacturing_ADP_memory'] = 0
                metrics['manufacturing_ADP_other'] = 0

            #############################################
            ### PRE-COMPUTATIONS: update variables used in the calcul based on inputs

            else:
                ### PUE
                defaultPUE = data_dict.pueDefault_dict['Unknown']

                ### PUE and HARDWARE LIFESPAN
                if selected_platform in ['desktop_computer', 'personal_laptop']:
                    PUE_used = 1
                    if selected_platform == 'desktop_computer':
                        hardware_lifespan = data_dict.hardware_impacts_dict['active_lifespan_desktop_computer']
                    else:
                        hardware_lifespan = data_dict.hardware_impacts_dict['active_lifespan_laptop']
                elif selected_platform == 'localServer':
                    PUE_used = defaultPUE
                    hardware_lifespan = data_dict.hardware_impacts_dict['active_lifespan_local_server']
                else:
                    # Cloud
                    hardware_lifespan = data_dict.hardware_impacts_dict['active_lifespan_cloud_server']
                    if selected_provider == 'other':
                        PUE_used = defaultPUE
                    else:
                        # if we don't know the PUE of this specific data centre, or if we 
                        # don't know the data centre, we use the provider's default
                        server_data = data_dict.datacenters_dict_byName.get(server)
                        if server_data is not None:
                            if pd.isnull(server_data['PUE']):
                                PUE_used = data_dict.pueDefault_dict[selected_provider]
                            else:
                                PUE_used = server_data['PUE']
                        else:
                            PUE_used = data_dict.pueDefault_dict[selected_provider]
                            
                # the input PUE is used only if the PUE box is shown AND the radio button is "Yes"
                if (is_shown(PUEdivStyle)) & (PUEradio == 'Yes'):
                    PUE_used = PUE
                
                ### CPUs: DYNAMIC AND MANUFACTURING IMPACTS
                if coreType in ['CPU', 'CPU + GPU']:
                    # Retrieving the CPU data
                    if is_shown(custom_CPu_inputs_style):
                        # We asked the question about TDP, so the dafault CPU is selected
                        CPU_model_n_cores = CPU_model_n_cores_input
                        CPUpower = tdpCPU # in Watt
                        CPU_die_area = CPU_die_area_input # in cm2
                    else:
                        # CPUmodel cannot be "other", so we retrieve the data of the selected CPU
                        CPU_model_n_cores = data_dict.cores_dict['CPU'][CPUmodel]['n_cores']
                        CPUpower = data_dict.cores_dict['CPU'][CPUmodel]['TDP']
                        CPU_die_area = data_dict.cores_dict['CPU'][CPUmodel]['die_area']
                    # Per core computations
                    CPUpower_per_core = CPUpower / CPU_model_n_cores
                    CPU_die_area_per_core = CPU_die_area / CPU_model_n_cores
                    fixed_CPU_manufacturing_GWP_per_core = data_dict.hardware_impacts_dict['cpu_base_impact_gwp'] / CPU_model_n_cores
                    fixed_CPU_manufacturing_ADP_per_core = data_dict.hardware_impacts_dict['cpu_base_impact_adp'] / CPU_model_n_cores
                    # Usage ration data
                    if usageCPUradio == 'Yes':
                        usageCPU_used = usageCPU
                    else:
                        usageCPU_used = 1.
                    # CPU impact values
                    dynamic_powerNeeded_CPU = PUE_used * n_CPUcores * CPUpower_per_core * usageCPU_used # in Watt
                    manufacturing_GWP_CPU_raw = n_CPUcores * (CPU_die_area_per_core * data_dict.hardware_impacts_dict['cpu_die_impact_gwp'] + fixed_CPU_manufacturing_GWP_per_core)
                    manufacturing_per_hour_GWP_CPU = manufacturing_GWP_CPU_raw / hardware_lifespan ## in gCO2e/hour
                    manufacturing_ADP_CPU_raw = n_CPUcores * (CPU_die_area_per_core * data_dict.hardware_impacts_dict['cpu_die_impact_adp'] + fixed_CPU_manufacturing_ADP_per_core)
                    manufacturing_per_hour_ADP_CPU = manufacturing_ADP_CPU_raw / hardware_lifespan ## in kgSbe/hour
                else:
                    dynamic_powerNeeded_CPU = 0
                    usageCPU_used = 0
                    CPU_model_n_cores = 0
                    CPUpower = 0
                    CPU_die_area = 0
                    manufacturing_per_hour_GWP_CPU = 0
                    manufacturing_per_hour_ADP_CPU = 0

                ### GPUs: DYNAMIC AND MANUFACTURING IMPACTS
                if coreType in ['GPU', 'CPU + GPU']:
                    # Dealing with TDP and die area
                    if is_shown(custom_GPu_inputs_style):
                        # We asked the question about TDP, so the dafault GPU is selected
                        GPUpower = tdpGPU # in Watt
                        GPU_die_area =GPU_die_area_input
                        GPU_memory = GPU_memory_input
                    else:
                        # GPUmodel cannot be "other"
                        GPUpower = data_dict.cores_dict['GPU'][GPUmodel]['TDP']
                        GPU_die_area = data_dict.cores_dict['GPU'][GPUmodel]['die_area']
                        GPU_memory = data_dict.cores_dict['GPU'][GPUmodel]['memory']
                    # Dealing with usage ratio
                    if usageGPUradio == 'Yes':
                        usageGPU_used = usageGPU
                    else:
                        usageGPU_used = 1.
                    # Computation
                    dynamic_powerNeeded_GPU = PUE_used * n_GPUs * GPUpower * usageGPU_used # in Watt
                    # GWP
                    manufacturing_GWP_GPU_no_mem = GPU_die_area * data_dict.hardware_impacts_dict['gpu_die_impact_gwp'] + data_dict.hardware_impacts_dict['gpu_base_impact_gwp']
                    manufacturing_GWP_GPU_mem = data_dict.hardware_impacts_dict['ram_die_impact_gwp']* GPU_memory / data_dict.hardware_impacts_dict['ram_density']
                    manufacturing_per_hour_GWP_GPU = n_GPUs * (manufacturing_GWP_GPU_no_mem + manufacturing_GWP_GPU_mem) / hardware_lifespan ## in gCO2e/hour
                    # ADP
                    manufacturing_ADP_GPU_no_mem = GPU_die_area * data_dict.hardware_impacts_dict['gpu_die_impact_adp'] + data_dict.hardware_impacts_dict['gpu_base_impact_adp']
                    manufacturing_ADP_GPU_mem = data_dict.hardware_impacts_dict['ram_die_impact_adp']* GPU_memory / data_dict.hardware_impacts_dict['ram_density']
                    manufacturing_per_hour_ADP_GPU = n_GPUs * (manufacturing_ADP_GPU_no_mem + manufacturing_ADP_GPU_mem) / hardware_lifespan ## in kgSbe/hour
                else:
                    GPUpower = 0
                    GPU_die_area = 0
                    GPU_memory = 0
                    usageGPU_used = 0
                    dynamic_powerNeeded_GPU = 0
                    manufacturing_per_hour_GWP_GPU = 0
                    manufacturing_per_hour_ADP_GPU = 0

                ### MEMORY: MANUFACTURING IMPACTS
                memory_strip_area = data_dict.hardware_impacts_dict['ram_default_strip_size'] / data_dict.hardware_impacts_dict['ram_density']
                # GWP
                manufacturing_GWP_memory_per_strip = memory_strip_area * data_dict.hardware_impacts_dict['ram_die_impact_gwp'] + data_dict.hardware_impacts_dict['ram_base_impact_gwp']
                manufacturing_GWP_memory_raw = manufacturing_GWP_memory_per_strip * memory / data_dict.hardware_impacts_dict['ram_default_strip_size']
                manufacturing_per_hour_GWP_memory = manufacturing_GWP_memory_raw / hardware_lifespan ## in gCO2e/hour
                # ADP
                manufacturing_ADP_memory_per_strip = memory_strip_area * data_dict.hardware_impacts_dict['ram_die_impact_adp'] + data_dict.hardware_impacts_dict['ram_base_impact_adp']
                manufacturing_ADP_memory_raw = manufacturing_ADP_memory_per_strip * memory / data_dict.hardware_impacts_dict['ram_default_strip_size']
                manufacturing_per_hour_ADP_memory = manufacturing_ADP_memory_raw / hardware_lifespan ## in kgSbe/hour

                ### OTHER DEVICES (casing, motherboard...) MANUFACTURING IMPACTS
                # If a personal computer is used, we consider that its other resources are fully dedicated to the 
                # computation during it. Otherwise, we apply a multiplier based on the ratio of the number of cores
                # used over the number of cores contained in a server.

                # TODO: maybe prompt the user when several GPUs are used along with a 'desktop_computer' which is quite unlikely.
                if selected_platform == 'desktop_computer':
                    # GWP
                    manufacturing_GWP_other_raw = data_dict.hardware_impacts_dict['desktop_computer_base_impact_gwp']
                    # ADP
                    manufacturing_ADP_other_raw = data_dict.hardware_impacts_dict['desktop_computer_base_impact_adp']
                elif selected_platform == 'personal_laptop':
                    # GWP
                    manufacturing_GWP_other_raw = data_dict.hardware_impacts_dict['laptop_base_impact_gwp']
                    # ADP
                    manufacturing_ADP_other_raw = data_dict.hardware_impacts_dict['laptop_base_impact_adp']
                else:
                    # We need the number of cores used to deduce the number of servers used
                    # so we distinguish between cases where only GPUs are used and cases where both core types
                    # are used. We also adapt to the kind of servers used.
                    if coreType == 'GPU':
                        if selected_platform == 'cloudComputing':
                            n_gpus_per_server = data_dict.hardware_impacts_dict['nb_GPU_cloud_per_server']
                        else:
                            n_gpus_per_server = data_dict.hardware_impacts_dict['nb_GPU_local_per_server']
                        n_servers = n_GPUs / n_gpus_per_server
                    else:
                        n_servers = n_CPUcores / (CPU_model_n_cores * data_dict.hardware_impacts_dict['nb_CPU_per_server'])
                    # GWP
                    manufacturing_GWP_other_raw = data_dict.hardware_impacts_dict['motherboard_impact_gwp'] + data_dict.hardware_impacts_dict['assembly_impact_gwp'] + data_dict.hardware_impacts_dict['rack_casing_impact_gwp'] + data_dict.hardware_impacts_dict['PSU_impact_gwp']
                    manufacturing_GWP_other_raw = manufacturing_GWP_other_raw * n_servers
                    # ADP
                    manufacturing_ADP_other_raw = data_dict.hardware_impacts_dict['motherboard_impact_adp'] + data_dict.hardware_impacts_dict['assembly_impact_adp'] + data_dict.hardware_impacts_dict['rack_casing_impact_adp'] + data_dict.hardware_impacts_dict['PSU_impact_adp']
                    manufacturing_ADP_other_raw = manufacturing_ADP_other_raw * n_servers
                # Compute per-hour values
                manufacturing_per_hour_GWP_other = manufacturing_GWP_other_raw / hardware_lifespan ## in gCO2e/hour
                manufacturing_per_hour_ADP_other = manufacturing_ADP_other_raw / hardware_lifespan ## in kgSbe/hour

                ### SERVER/LOCATION
                if is_shown(custom_carbon_intensity_style):
                    carbonIntensity = custom_carbon_intensity_input
                else:
                    carbonIntensity = data_dict.CI_dict_byLoc[locationVar]['carbonIntensity']

                ### MULTIPLICATIVE FACTOR
                if mult_factor_radio == 'Yes':
                    mult_factor_used = mult_factor
                else:
                    mult_factor_used = 1

                #############################################
                ### COMPUTATIONS: final outputs are computed

                # Manufacturing carbon emissions, in gCO2e
                manufacturing_GWP_CPU = runTime * manufacturing_per_hour_GWP_CPU * mult_factor_used
                manufacturing_GWP_GPU = runTime * manufacturing_per_hour_GWP_GPU * mult_factor_used
                manufacturing_GWP_memory = runTime * manufacturing_per_hour_GWP_memory * mult_factor_used
                manufacturing_GWP_other = runTime * manufacturing_per_hour_GWP_other * mult_factor_used
                manufacturing_GWP = manufacturing_GWP_CPU + manufacturing_GWP_GPU + manufacturing_GWP_memory + manufacturing_GWP_other

                # Manufacturing abiotic resources depletion, in kgSb e
                manufacturing_ADP_CPU = runTime * manufacturing_per_hour_ADP_CPU * mult_factor_used
                manufacturing_ADP_GPU = runTime * manufacturing_per_hour_ADP_GPU * mult_factor_used
                manufacturing_ADP_memory = runTime * manufacturing_per_hour_ADP_memory * mult_factor_used
                manufacturing_ADP_other = runTime * manufacturing_per_hour_ADP_other * mult_factor_used
                manufacturing_ADP = manufacturing_ADP_CPU + manufacturing_ADP_GPU + manufacturing_ADP_memory + manufacturing_ADP_other
                
                # Power needed, in Watt
                powerNeeded_core = dynamic_powerNeeded_CPU + dynamic_powerNeeded_GPU
                powerNeeded_memory = PUE_used * (memory * data_dict.hardware_impacts_dict['memoryPower'])
                powerNeeded = powerNeeded_core + powerNeeded_memory

                # Energy needed, in kWh (so dividing by 1000 to convert from Wh)
                energyNeeded_CPU = runTime * dynamic_powerNeeded_CPU * mult_factor_used / 1000
                energyNeeded_GPU = runTime * dynamic_powerNeeded_GPU * mult_factor_used / 1000
                energyNeeded_core = runTime * powerNeeded_core * mult_factor_used / 1000
                eneregyNeeded_memory = runTime * powerNeeded_memory * mult_factor_used / 1000
                energyNeeded = runTime * powerNeeded * mult_factor_used / 1000

                # Carbon emissions: carbonIntensity is in g per kWh, so results in gCO2e
                CE_CPU = energyNeeded_CPU * carbonIntensity
                CE_GPU = energyNeeded_GPU * carbonIntensity
                CE_core = energyNeeded_core * carbonIntensity
                CE_memory  = eneregyNeeded_memory * carbonIntensity
                carbonEmissions = energyNeeded * carbonIntensity

                # Storing all outputs to catch the app state and adapt textual content
                output['coreType'] = coreType
                output['CPUmodel'] = CPUmodel
                output['numberCPUs'] = n_CPUcores
                output['CPU_model_n_cores'] = CPU_model_n_cores
                output['tdpCPU'] = CPUpower
                output['CPU_die_area'] = CPU_die_area
                output['usageCPUradio'] = usageCPUradio
                output['usageCPU'] = usageCPU_used
                output['GPUmodel'] = GPUmodel
                output['numberGPUs'] = n_GPUs
                output['tdpGPU'] = GPUpower
                output['GPU_die_area'] = GPU_die_area
                output['GPU_memory'] = GPU_memory
                output['usageGPUradio'] = usageGPUradio
                output['usageGPU'] = usageGPU_used
                output['memory'] = memory
                output['runTime_hour'] = actual_runTime_hours
                output['runTime_min'] = actual_runTime_min
                output['platformType'] = selected_platform
                output['locationContinent'] = locationContinent
                output['locationCountry'] = locationCountry
                output['locationRegion'] = locationRegion
                output['provider'] = selected_provider
                output['serverContinent'] = serverContinent
                output['server'] = server
                output['location'] = locationVar
                output['carbonIntensity'] = carbonIntensity
                output['PUE'] = PUE_used
                output['PUEradio'] = PUEradio
                output['mult_factor'] = mult_factor_used
                output['mult_factor_radio'] = mult_factor_radio
                output['appVersion'] = version
                metrics['energy_needed'] = energyNeeded
                metrics['carbonEmissions'] = carbonEmissions
                metrics['manufacturing_carbonEmissions'] = manufacturing_GWP
                metrics['manufacturing_abiotic_resources'] = manufacturing_ADP
                metrics['runTime'] = runTime
                metrics['power_needed'] = powerNeeded
                metrics['CE_CPU'] = CE_CPU
                metrics['CE_GPU'] = CE_GPU
                metrics['CE_core'] = CE_core
                metrics['CE_memory'] = CE_memory
                metrics['manufacturing_CE_CPU'] = manufacturing_GWP_CPU
                metrics['manufacturing_CE_GPU'] = manufacturing_GWP_GPU
                metrics['manufacturing_CE_memory'] = manufacturing_GWP_memory
                metrics['manufacturing_CE_other'] = manufacturing_GWP_other
                metrics['manufacturing_ADP_CPU'] = manufacturing_ADP_CPU
                metrics['manufacturing_ADP_GPU'] = manufacturing_ADP_GPU
                metrics['manufacturing_ADP_memory'] = manufacturing_ADP_memory
                metrics['manufacturing_ADP_other'] = manufacturing_ADP_other

            return output, metrics
        
        @self.callback(
            [
                Output('usageCPU_radio', 'options'),
                Output('usageGPU_radio', 'options'),
                Output('pue_radio', 'options'),
                Output('mult_factor_radio', 'options'),
            ],
            Input('language_dropdown', 'value'),
        )
        def translate_yes_no_options(language_id: str):
            """Translates the YES/NO radio labels.

            Args:
                language_id (str):  the language identifier for translation purpose
            """
            translated_yes_no_options = get_yes_or_no_options(language_id)
            return tuple(4 * [translated_yes_no_options])

        @self.callback(
            [
                Output('carbon_intensity_display_value', 'children'),
                Output('carbon_intensity_display', 'style'),
                Output('carbon_intensity_display_source', 'children'),
                Output('carbon_intensity_display_source', 'href'),
            ],
            Input('form_aggregate_data', 'data'),
            Input('location_continent_dropdown', 'value'),
            Input('versioned_data', 'data'),
            State('language_dropdown', 'value'), 
        )
        def display_carbon_intensity(form_data, selected_continent, versioned_data, language):
            hide = {'display': 'none', 'margin-top': '8px'}
            show = {'display': 'inline', 'flex-direction': 'column', 'margin-top': '8px'}

            if form_data is None or selected_continent == 'custom':
                return None, hide, None, None

            carbon_intensity = form_data.get('carbonIntensity')

            if carbon_intensity is None or versioned_data is None:
                return None, hide, None, None   

            data_source_path = versioned_data['data_source_path']
            source_label = TRANSLATIONS_DICT.get('Carbon_intensity_source', {}).get(language, 'source')

            return round(carbon_intensity, 2), show, source_label, data_source_path
        
    def _define_training_fields_callbacks(self):
        '''
        Embeds the callbacks specific the training fields.
        '''
        @self.callback(
            [
                Output('RandD_radio', 'options'),
                Output('retrainings_radio', 'options'),
            ],
            Input('language_dropdown', 'value'),
        )
        def translate_yes_no_options(language_id: str):
            """Translates the YES/NO radio labels.
            This callback cannot be merged into the corresponding one for other radio entries
            (like CPU usage...) because the HTML components of the retraining and R&D fields
            do not exist if the form is not a training form.

            Args:
                language_id (str):  the language identifier for translation purpose
            """
            translated_yes_no_options = get_yes_or_no_options(language_id)
            return tuple(2 * [translated_yes_no_options])
