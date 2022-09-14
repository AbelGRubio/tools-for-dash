import logging
import random

import dash_bootstrap_components as dbc
from dash import dcc, html, State, Output, Input, callback

from .form_interface import FormInterface


class CollapseForm(FormInterface):
    """
    This class have a button to collapse the form
    """
    def __init__(self, form_name: str,
                 logger: logging.Logger = None,
                 path: str = None,
                 **kwargs):
        super(CollapseForm, self).__init__(form_name=form_name,
                                           logger=logger, path=path, **kwargs)
        self.id_button_collapse = '{}{}buttoncollapse'.format(self.form_name,
                                                   str(int(random.random() * 1000)).zfill(3))
        self.id_collapse = '{}{}collapse'.format(self.form_name,
                                                 str(int(random.random() * 1000)).zfill(3))

    def add_callback_collapse_form(self):

        @callback(
            Output(self.id_collapse, "is_open"),
            [Input(self.id_button_collapse, "n_clicks")],
            [State(self.id_collapse, "is_open")],
        )
        def toggle_collapse(n, is_open):
            if n:
                return not is_open
            return is_open

    def reload_layout(self, state=True):
        self.splits_elements()

        buttons_layout = [_b[0] for _b in self.buttons.values()]
        extra_elements = self.add_extra_element()

        if len(extra_elements) > 0:
            _ly = [html.Div([dbc.Col(children=extra_elements),
                             html.Div(children=buttons_layout)
                             ],
                            className='d-flex justify-content-between')]
        else:
            _ly = buttons_layout

        aux_form = dbc.Form(children=[self._line_alert,
                                      *list(self.others_elements.values()),
                                      *_ly,
                                      ],
                            style=self._style,
                            id=self.id_form)
        title = self.form_name.replace('_', ' ').capitalize()
        self._layout = html.Div([
            dbc.CardHeader(
                dbc.Button(
                    dcc.Markdown(
                                "**{}**".format(title),
                                className='markdown1'
                            ),
                    color="black",
                    className='collapse_button1',
                    id=self.id_button_collapse,
                )
            ),
            dbc.Collapse(
                dbc.CardHeader(
                    [
                        aux_form,
                    ]),
                id=self.id_collapse,
                is_open=False,
            )
        ])

        self._set_inputs_and_states()
        if state:
            self.add_callback_collapse_form()
            self._add_callback()














