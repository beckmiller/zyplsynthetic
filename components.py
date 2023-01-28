import feffery_antd_components as fac
from dash import html, dash_table
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import uuid 

def Create_DataTable(df, id=str(uuid.uuid4), table_name=None, whiteSpace="", page_size=10, filter_action="none", sort_action="none"):
    return card_style(html.Div([
        html.Center(html.Strong(table_name, style={"color":"black"})),
        dash_table.DataTable(
                        data=df.to_dict('records'),
                        id=id,
                        columns=[{'id': c, 'name': c} for c in df.columns],
                        filter_action=filter_action,#native
                        style_cell={'textAlign': 'center',
                                    'padding': '5px'},
                         style_data_conditional=[
                            {
                                'if': {
                                    'state': 'active'  # 'active' | 'selected'
                                },
                            'backgroundColor': 'rgba(0, 116, 217, 0.5)',
                            'border': 'none'#'1px solid rgb(0, 116, 217)'
                            },
                         ],
                        page_action="native",
                        style_header={
                            'backgroundColor': '#f2f2fa',
                            'fontWeight': 'bold',
                            "color":"black",
                            # 'border': '1px solid black',
                            'font-size': '14px',
                            'border':'none'
                        },
                        style_data={'backgroundColor':'#f2f2fa', 
                        "color":"black", 'whiteSpace': whiteSpace},
                        style_table={'overflowY': 'auto'},
                        page_size=page_size,
                        # filter_action="native",
                        sort_action=sort_action,# native 
                        page_current= 0,
                        style_as_list_view=True,
                        )
    ]))


def tabs(first_content, second_content):
    return fac.AntdTabs(
                [
                    fac.AntdTabPane(
                        html.Div([
                            first_content],
                            style={
                                # 'backgroundColor': 'rgba(241, 241, 241, 0.4)',
                                # 'height': '200px',
                                # 'display': 'flex',
                                'justifyContent': 'center',
                                'alignItems': 'center'
                            }
                ),
                        tab='Result models',
                        key='Result models'
                    ),
                    fac.AntdTabPane(
                        html.Div([
                            second_content],
                            style={
                                # 'backgroundColor': '#cbd3dd',
                                # 'height': '200px',
                                # 'display': 'flex',
                                'justifyContent': 'center',
                                'alignItems': 'center'
                            }
                ),
                        tab='Backtest',
                        key='Backtest'
                    )
                ],
                tabPaneAnimated=True,
                tabPosition='top'
            )


def dmc_select(data=[], clearable=False, label=None, id=None, placeholder=None, style=None, searchable=True):
    return dmc.Select(
                                    label=label,
                                    placeholder=placeholder,
                                    id=id,
                                    clearable=clearable,
                                    data=data,
                                    style=style,
                                    searchable=searchable,
                                    nothingFound="No options found",
                                    persistence=True
                                    
                                )

def dmc_buttons(label=None, id=id, gradient={"from": "indigo", "to": "cyan"}, style={}):
    return dmc.Button(
                        label,
                        variant="gradient",
                        gradient=gradient,
                        style=style,
                        id=id,
                        n_clicks=0
                        
                        )


def dmc_accordion(backtest_datasets=None, datasets=None):
    return dmc.Accordion(
                        disableChevronRotation=False,
                        children=[
                            dmc.AccordionItem(
                                [
                                    dmc.AccordionControl(
                                        "Datasets",
                                        icon=DashIconify(
                                            icon="ic:outline-dataset-linked",
                                            color=dmc.theme.DEFAULT_COLORS["blue"][6],
                                            width=20,
                                        ),
                                    ),
                                    dmc.AccordionPanel([
                                        datasets
                                    ]),
                                ],
                                value="info",
                            ),
                            dmc.AccordionItem(
                                [
                                    dmc.AccordionControl(
                                        "Backtest datasets",
                                        icon=DashIconify(
                                            icon="ph:database-bold",
                                            color=dmc.theme.DEFAULT_COLORS["red"][6],
                                            width=20,
                                        ),
                                    ),
                                    dmc.AccordionPanel([
                                        backtest_datasets
                                    ]),
                                ],
                                value="addr",
                            ),
                        ],
                        radius="xl",
                        variant="separated"
                    )

def fac_antdswitch(id=None, checkedChildren=None, unCheckedChildren=None):
    return fac.AntdSwitch(
                        id=id,
                        checkedChildren=checkedChildren,
                        unCheckedChildren=unCheckedChildren
                                )


def dmc_input(id=None, style=None, label="", description="", placeholder=""):
    return dmc.TextInput(
        id=id,
        label=label, 
        style=style,
        description=description,
        placeholder=placeholder 
        ),


def dmc_chips(id=""):
    return html.Div([
        html.Label("model list"),
        dbc.DropdownMenu([
                                dmc.ChipGroup(
                                    [
                                    dmc.Chip(
                                        x,
                                        value=y,
                                        variant="filled",
                                        size='sm',
                                        radius=10,
                                    )
                                    for x, y in {"Extra Trees Classifier":"et", 
                                                                    "Ridge Classifier":"ridge", 
                                                                    "SVM - Linear Kernel":"svm", 
                                                                    "Dummy Classifier":"dummy",
                                                                    "Random Forest Classifier":"rf",
                                                                    "Gradient Boosting Classifier":"gbc",
                                                                    "Ada Boost Classifier":"ada",
                                                                    "Extreme Gradient Boosting":"xgboost",
                                                                    "Logistic Regression":"lr",
                                                                    "CatBoost Classifier":"catboost",
                                                                    "Decision Tree Classifier":"dt",
                                                                    "Linear Discriminant Analysis":"lda",
                                                                    "Light Gradient Boosting Machine":"lightgbm",
                                                                    "K Neighbors Classifier":"knn",
                                                                    "Naive Bayes":"nb",
                                                                    "Quadratic Discriminant Analysis":"qda"}.items()
                                            ],
                                            id=id,
                                            value=["et",  "ridge", "svm", "dt", "knn", "lr", "rf", "gbc", "catboost"],
                                            multiple=True,
                                            mb=10,
                                            align="center"
                                            )
                            ],
                            label="Models")])
    

def card_style(content, style={"display":"block"}, style1={'border-radius': '10px'},   id=str(uuid.uuid4()), color="#f2f2fa"):
    return dbc.CardGroup([
        dbc.Card([
            dbc.CardBody([
                    content
            ])
        ], color=color, style=style1)
    ], style=style, id=id)