import time
import dash 
import dash_mantine_components as dmc
from dash import html, Output, Input, no_update, callback
from dash_iconify import DashIconify
import dash_bootstrap_components as dbc
dash.register_page(__name__, path='/')

layout = html.Div([
    # dbc.Row(dmc.Space(h=100)),
    dbc.Row([
        dbc.Col(md=4),
        dbc.Col([
            dmc.Paper([dmc.Center(html.Div(
                        style={"width": 200},
                        children=dmc.LoadingOverlay([
                            dmc.Group(
                                # direction="column",
                                grow=False,
                                id="loading-form",
                                children=[
                                    dmc.TextInput(
                                        label="Username",
                                        id = 'username',
                                        placeholder="Your username",
                                        icon=[DashIconify(icon="radix-icons:person")],
                                    ),
                                    dmc.PasswordInput(
                                        label="Password",
                                        id = 'password',
                                        placeholder="Your password",
                                        icon=[DashIconify(icon="radix-icons:lock-closed")],
                                        style={"width":"200px"}
                                    ),
                                    
                                    dmc.Button(
                                        "Login", id="login_button", variant="outline", fullWidth=True
                                    ),
                                ],
                            ),
                            dmc.NotificationsProvider([
                            html.Div(id='output_state_login')
                                ]),
                            html.Div(id='hidden_div_for_redirect_callback'),
                        ])
                    ),style={"height":200, "width":"100%"})],p="50px", radius="xl", shadow="xl",withBorder=True, my="200px", style={'color':'#f2f2fa'})
        ], md=4, style={"display":"flex", "justifyContent":"center", "alignItems":"center"}),
    ]),

])



