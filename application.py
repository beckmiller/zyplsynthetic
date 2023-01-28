import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, DiskcacheManager, State, ctx, CeleryManager
# from explainerdashboard.custom import *
# from explainerdashboard import ClassifierExplainer, ExplainerDashboard
from sklearn.ensemble import RandomForestClassifier
# from explainerdashboard import ClassifierExplainer, ExplainerDashboard
# from explainerdashboard.datasets import titanic_survive
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import cohen_kappa_score, confusion_matrix
from flask import Flask, redirect
from flask_login import login_user, LoginManager, UserMixin, logout_user, current_user
import os
import diskcache
from celery import Celery
from uuid import uuid4
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc

if "REDIS_URL" in os.environ:
    # Use Redis & Celery if REDIS_URL set as an env variable
    from celery import Celery

    celery_app = Celery(
        __name__, broker=os.environ["REDIS_URL"], backend=os.environ["REDIS_URL"]
    )
    background_callback_manager = CeleryManager(
        celery_app, cache_by=[lambda: launch_uid], expire=60
    )

else:
    # Diskcache for non-production apps when developing locally
    import diskcache

    cache = diskcache.Cache("./cache")
    background_callback_manager = DiskcacheManager(
        cache, cache_by=[lambda: launch_uid], expire=60
    )



launch_uid = uuid4()

server_flask = Flask(__name__)
# external_scripts = ["https://unpkg.com/dash.nprogress@latest/dist/dash.nprogress.js"] #external_scripts=external_scripts,
application = dash.Dash(use_pages=True, server=server_flask,  suppress_callback_exceptions=True,
                        external_stylesheets=[
                            dbc.themes.COSMO, dbc.icons.FONT_AWESOME],
                            )
server = application.server
app = application.server
# du_configure = du.configure_upload(application, r"Datasets", use_upload_id=False,upload_api=None, http_request_handler=None)
application.title = 'arnur'
# application._favicon = ("zypl_logo.jpg")




server.config.update(SECRET_KEY=os.urandom(24))


login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/"


class User(UserMixin):
    # User data model. It has to have at least self.id as a minimum
    def __init__(self, username):
        self.id = username


@login_manager.user_loader
def load_user(username):
    """This function loads the user by user id. Typically this looks up the user from a user database.
    We won't be registering or looking up users in this example, since we'll just login using LDAP server.
    So we'll simply return a User object with the passed in username.
    """
    return User(username)



navbar = html.Div([dbc.NavbarSimple(
            children=[
                            
                
                # html.Div(id="user-status-header", style={"margin-left":"10px", "margin-top":'8px'}),
            ],
            brand="Barbel Beck",
            brand_href="/",
            dark=True,
            fluid=True,
            class_name='color-navbar'
        ), 
        dmc.Space(h=30)])



application.layout = html.Div([dcc.Location(id="url", refresh=False),
                                        navbar, 
                                        # html.H1('ASD'),
                                        html.Div(children=[
                                            html.Div(html.Div(id='hidden_div_for_redirect_callback')),
                                             dash.page_container
                                        ], id="page-content", className="content"),
                                        
])                                     
# @application.callback(
#     Output("user_status_header", "children"),
#     Output('user_status_header', 'style'),
#     Input("url", "pathname"),
# )
# def update_authentication_status(path):
#     logged_in = current_user.is_authenticated
#     if path == "/logout" and logged_in:
#         logout_user()

#     if logged_in:
#         return html.Span(dbc.Badge("logout",href="/logout",color="danger",className="me-1 text-decoration-none")), {'display':'block', "justify-content":"flex-end"}
#     else:
#         return html.Span(dbc.Badge("Login",href="/login",color="info",className="me-1 text-decoration-none")), {'display':'none'}


@application.callback(
    Output("output_state_login", "children"),
    Output("hidden_div_for_redirect_callback", "children"),
    Input("login_button", "n_clicks"),
    State("username", "value"),
    State("password", "value"),
    prevent_initial_call=True,
)
def login_button_click(n_clicks, username, password):
    if username == None and password == None:
        raise PreventUpdate
    try:
        if ctx.triggered_id == 'login_button':
            

            if username == "test" and  password == "test":
                login_user(User(username))
                return 'Done', dcc.Location(pathname="/main", id="someid_doesnt_matter", refresh=True)
            else:
                return dmc.Notification(
                    id="better-notify",
                    title="Error",
                    message=["Incorrect username or password"],
                    action="show"), dash.no_update, dash.no_update
    except:
        raise PreventUpdate


if __name__ == "__main__":
    application.run_server(debug=True,  host='0.0.0.0')
