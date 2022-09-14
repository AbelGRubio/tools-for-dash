import dash_bootstrap_components as dbc
from dash import html


class Sidebar:
    def __init__(self, sidebar_dict):
        super(Sidebar).__init__()
        self.s_dict = sidebar_dict

    def create_sidebar(self):
        sidebar = html.Div(
            [
                html.Div(
                    [
                        html.Img(src=r'../assets/imgs/logo-blanco.png', style={"width": "3rem"}),
                        html.H5("Waterfall Analyzer", className='sidebar_title'),
                    ],
                    className="sidebar-header",
                ),
                html.Hr(),
                dbc.Nav(
                    [
                        dbc.NavLink(
                            [html.I(className=self.s_dict[i]['icon']),
                             html.Span(self.s_dict[i]['name'])],
                            href=self.s_dict[i]['ref'],
                            active=self.s_dict[i]['active'],
                        ) for i in self.s_dict
                    ],
                    vertical=True,
                    pills=True,
                ),
                html.Div('Software Version 1.2.3', className='text_sidebar_footer1')
            ],
            className="sidebar",
        )
        return sidebar
