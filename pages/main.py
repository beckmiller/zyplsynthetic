from importlib.resources import path
import dash_bootstrap_components as dbc
import dash
from dash import html, dcc, dash_table, callback, Input, Output, State, long_callback, get_app
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from urllib.parse import unquote
import dash_mantine_components as dmc
from datetime import date
import base64
import io
import pandas as pd
import numpy as np
import dash_uploader as du
from dash.exceptions import PreventUpdate
import os
# from db import Projects
import datetime
import feffery_antd_components as fac
from components import *
from synthetic_generator import SyntheticDataGenerator
from generate_barbell import generate_barbell_distribution
app = dash.get_app()
du.configure_upload(app, r"pages/upload_datasets/",
                    use_upload_id=False, upload_api=None, http_request_handler=None)


def title():
    return f"Barbell"


dash.register_page(__name__,
                   path="/main",
                   title=title)


def get_upload_component(id):
    return du.Upload(
        id=id,
        max_file_size=1800,  # 1800 Mb
        filetypes=['csv', 'xlsx', 'xls'],
        # upload_id=uuid.uuid1(),  # Unique session id
        pause_button=True,
        default_style={'color': 'green'},
    )


def get_app_layout():
    return html.Div(
        [
            html.Div(
                [
                    get_upload_component(id='dash-uploader'),
                    # html.Div(id='callback-output'),
                ],
                style={  # wrapper div style
                    'textAlign': 'center',
                    'width': '600px',
                    'padding': '10px',
                    'display': 'inline-block'
                }),
        ],
        style={
            'textAlign': 'center',
        },
    )


def layout(project_name=None):
    return html.Div([
        dbc.Row([

            dbc.Col([
                dbc.CardGroup([
                    dbc.Card([
                        dbc.CardBody([
                            html.Strong(project_name, hidden=True,
                                        key=project_name, id='hidden_project_name'),
                            html.Div(html.Center(html.I(
                                className="fas fa-solid fa-cloud-arrow-up fa-3x")), style={'margin-top': '25px'}),
                            get_app_layout()
                        ])
                    ], style={'border-radius': '15px', },  color="#f2f2fa", outline=False, body=True)
                ])
            ], md=6),
            dbc.Col([
                dbc.Row([
                    


                    dbc.Col([
                        card_style(html.Div([
                            dbc.Row([
                                dbc.Col([
                                    dmc_select(id="select_target",
                                               label="Select target"),
                                ]),
                                dbc.Col([
                                    #  dmc_select(id="select_macro", label="Select macro columns"),
                                    dmc.MultiSelect(
                                        id="select_macro", label="Select macro columns", limit=3, persistence=True)
                                ])
                            ]),
                            dmc.Space(h=20),
                            dbc.Row([
                                dbc.Col([
                                    #  dmc_input(id="input_samples")
                                    dmc.NumberInput(id="input_samples",
                                                    label="Input samples", persistence=True)
                                ]),
                                dbc.Col([
                                    html.Center(dmc_buttons(label="Generate", id="button_generate", style={
                                        "margin-top": "25px", "width": "250px"}))
                                ])
                            ]),
                        ]), style1={'border-radius': '10px', "height":"280px"})
                    ])
                ]),
            ], md=6),
        ]),
        dmc.Space(h=30),
        dbc.Row([
        dbc.Col([
            dcc.Loading(html.Div(id='output_data_upload'),
                                    type="circle", color="#00faae",),
        ], md=6),
        
        dbc.Col([
            dcc.Loading(html.Div(id="generate_main_data"))
        ], md=6)

                    ]),

        dcc.Store(id="size_of_data"),
        # dcc.Download(id="download-component_logs"),
        dbc.Row([
                html.Div(id="download_button"),
                html.Center(dmc.Button(
                            children=[html.I(className="fa fa-download mr-1"), " Download"],
                            # variant="gradient",
                            # gradient={"from": "indigo", "to": "cyan"},
                            style={"margin-top":"25px", "width": 200},
                            id='btn_logs',
                            # class_name="all_button",
                            
                        ), style={'display':'none'}, id="div_button_display"),

                dcc.Download(id="download-component_logs"),
                # dcc.Store(id='df_logs')
            ])
 

        
    ])


@du.callback(
    output=[Output("output_data_upload", "children"),
            Output('select_target', 'data'),
            Output('select_macro', 'data'),
            Output("size_of_data", "data")],
    id="dash-uploader",
)
def callback_on_completion(status: du.UploadStatus):
    df_path = str(status.latest_file).split('/')
    size_of_data = round(status.uploaded_size_mb, 2)
    name_dataset = df_path[3]
    pathh = os.getcwd()
    if '.xlsx' in df_path[3]:
        df = pd.read_excel(f'{pathh}/pages/upload_datasets/{df_path[3]}')
    elif '.csv' in df_path[3]:
        df = pd.read_csv(f'{pathh}/pages/upload_datasets/{df_path[3]}')
    size_of_data = {'size_of_data': size_of_data, 'name_dataset': name_dataset}
    columns = df.columns
    return Create_DataTable(df=df, id="download_df", table_name="Loaded dataset"),  columns, columns, name_dataset


@callback(
    Output("generate_main_data", "children"),
    Output("div_button_display", "style"),
    Input("button_generate", "n_clicks"),
    State('select_target', 'value'),
    State('select_macro', 'value'),
    State('input_samples', 'value'),
    State('size_of_data', 'data'),
    prevent_initial_call=True
)
def generete(n, select_target, select_macro, input_samples, dataset_name):
    print(dataset_name)
    # if dash.ctx =="button_generate":
    if n > 0:
        if '.xlsx' in dataset_name:
            df_main = pd.read_excel(f'pages/upload_datasets/{dataset_name}')
        elif '.csv' in dataset_name:
            df_main = pd.read_csv(f'pages/upload_datasets/{dataset_name}')
        else:
            df_main = pd.read_csv(f'pages/upload_datasets/{dataset_name}')

        df = df_main.drop(columns=select_macro)

        synth_data = SyntheticDataGenerator(
            df, select_target).generate_data(input_samples)
        gen = generate_barbell_distribution(
            df_main, select_macro,  int(synth_data.shape[0]))
        synth_data = synth_data.reset_index(drop=True)
        barbell_df = pd.concat([synth_data, gen], axis=1)
        # gen.to_csv("gen.csv")
        # synth_data.to_csv("synth_data.csv")
        return Create_DataTable(barbell_df, id="barbell_df",table_name="Generated Barbell"), {"display":"block"}
    else:
        # dash.exceptions.PreventUpdate
        return "Error"


@callback(
    Output("download-component_logs", "data"),
    Output("btn_logs", "children"),
    Input("btn_logs", "n_clicks"),
    [State('barbell_df', 'data')],
    prevent_initial_call=True,
)
def datatable(n, data):
    try:
        if dash.ctx.triggered_id == "btn_logs":
            df = pd.DataFrame(data)
            # df = r.get('df')
            return dcc.send_data_frame(df.to_excel, "Logs.xlsx", sheet_name="Sheet_name_1"), dash.no_update
        else:
            dash.exceptions.PreventUpdate
    except:
        raise PreventUpdate