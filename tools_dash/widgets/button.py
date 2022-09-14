import dash_bootstrap_components as dbc
from dash import html


class Button:
    def __init__(self,
                 label_name: str,
                 item_name: str,
                 *args, **kwargs
                 ):
        self._label_name = label_name
        self._item_name = item_name
        self.layout = self._layout()

    def __repr__(self):
        return f'{self.layout!r}'

    def _layout(self):
        return dbc.Button(self._label_name,
                          id='{}'.format(self._item_name),
                          outline=True,
                          className="ms-1",
                          color="success",
                          n_clicks=0)


def generate_button(label_name: str,
                    item_name: str,
                    **kwargs):
    return dbc.Button(label_name,
                      id='{}'.format(item_name),
                      outline=True,
                      className="ms-1",
                      color="success",
                      n_clicks=0)


def generate_buttons(list_buttons: list, extra_button: dbc.Button = None):
    buttons = [generate_button(lbl, itnm) for lbl, itnm in list_buttons]
    layout = html.Div(children=buttons)
    if extra_button:
        layout = [html.Div(extra_button), layout]

    return html.Div(children=layout,
                    className="d-flex justify-content-between")