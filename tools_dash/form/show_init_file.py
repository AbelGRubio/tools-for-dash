import logging
import random

import dash_bootstrap_components as dbc
from dash import html

from .form_interface import FormInterface
from .functions import generate_form_from_parser


class ShowInitFile(FormInterface):
    """
    Muestra los archivos .ini en un formulario
    """
    def __init__(self, form_name: str,
                 logger: logging.Logger = None,
                 path: str = None,
                 **kwargs):
        super(ShowInitFile, self).__init__(form_name=form_name,
                                           logger=logger, path=path,
                                           load=False, **kwargs)

        self.custom_name_path = kwargs['custom_name_path']
        self.id_form = '{}-{}-{}formname'.format(self.custom_name_path,
                                                 self.form_name,
                                                 str(int(random.random() * 1000)).zfill(3))
        self._read_parser_config()
        self._load_elements()

    @staticmethod
    def _get_property(component_id: str):
        property_name = 'value'

        if 'date' in component_id:
            property_name = 'date'
        elif 'button' in component_id:
            property_name = 'n_clicks'
        elif 'title' in component_id:
            property_name = 'children'

        return property_name

    def _load_elements(self):
        self._parser_config['button'] = {'accept': '',
                                         'cancel': ''}
        self._list_elements = generate_form_from_parser(self.form_name[:self.limit_name],
                                                        self._parser_config,
                                                        all_text=True)

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

        title_ = 'Mostrando path: {} y el archivo: {}'.format(self.custom_name_path,
                                                              self.form_name)

        self._layout = dbc.Collapse(children=[html.H2(title_),
                                              *list(self.others_elements.values()),
                                              self._line_alert,
                                              *_ly,
                                              ],
                                    style=self._style,
                                    is_open=False,
                                    id=self.id_form)
        self._set_inputs_and_states()
        if state:
            self._add_callback()

