import logging
import random

import dash_bootstrap_components as dbc
from dash import html, Input, Output, callback

from .modal_form import ModalForm


class UpdatePointForm(ModalForm):
    """
    Formulario que tiene un slider para añadir `puntos a observar
    """
    def __init__(self, form_name: str,
                 logger: logging.Logger = None,
                 path: str = None,
                 **kwargs):
        super(UpdatePointForm, self).__init__(form_name=form_name,
                                              logger=logger, path=path,
                                              load=False,
                                              **kwargs)
        self.id_add_point_button = '{}buttonadd_point{}'.format(self._form_name[:self.limit_name],
                                                                str(int(random.random() * 1000)).zfill(3))

        self.click_add_point = 0
        self.add_point_button = self.define_button_add_point()

        self.buttonaccept = None
        self.buttoncancel = None
        self.buttonclear = None
        self.dropdown = None

        self._read_parser_config()
        self._load_elements()
        self.update_elements()
        f = 1

    def _slider_action(self, value):
        return 'You have selected "{}"'.format(value)

    def _add_slider_callback(self):

        slider = None
        slider_p = 'value'
        header = None
        header_p = 'children'

        for _k in self._list_elements:
            if 'slider' in _k:
                slider = _k
            if 'headerc' in _k:
                header = _k

        output_ = Output(component_id=header,
                         component_property=header_p)
        input_c = Input(component_id=slider,
                        component_property=slider_p)

        @callback(
            output_,
            input_c,
            prevent_initial_call=True,
        )
        def function(value):

            return self._slider_action(value)

    def _add_point_action(self, **kwargs):

        name_dropdown = ''
        for _n in kwargs.keys():
            if 'dropdown' in _n:
                name_dropdown = _n
                name_dropdown = name_dropdown.split('.')[0]
                break

        name_slider = ''
        for _n in kwargs.keys():
            if 'slider' in _n:
                name_slider = _n
                name_slider = name_slider.split('.')[0]
                break

        dropdown_options = '{}.options'.format(name_dropdown)
        dropdown_value = '{}.value'.format(name_dropdown)

        kwargs[dropdown_options].append(str(kwargs['{}.value'.format(name_slider)]))
        kwargs[dropdown_options] = list(set(kwargs[dropdown_options]))
        kwargs[dropdown_value] = kwargs[dropdown_options]

        self.response['message'] = 'New point added'
        self.response['open_alert'] = True
        self.response['color_alert'] = 'primary'
        self.response['open_modal'] = True

        for _k in self.response.keys():
            kwargs[_k] = self.response[_k]

        return kwargs

    def _add_add_point_function(self):
        self._buttons_actions['{}add_point'.format(self.nm)] = (self._add_point_action,)
        self.buttons[self.id_add_point_button] = (self.add_point_button, self.click_add_point)

        _b = self.id_add_point_button
        name = self.short_name(_b)
        _p = self._get_property(_b)
        self.inputs_and_states['{}.{}'.format(name, _p)] = Input(component_id=_b,
                                                                 component_property=_p)
        _b = ''
        for _k in self._list_elements:
            if 'dropdown' in _k:
                _b = _k
                break
        name = self.short_name(_b)
        _p = 'options'
        self.inputs_and_states['{}.{}'.format(name, _p)] = Input(component_id=_b,
                                                                 component_property=_p)
        self.outputs['{}.{}'.format(name, _p)] = Output(component_id=_b,
                                                        component_property=_p)

    def _add_extra_element_buttons(self):
        if self.extra_elements:
            for _k in self.extra_elements:
                if 'button' in _k:
                    self.buttons['{}'.format(_k)] = (self.extra_elements[_k]['widget'], 0)
            f = 1

    def update_elements(self):
        values = ['buttonaccept', 'buttoncancel',
                  'buttonclear', 'dropdown']

        for _k in values:
            for _le in self._list_elements.keys():
                if _k in _le:
                    setattr(self, _k, (_le, self._list_elements[_le]))

        f = 1

    def define_button_add_point(self):
        button = dbc.Button('Add point',
                            id=self.id_add_point_button, n_clicks=0)
        return button

    def reload_layout(self, state=True):
        self.splits_elements()
        self._add_extra_element_buttons()

        if self.extra_elements:
            buttons_layout = [self.buttons[_kb][0] for _kb in self.buttons
                              if _kb not in self.extra_elements]
        else:
            buttons_layout = [self.buttons[_kb][0] for _kb in self.buttons]

        extra_elements = self.add_extra_element()

        if self.add_point_button:
            _ly = [html.Div([dbc.Col(children=self.add_point_button),
                             html.Div(children=buttons_layout)
                             ],
                            className='d-flex justify-content-between')]
        else:
            _ly = buttons_layout

        self._layout = dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle(self._title_form),
                                close_button=True),
                dbc.ModalBody([self._line_alert,
                               *list(self.others_elements.values()),
                               ],
                              id=self._body_modal_name),
                dbc.ModalFooter(
                    _ly
                ),
            ],
            id=self.id_modal_name,
            centered=self.centered,
            size=self.size,
            is_open=False,
            keyboard=self.keyboard,
            backdrop=self.backdrop,
            scrollable=self.scrollable,
        )
        self._set_inputs_and_states()
        self._add_open_modal_button()
        self._add_output_open_modal()
        self._add_add_point_function()
        if state:
            self._add_slider_callback()
            self._add_callback()


