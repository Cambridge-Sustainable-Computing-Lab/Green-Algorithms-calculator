"""
Implements the methodology blueprint.
"""

from dash_extensions.enrich import DashBlueprint, PrefixIdTransform
from dash import html, dcc

from utils.utils import custom_prefix_escape

from blueprints.translation.translatable_markdown_text_blueprint import translatable_markdown_text
from blueprints.translation.translatable_div_text_blueprint import translatable_div_text

class MethodologyBlueprint(DashBlueprint):
    '''
    Actually, as the methodology content is static, there is no callback to implement.
    The reason for this file is mostly to respect the structure of the other blueprint folders.
    '''
    
    def __init__(
            self,
            id_prefix: str,
            to_add_ai_methodology_text: bool = False
        ):
        '''
        Args:
            additional_formula_textual_content (bool): whether to add the AI textual content in the methodology container
        '''
        super().__init__(transforms = [PrefixIdTransform(prefix = id_prefix, escape=custom_prefix_escape)])
        ai_methodology_text = dcc.Markdown()
        if to_add_ai_methodology_text:
            ai_methodology_text = html.Div(
                translatable_markdown_text('ai_methodology_content').embed(self),
                style={'margin-bottom': '10px'}
            )
        self.layout = self._get_layout(ai_methodology_text)
        

    def _get_layout(self, ai_methodology_text: html.Div):
        return html.Details(
            [
                html.Summary(
                    translatable_div_text("Methodology_header").embed(self),
                    className='methodology-summary',
                ),
                html.Div(
                    [
                        #### FORMULA ####

                        html.Div(
                            [
                                html.H2(translatable_div_text("The_formula_header").embed(self)),

                                ai_methodology_text,

                                html.Div(translatable_markdown_text("the_formula_detail").embed(self)),

                            ],
                            className='container formula'
                        ),

                        #### DEFINITIONS ####

                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H2(translatable_div_text("About_CO2e").embed(self)),

                                        html.Div(translatable_markdown_text('about_co2_detail').embed(self))
                                    ],
                                    className='container'
                                ),

                                html.Div(
                                    [
                                        html.H2(translatable_div_text("What_is_a_tree-month").embed(self)),

                                        html.Div(translatable_markdown_text("What_is_a_tree-month_details").embed(self)),
                                    ],
                                    className='container'
                                ),
                            ],
                            className='super-section definitions'
                        ),
                    ],
                    className='methodology-container'
                ),
            ],
            className='container methodology-panel',
        )
