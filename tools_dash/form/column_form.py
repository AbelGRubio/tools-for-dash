import logging
import random

import dash_bootstrap_components as dbc
from dash import dcc, html, State, Output, Input, callback

from .collapse_form import CollapseForm


class ColumnForm(CollapseForm):
    """
    clase que se heredada de Collapseform y muestra el formulario en columnas.
    teniendo los botones al lado derecho
    """
    def __init__(self, form_name: str,
                 logger: logging.Logger = None,
                 path: str = None,
                 **kwargs):
        super(ColumnForm, self).__init__(form_name=form_name,
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

    def split_into_columns(self, buttons_layout: list):
        layout_columns = []
        if self.others_elements:
            aux = []
            cnt = 0
            max_cont = 2
            size_elements = len(self.others_elements)
            for num, _e in enumerate(self.others_elements.values()):
                aux.append(_e)
                cnt += 1
                if cnt == max_cont:
                    layout_columns.append(dbc.Col(children=aux,
                                                  className='col-sm-3'))
                    aux = []
                    cnt = 0
                if num == size_elements-1:
                    layout_columns.append(dbc.Col(children=aux,
                                                  className='col-sm-3'))

        layout_columns.append(dbc.Col(children=buttons_layout,
                                      className='col-sm-3'))

        return dbc.Row(layout_columns)

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
        print(self._line_alert.id)
        aux_form = dbc.Form(children=[self._line_alert,
                                      self.split_into_columns(_ly)
                                      # *list(self.others_elements.values()),
                                      # *_ly,
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

