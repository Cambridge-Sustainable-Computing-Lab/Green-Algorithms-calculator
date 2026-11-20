# Pages

The calculator contains two pages:

- the [`home.py` page](../../developer_guide/pages/home_page.md) implements the classic (and original) view of the calculator
- the [`ai.py` page](../../developer_guide/pages/ai_page.md) implements an AI-dedicated page, built on the same blocks

## Pages implementation

The above two scripts implement both the layout and callbacks of the pages. As explained in our [getting_started file](../../developer_guide/getting_started.md#pages), pages are implemented as `DashBlueprint` instances. These are then registered in the app.

Our pages layout mostly resumes to correctly assembling the modules layout. Thus, the few page-level callbacks are designed to ensure the interaction between the different modules: forward the `ImportExportBlueprint` data to the `FormBlueprint` when the user imports data and reciprocally when the user exports the form state, turn the `FormBlueprint` results into metrics to be displayed in the `CoreImpactsBlueprint` and `EquivalentsMetricsBlueprint`... These callbacks mostly involve `dcc.Store` components as they act as intermediate variables between the different modules.

??? danger "ID prefix must be manually added for outer callbacks"
    The callbacks that benefit from automatic ID prefixing are only those that are directly attached to the `DashBlueprint` instance. So for all callbacks implemented at the page level for instance, the ID prefix must be manually added to the Input, Output and State.

``` py title='An example of "outer" callback'
HOME_PAGE = DashBlueprint()
HOME_PAGE_ID_PREFIX = 'main'

@HOME_PAGE.callback(
        Output(f'{HOME_PAGE_ID_PREFIX}-export-content', 'data'),
        Input(f"{HOME_PAGE_ID_PREFIX}-btn-download_csv", "n_clicks"),
        State(f'{HOME_PAGE_ID_PREFIX}-form_aggregate_data', 'data'),
        State(f'{HOME_PAGE_ID_PREFIX}-form_output_metrics', "data"),
)
def forward_form_input_to_export_module(_, form_aggregate_data, form_output_metrics):
    ...
```

## The navigation bar

::: app.get_pages_navbar_layout
    handler: python
        # virer les argument et return

::: app.style_navlink
    handler: python