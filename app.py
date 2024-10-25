import dash
from dash import html
import dash_bootstrap_components as dbc


# Create app ---------------------------------------------------------------
app = dash.Dash(
    __name__, suppress_callback_exceptions = True,
    external_stylesheets=[dbc.themes.LITERA, dbc.icons.FONT_AWESOME],
    use_pages=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1", 'charSet':'“UTF-8”'}])

server = app.server
app.title = "Sample Visualizer"

sidebar = html.Div(
    [
        html.Div(
            [
                html.Img(src="assets/menu.png", style={"width": "3.5rem", 'margin-left': '-0.5vw'}),
                html.H2("Menu", style={'margin-left': '0.5vw'}),
            ],
            className="sidebar-header",
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.I(className="fas fa-eye", **{'aria-hidden': 'true'}, style = {'margin-right': '0.2vw'}),
                        html.Span("Overview")
                    ],
                    href="/",
                    active="exact"
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa fa-cubes"),
                        html.Span("3D scans"),
                    ],
                    href="/scans",
                    active="exact"
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa fa-bar-chart"),
                        html.Span("Geochemistry"),
                    ],
                    href="/geochem",
                    active="exact"
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa fa-arrow-down"),
                        html.Span("Depth profile"),
                    ],
                    href="/profile",
                    active="exact"
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa fa-snowflake"),
                        html.Span("Morph. complexity")
                    ],
                    href="/morph-complex",
                    active="exact"
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-square-root-variable"),
                        html.Span("Statistics")
                    ],
                    href="/stats",
                    active="exact"
                )
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar", style = {'margin-right': '2rem'}
)

app.layout = html.Div([
        sidebar,
        dash.page_container

], style = {"height": "100vh" ,"margin-bottom": "0px"})


# Runs the app ------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=True)