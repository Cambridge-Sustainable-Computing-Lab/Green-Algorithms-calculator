'''
The Green Algorithms calculator is a modularized two-pages application
fully implemented in [Dash](https://dash.plotly.com/). The code base is organized as follows: 

* the `app.py` script generates and runs the app,
* the `pages\home.py` and `pages\\ai.py` scripts define the page-level features of the app,
* the `blueprints\` scripts implement the calculator modules,
* the `assets\` folder contains media and CSS files,
* the `utils\` consists of Python and Dash utils.
* the `Green-Algorithms-data\` folder is a git-submodule that targets the [Green-Algorithms-data repository](https://github.com/Cambridge-Sustainable-Computing-Lab/Green-Algorithms-data) containing the backend data,

The calculator is a `DashProxy` object, that wraps both the HTML components (its layout) and the logic (the attached callbacks) of the app. Note that the [`DashProxy` object](https://www.dash-extensions.com/sections/enrich#a-dashproxy) 
is a "drop-in replacement" for the `dash.Dash` object. We must use it because of the DashBlueprints class for modularization.
'''
### WARNING: Above text is part of the online documentation. Be careful when modifying it.

import os
import dash
from flask import send_file # Integrating Loader IO

from dash import html, dcc, ctx, _dash_renderer
from dash.dependencies import Input, Output, State

from dash_extensions.enrich import DashProxy
import dash_mantine_components as dmc
_dash_renderer._set_react_version("18.2.0")

from utils.handle_inputs import load_data, CURRENT_VERSION, DATA_DIR, get_available_versions, APP_VERSION_OPTIONS_LIST
from pages.home import HOME_PAGE, HOME_PAGE_ID_PREFIX
from pages.ai import AI_PAGE, AI_PAGE_ID_PREFIX

from blueprints.translation.translatable_div_text_blueprint import translatable_div_text
from blueprints.translation.translatable_markdown_text_blueprint import translatable_markdown_text


###################################################
## CREATE APP AND PAGES

external_stylesheets = [
    dict(
        href="https://fonts.googleapis.com/css?family=Raleway:300,300i,400,400i,600|Ruda:400,500,700&display=swap",
        rel="stylesheet"
    ),
]

app = DashProxy(
    __name__,
    use_pages=True,
    external_stylesheets=external_stylesheets,
    # Below tags are to ensure proper responsiveness on mobile devices
    meta_tags=[
        dict(
            name= 'viewport',
            content="width=device-width, initial-scale=1.0" 
        )
    ],
    ############
    # DEBUGONLY: suppress_callback_exceptions = False
    suppress_callback_exceptions=True
    # Callbacks exceptions are removed because otherwise warning messages are raised
    # due to callbacks based on HTML components that are said to be nonexistent
    # whereas they are just implemented on the other app page.
    # In case a callback does not work, allowing callback_exception back
    # may help to find the right fix.
)

app.title = "Green Algorithms"
server = app.server

HOME_PAGE.register(app, module='home', path='/', title='Green Algorithms - Classic view')
AI_PAGE.register(app, module='ai', path='/ai', title='Green Algorithms - AI view')

image_dir = os.path.join("assets", "images")

###################################################
## CREATE NAVBAR

name_per_page = {'Home': translatable_div_text('Classic-view').embed(app), 'Ai': translatable_div_text('AI-view').embed(app)}
pages = list(dash.page_registry.values())

appVersions_options = get_available_versions()

def get_pages_navbar_layout():
    '''
    Defines the navigation bar layout. It relies on the `NavLink` item from the
    dash_mantine_components library and the built-in navigation feature of dash pages.
    '''

    return html.Div(
    [
        dmc.NavLink(
            label=html.Div(
                name_per_page[pages[0]['name']],
                className='navlink-label',
                id=f'{pages[0]["name"]}-navlink-label',
            ),
            # Built-in navigation from Dash (see the documentation)
            href=pages[0]["path"],
            id=f'{pages[0]["name"]}-navlink',
            className='page-navlink',
        ),

        dmc.NavLink(
            label=html.Div(
                name_per_page[pages[1]['name']],
                className='navlink-label',
                id=f'{pages[1]["name"]}-navlink-label',
            ),
            # Built-in navigation from Dash (see the documentation)
            href=pages[1]["path"],
            id=f'{pages[1]["name"]}-navlink',
            className='page-navlink',
        ),
    ],
    className = 'pages-menu',
)

pages_navbar = get_pages_navbar_layout()

versions_choice = html.Div(
    [
        html.Div(
            [
                html.Div('i', className='tooltip-icon'),

                html.P(translatable_div_text('Version tooltip').embed(app), className='tooltip-text'),
            ],
            className='tooltip',
            id='data_version_tooltip'
        ),
        
        html.Div(
            [
                html.P(translatable_div_text("Change data version").embed(app), id='old_version_link'),
            ],
            className='change_version_text'
        ),

        html.Div(
            dcc.Dropdown(
                id="app_versions_dropdown",
                options=appVersions_options,
                className='bottom-dropdown',
                clearable=False,
                value=CURRENT_VERSION
            ),
            id='app_versions_dropdown_div',
            style={'display': 'none'},
        )
    ],
    className='form-row short-input',
    id='versions_div',
)

language_choice = html.Div(
    [
        html.Div(
            [
                html.P(translatable_div_text("Change language").embed(app), id='language_choice_link'),
            ],
            className='change_version_text'
        ),

        html.Div(
            [
                dcc.Dropdown(
                    id="language_dropdown",
                    options=[
                    {"label": "English", "value": "en"},
                    # Below line is commented because the French translation is not completed yet
                    # {"label": "Français", "value": "fr"},
                ],
                    value='en',
                    persistence=True,
                    clearable=False,
                ),
            ],
            id='language_dropdown_div',
            style={'display': 'none'},
        ),
    ],
    className='form-row short-input',
    id='language_div'
)

###################################################
## CREATE LAYOUT

app.layout = dmc.MantineProvider(
    html.Div(
        [
            #### BACKEND PURPOSE ####

            # Used to forward the version coming from a CSV uploaded to the Home page 
            dcc.Store(id=f"{HOME_PAGE_ID_PREFIX}-version_from_input"),
            # Used to forward the version coming from a CSV uploaded to the Ai page 
            dcc.Store(id=f"{AI_PAGE_ID_PREFIX}-version_from_input"),
            # A dictionnary containing all the backend data used everywhere in the app
            dcc.Store(id="versioned_data"),
            # The component storing the url state, only used to trigger callback when the app is loaded
            dcc.Location(id='url_content', refresh='callback-nav'), 

            #### HEADER ####

            html.Div(
                [
                    html.Div(
                        [
                            html.Img(
                                src=os.path.join(image_dir, "ga_logo_tree.svg"),
                                id="ga_logo",
                                className="header-logo",
                                style={"width": "90px", "padding": "5px", "padding-bottom": "10px"},
                            ),
                            html.Div(
                                [
                                    html.H1(translatable_div_text("Green Algorithms calculator").embed(app)),
                                    html.P(translatable_div_text("Subtitle").embed(app)),
                                ],
                                className='header_title_container',
                            ),
                        ],
                        className='header_title',
                        style={"display": "flex", "flex-direction": "row", "align-items": "center"},
                    ),
                
                    # html.Div(
                    #     [
                    #         html.Hr(style={'background-color': 'rgb(60, 60, 60)'}),
                    #     ],
                    #     className='Hr_div_header',
                    # ),

                    pages_navbar,

                    html.Div(
                        [
                            language_choice,
                            versions_choice,
                            html.Div(
                                html.A(
                                    html.Button("Data and code", id='github-link-button', className='btn-download_csv',),
                                    href='https://github.com/Cambridge-Sustainable-Computing-Lab/Green-Algorithms-calculator',
                                    target="_blank",
                                ),
                                className='header-button-container'
                            )
                        ],
                        className='version_and_language_div'
                    ),

                ],
                className='container header'
            ),

            #### PAGE CONTENT #####
            
            # Pages are registered manually above and their layout is inserted in the app
            # as suggested in the official documentation (https://dash.plotly.com/urls)
            dash.page_container,

            # TODO include outstanding issues and PRs
                        html.Div(
                            [
                                html.H2(translatable_div_text("Some_news").embed(app)), # TODO align this left?
            
                                html.P(translatable_div_text('Carbon_intensity_update').embed(app)),
            
                                html.P(translatable_markdown_text('Release_message').embed(app)),
            
                                html.P(translatable_markdown_text('Bugs_message').embed(app)),
            
                                html.Div(
                                    [
                                        html.A(
                                            html.Button(translatable_div_text('More on the project website').embed(app), id='website-link-button'),
                                            href='https://www.green-algorithms.org',
                                            target="_blank",
                                            className='button-container'
                                        ),
                                    ],
                                    className='buttons-row'
                                ),
                            ],
                            className='container footer'
                        ),

            #### FOOTERS #####

            # TODO revisit the footer
        
            html.Div(
                [
                    ### DATA AND CODE ###

                    html.Div(
                        [
                            html.H2(translatable_div_text("Data and code").embed(app)),

                            html.Div(translatable_markdown_text("Data_and_code_text").embed(app)),
                        ],
                        className='container footer'
                    ),

                ],
                className='super-section data-questions'
            ),

            #### HOW TO CITE ####

            html.Div(
                [
                    html.H2(translatable_div_text("How to cite this work").embed(app)),

                    html.Div(translatable_markdown_text("How_to_cite_text").embed(app))
                ],
                className='container citation footer'
            ),

            #### ABOUT US ####

            html.Div(
                [
                    html.H2(translatable_div_text("About us").embed(app)),

                    html.Div(translatable_markdown_text('About_us_text').embed(app), className='authors'),

                    html.Div(translatable_markdown_text('About_us_text_2').embed(app), className='authors'),
                ],
                className='container about-us footer'
            ),

            #### FUNDERS ####

            # TODO add funders logos

            #### SHOW YOUR STRIPES ####

            html.Div(
                [
                    html.H2(translatable_div_text("ShowYourStripes").embed(app)),

                    html.Div(translatable_markdown_text("ShowYourStripes_text").embed(app)),

                    html.Div(translatable_markdown_text("More_on").embed(app)),
                    
                    html.Div(translatable_markdown_text("Additional_credits").embed(app)),

                ],
                className='container show-stripes footer'
            ),
        ],
        className='fullPage'
    )
)



###################################################
# CALLBACKS #

# These are the few callbacks implemented at the app level, namely
# those related to the version choice and backend data loading, 
# and page navigation.

################## NAVIGATION BAR

@app.callback(
        [
            Output('Home-navlink', 'style'),
            Output('Classic-view-text_value', 'style'),
            Output('Ai-navlink', 'style'),
            Output('AI-view-text_value', 'style'),
        ],
        Input('url_content', 'pathname')
)
def style_navlink(url_pathname: str):
    """ 
    Once the page is changed (built-in page navigation), this
    callback adapts the css of the navigation labels.

    Args:
        url_pathname (str): used to retrieve the page that is being displayed.
    """
    # Define the different styles possibilities
    to_be_clicked_style = {'cursor': 'pointer'}
    to_be_clicked_label_style = {'text-decoration': 'underline', 'font-weight': '200'}
    current_page_navlink_style = {'cursor': 'default'}
    current_page_label_style = {'text-decoration': 'none', 'font-weight': '600'}
    # Allocate the style dictionnaries to the right ouputs
    if 'ai' in url_pathname:
        return to_be_clicked_style, to_be_clicked_label_style, current_page_navlink_style, current_page_label_style
    else:
        return current_page_navlink_style, current_page_label_style, to_be_clicked_style, to_be_clicked_label_style


################## LANGUAGE CHOICE
    
@app.callback(
    Output('language_dropdown_div', 'style'),
    Input('language_choice_link','n_clicks'),
    State('language_dropdown_div', 'style'),
)
def display_oldVersion(clicks: int, previous_style:dict):
    """
    Show the different available languages.
    """
    if (clicks is not None):
        return {'display':'flex', 'flex-direction': 'row', 'width': 'fit-content'}
    else:
        return previous_style

################## APP VERSIONING

@app.callback(
    Output('app_versions_dropdown','value'),
    [
        Input(f"{HOME_PAGE_ID_PREFIX}-version_from_input",'data'),
        Input(f"{AI_PAGE_ID_PREFIX}-version_from_input",'data'),
    ]
)
def set_version_from_csv_inputs(version_from_home_input: str, version_from_ai_input: str):
    """
    Set the app version based on csv inputs 
    dropped either from the home page or the ai page.
    """
    # We use the ctx.triggered_id to get know which input triggered the callback.
    new_version = None
    if HOME_PAGE_ID_PREFIX in ctx.triggered_id:
        new_version = version_from_home_input
    elif AI_PAGE_ID_PREFIX in ctx.triggered_id:
        new_version = version_from_ai_input
    return new_version

@app.callback(
    Output('app_versions_dropdown_div', 'style'),
    [
        Input('old_version_link','n_clicks'),
        Input('app_versions_dropdown','value')
    ],
    [
        State('app_versions_dropdown_div', 'style')
    ]
)
def display_oldVersion(clicks: int, version: str, oldStyle: dict):
    """
    Show the different available versions.
    """
    if (clicks is not None)|((version is not None)&(version != CURRENT_VERSION)):
        return {'display':'flex', 'flex-direction': 'row', 'width': 'fit-content'}
    else:
        return oldStyle
    
@app.callback(
    Output("versioned_data", "data"),
    [
        # To force initial triggering
        Input('url_content','search'),
        Input('app_versions_dropdown','value'),
    ],
)
def load_data_from_version(_, new_version:str) -> dict:
    """
    Loads all the backend data required to propose consistent options to 
    the user and ensures calculator computations can be performed. 
    This data comes from the csv files stored in the `/data` folder. 
    
    It is loaded when the app is launched and then triggers all the callbacks 
    that require backend data (cores, server, location, carbon intensity and metrics-related callbacks).
    As the name suggests, this data is versioned to ensure the results replicability across the
    different versions of the data.

    Args:
        _ (url_content): non-used argument, but required to trigger the callback when the app is loaded.
        new_version (str): the data version to load.

    Returns:
        the only app level variable, containing all the backend data.
    """
    # Collect input version and check validity
    if new_version is None:
        new_version = CURRENT_VERSION
    assert new_version in APP_VERSION_OPTIONS_LIST + [CURRENT_VERSION]

    # Load corresponding backend data
    if new_version == CURRENT_VERSION:
        new_data = load_data(version=CURRENT_VERSION)
    else:
        new_data = load_data(version=new_version)

    versioned_data = vars(new_data)
    return versioned_data


# Loader IO
@app.server.route('/loaderio-1360e50f4009cc7a15a00c7087429524/')
def download_loader():
    return send_file('assets/loaderio-1360e50f4009cc7a15a00c7087429524.txt',
                        mimetype='text/plain',
                        attachment_filename='loaderio-1360e50f4009cc7a15a00c7087429524.txt',
                        as_attachment=True)

if __name__ == '__main__':
    app.run_server(debug=True)