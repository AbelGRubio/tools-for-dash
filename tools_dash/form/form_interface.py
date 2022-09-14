"""
    Interface creada para clase formulario donde se registran algunas propiedades comunes
    a todos los formularios

"""
import datetime
import logging
import os

import dash_bootstrap_components as dbc
from dash import State, Input, Output, callback

from .functions import *


class TypeStruct(Exception):
    """
    Custom exception para indicar que lo añadido no es correcto.
    """
    def __init__(self):
        self.message = f'Type struct incorrect. Should be a dict with key as argument and the ' \
                       f'value has to be a layout'

    def __str__(self):
        return self.message


class FormInterface:
    """
    Class form where you can find some properties and funtionality defined here

    ** _logger: is used to define the logger

    This attribute only have to be defined one time
    """
    _logger: logging.Logger = None,

    def __init__(self, form_name: str,
                 logger: logging.Logger = None,
                 path: str = None,
                 buttons_actions: dict = None,
                 extra_elements: dict = None,
                 load: bool = True,
                 **kwargs):
        """

        :param form_name: this name have to be equal to the file .ini on the folder
            assets/forms

         Nombre del formulario, tiene que ser igual que el archivo .ini que hay en la carpeta
            no ha de incluirse .ini. Este nombre se utiliza para poner titulo a formulario. Los espacios _ los
            sustituye por espacios en blanco.
        :param logger:
        :param path: where you type
        :param buttons_actions: diccionario para indicar otras acciones que han de hacer los botones
        :param extra_elements: elementos extra a tener en cuenta para realizar las acciones
        :param load: sirve para indicar si hay que cargar el .ini o no
        :param kwargs:
        """
        self._form_name = form_name
        self.form_name = form_name
        self.limit_name = 4
        self.nm = self.form_name[:self.limit_name]

        self._list_elements = {}
        self._buttons_actions = None
        self._element_actions = {}
        self.define_buttons_actions(buttons_actions)
        self._layout = None
        self._style = {"margin": "10px"}
        self.others_elements = {}
        self.buttons = {}
        self.outputs = {}
        self.states = {}
        self.inputs_and_states = {}
        self._element_past_values = {}
        self.extra_elements = extra_elements

        if logger is None:
            from configuration import LOGGER
            self.__class__._logger = LOGGER
        else:
            if type(self.__class__._logger) is tuple:
                self.__class__._logger = logger

        self.id_form = '{}{}formname'.format(self.form_name,
                                             str(int(random.random() * 1000)).zfill(3))
        self._title_form = self._form_name.replace('_', ' ').capitalize()

        """definicion del mensaje de alert"""
        self._alert_name = '{}{}-alert'.format(self.form_name,
                                               str(int(random.random() * 1000)).zfill(3))
        self._line_alert = dbc.Alert(children="", color="success",
                                     id=self._alert_name, is_open=False,
                                     dismissable=True,
                                     duration=4000)

        if path is None:
            self._path = r'assets\forms'
            self.basename_path = r'assets'
        else:
            self._path = path
            self.basename_path = os.path.basename(path)
        self._parser_config = configparser.ConfigParser()
        if load:
            self._read_parser_config()
            self._load_elements()
        self.response = {}

    def __copy__(self) -> NotImplemented:
        """
        Copia del formulario

        TODO: hay que implementar correctamente los métodos
         __radd__, __copy__ y __add__
        :return:
        """
        class_type = type(self)
        return class_type(form_name=self.form_name,
                          logger=self._logger)

    def __radd__(self, other) -> NotImplemented:
        """
        para cuando sumemos un dictionario con nuevos items
        y hacer control de los items que entran
        """
        if type(other) == dict:
            _add_list_generators = dict(**self._list_elements,
                                        **other._list_elements)
            self.reload_layout()
        else:
            raise TypeStruct()

    def __add__(self, other: dict) -> NotImplemented:
        """
        Para cuando sumemos dos formularios difentes, por si queremos juntarlos
        :param other
        :return:
        """
        aux = {}
        for _k in other.keys():
            if other[_k][0]:
                aux[_k] = other[_k][1]
        _add_list_generators = dict(**self._list_elements, **aux)
        self._list_elements = _add_list_generators
        self.reload_layout(False)
        return self

    def copy(self) -> NotImplemented:
        return self.__copy__()

    @property
    def layout(self):
        """
        Getter para la variable layout, se ejecutará una vez terminado de añadir
        todos los elementos que queremos controlar
        :return:
        """
        if self._layout is None:
            self.reload_layout()

        return self._layout

    @staticmethod
    def _get_property(component_id: str):
        """
        TODO: hacer el cambio a diccionario
        :param component_id: obtiene la propiedad que interesa
        :return:
        """
        property_name = 'value'

        if 'date' in component_id:
            property_name = 'date'
        elif 'button' in component_id:
            property_name = 'n_clicks'

        return property_name

    def _load_elements(self):
        """
        Carga todos los elementos leidos desde el parser.
        :return:
        """
        self._list_elements = generate_form_from_parser(self.form_name[:self.limit_name],
                                                        self._parser_config)

    def _load_path_file(self, filename: str = None):
        """
        Crea la ruta donde se encuentra el archivo .ini para cargar
        :param filename: nombre del archivo
        :return:
        """
        if not filename:
            filename = self.form_name
        self.load_path_file = os.path.join(self._path, '.'.join([filename, 'ini']))
        return self.load_path_file

    def _read_parser_config(self, filename: str = None):
        """
        lee el parser
        :param filename: nombre del archivo a leer
        :return:
        """
        _path_file = self._load_path_file(filename)
        if os.path.exists(_path_file):
            self._parser_config.clear()
            self._parser_config.read(_path_file)
            self._logger.info('Reader parser .ini from {}'.format(_path_file))
        else:
            self._logger.warning("No file .ini in folder.")

    def _get_pressed_button(self, **kwargs) -> str:
        """
        Obtiene el boton que se ha pulsado, esta funcion se utiliza para saber qué acción
        hay que ejecutar despues
        :param kwargs: argumentos variables que corresponden con los items que se estan
            controlando

        :return:
        """
        buttons_clicks_past = dict([(self.short_name(_k), self.buttons[_k][1]) for _k in self.buttons])
        buttons_click_new = dict([(_k, kwargs[_k]) for _k in kwargs if 'button' in _k])

        name = ''
        for _o, _n in zip(buttons_clicks_past, buttons_click_new):
            if _o in _n:
                if buttons_clicks_past[_o] != buttons_click_new[_n]:
                    name = _o.replace('button', '')
                    new_click_state = buttons_click_new[_n]
                    for _b in self.buttons:
                        if self.short_name(_b) in _n:
                            self.buttons[_b] = (self.buttons[_b][0], new_click_state)
                            break
                    break
        #
        if name == '':
            """por si cambia algun valor en los items y hay que hacer algo"""
            for _k in self._element_past_values:
                if self._element_past_values[_k] != kwargs[_k]:
                    name = _k
                    break

        return name

    def _clear_form(self, **kwargs):
        """
        Función para limpiar el formulario

        :param kwargs: argumentos variables que corresponden con los items que se estan
            controlando

        :return:
        """

        _switch = {'date': datetime.datetime.today(),
                   'switch': False,
                   'dropdown': None}

        for _ke in kwargs:  # :self._list_elements.keys():
            if 'button' not in _ke:
                value = ''
                _bool_switch = [sn in _ke for sn in _switch.keys()]
                if any(_bool_switch):
                    _opt_switch = [k for k, s in zip(_switch.keys(), _bool_switch) if s][0]
                    value = _switch[_opt_switch]
                    if _ke.endswith('.options'):
                        value = []

                kwargs[_ke] = value

        self.response['message'] = 'Ha limpiado el modal'
        self.response['open_alert'] = True
        self.response['color_alert'] = 'warning'

        for _k in self.response.keys():
            kwargs[_k] = self.response[_k]

        return kwargs

    def _cancel_form(self, **kwargs):
        """
        Función para cancelar el formulario
        :param kwargs: argumentos variables que corresponden con los items que se estan
            controlando
        :return:
        """
        self.response['message'] = 'Ha cancelado el modal'
        self.response['open_alert'] = True
        self.response['color_alert'] = 'danger'

        for _k in self.response.keys():
            kwargs[_k] = self.response[_k]

        return kwargs

    def _accept_form(self, **kwargs):
        """
        Función para aceptar el formulario

        :param kwargs: argumentos variables que corresponden con los items que se estan
            controlando
        :return:
        """
        self.response['message'] = 'Ha aceptado el modal'
        self.response['open_alert'] = True
        self.response['color_alert'] = 'success'

        for _k in self.response.keys():
            kwargs[_k] = self.response[_k]

        return kwargs

    def _action_button(self, **kwargs):
        """
        Ejecuta la accion correspondiente al boton

        :param kwargs: argumentos variables que corresponden con los items que se estan
            controlando

        :return:
        """
        pressed_button = self._get_pressed_button(**kwargs)
        print('modal: {} pressed button is {}'.format(self.nm,
                                                      pressed_button))
        if pressed_button in self._buttons_actions.keys():
            for _fun in self._buttons_actions[pressed_button]:
                kwargs = _fun(**kwargs)

        if pressed_button in self._element_actions.keys():
            for _fun in self._element_actions[pressed_button]:
                kwargs = _fun(**kwargs)

        if pressed_button == '':
            """ para evitar las llamadas vacias """
            self.response['open_modal'] = False
            for _k in self.response:
                kwargs[_k] = self.response[_k]

        response = []
        for _k in self.outputs.keys():
            response.append(kwargs[_k])

        return response

    def _get_inputs(self, dict_values: dict = None):
        """
        obtiene los imputs
        :param dict_values:
        :return:
        """
        aux = self.buttons
        if dict_values:
            aux = dict_values

        inputs = {}
        for _b in aux:
            name = self.short_name(_b)
            _p = self._get_property(_b)
            inputs['{}.{}'.format(name, _p)] = Input(component_id=_b,
                                                     component_property=_p)
        return inputs

    def _get_states(self, dict_values: dict = None):
        """
        Obtiene los states
        :param dict_values:
        :return:
        """
        aux = self.others_elements
        if dict_values:
            aux = dict_values

        self.states = {}
        for _b in aux:
            name = self.short_name(_b)
            _p = self._get_property(_b)
            self.states['{}.{}'.format(name, _p)] = State(component_id=_b,
                                                          component_property=_p)
        return self.states

    def _get_outputs(self, dict_values: dict = None):
        """
        Obtiene los ouputs
        :param dict_values:
        :return:
        """
        if len(self.outputs) > 0:
            aux = {'message': Output(component_id=self._alert_name,
                                     component_property="children"),
                   'open_alert': Output(component_id=self._alert_name,
                                        component_property="is_open"),
                   'color_alert': Output(component_id=self._alert_name,
                                         component_property="color")}
            for _k in self.outputs.keys():
                aux[_k] = self.outputs[_k]
            self.outputs = aux
        else:
            self.outputs = {'message': Output(component_id=self._alert_name,
                                              component_property="children"),
                            'open_alert': Output(component_id=self._alert_name,
                                                 component_property="is_open"),
                            'color_alert': Output(component_id=self._alert_name,
                                                  component_property="color")}

        self.response = {
            'message': '',
            'open_alert': False,
            'color_alert': 'success'
        }

        if dict_values:
            for _b in dict_values:
                component_id = dict_values[_b].component_id
                short_id = self.short_name(component_id)
                _p = self._get_property(_b)
                self.outputs['{}.{}'.format(short_id, _p)] = Output(component_id=component_id,
                                                                    component_property=_p)

        return self.outputs

    def _set_inputs_and_states(self):
        """
        Obtiene los imputs and states para ponerlos en el callback
        :return:
        """
        inputs_dict = self._get_inputs()
        states_dict = self._get_states()
        self._get_outputs(states_dict)

        if len(self.inputs_and_states) > 0:
            """
            para gestionar si se ha asignado una custom function a un valor
            """
            aux = dict(**inputs_dict, **states_dict)
            for _k in self.inputs_and_states.keys():
                aux[_k] = self.inputs_and_states[_k]
            self.inputs_and_states = aux
        else:
            self.inputs_and_states = dict(**inputs_dict, **states_dict)

    def splits_elements(self) -> None:
        """
        Divide los elementos que carga el .ini entre botones y los demás elementos
        :return: 
        """
        self.buttons = {}
        self.others_elements = {}

        for _k in self._list_elements:
            if 'button' in _k:
                self.buttons[_k] = (self._list_elements[_k], 0)
            else:
                self.others_elements[_k] = self._list_elements[_k]

    def add_extra_element(self):
        """
        Añade los elementos extra al formualrio
        :return:
        """
        extra_elements = []
        if self.extra_elements:
            for _ee in self.extra_elements:
                _e = self.extra_elements[_ee]

                if _e['show']:
                    extra_elements.append(_e['widget'])

                if 'button' in _ee:
                    name = self.short_name(_ee.replace('button', ''))
                    # print(name)
                    if 'clear' in _e:
                        if name not in self._buttons_actions:
                            self._buttons_actions[name] = [self.add_default_response, ]
                        for _fun in _e['clear']:
                            self._buttons_actions[name].append(_fun)
                    if 'accept' in _e:
                        if _ee not in self._buttons_actions:
                            self._buttons_actions[name] = [self.add_default_response, ]
                        for _fun in _e['accept']:
                            self._buttons_actions[name].append(_fun)
                    continue

                if 'input' in _e:
                    for _p in _e['input']:
                        name = '{}.{}'.format(_ee, _p)
                        self.inputs_and_states[name] = Input(component_id=_ee,
                                                             component_property=_p)

                if 'state' in _e:
                    for _p in _e['state']:
                        name = '{}.{}'.format(_ee, _p)
                        self.inputs_and_states[name] = State(component_id=_ee,
                                                             component_property=_p)

                if 'output' in _e:
                    for _p in _e['output']:
                        name = '{}.{}'.format(_ee, _p)
                        self.outputs[name] = Output(component_id=_ee,
                                                    component_property=_p)

                if 'clear' in _e:
                    for _fun in _e['clear']:
                        self._buttons_actions['{}clear'.format(self.nm)].append(_fun)
                if 'accept' in _e:
                    for _fun in _e['accept']:
                        self._buttons_actions['{}accept'.format(self.nm)].append(_fun)

                f = 1

        return extra_elements

    def short_name(self, name: str):
        return name[:-3]

    def set_kwarg_to_args(self, *args) -> dict:
        """
        Obtain the kwargs associated to args
        :param args:
        :return:
        """
        kwargs = {}
        for _e, _k in zip(args, list(self.inputs_and_states.keys())):
            kwargs[_k] = _e
        return kwargs

    def find_id_item(self, item_name: str):
        """
        Find the first item which name similar to item_name
        :param item_name:
        :return:
        """
        id_name = '{}{}'.format(self.form_name[:self.limit_name],
                                item_name)
        id_element = None
        for _k in self._list_elements.keys():
            if id_name in _k:
                id_element = _k
                break

        return id_element

    def reload_layout(self, state: bool = True):
        """
        layout creation
        :param state: boolean for add the callback or not
        :return:
        """
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

        self._layout = dbc.Form(children=[html.H2(self._title_form),
                                          self._line_alert,
                                          *list(self.others_elements.values()),
                                          *_ly,
                                          ],
                                style=self._style,
                                id=self.id_form)
        self._set_inputs_and_states()
        if state:
            self._add_callback()

    def define_buttons_actions(self, buttons_actions: dict) -> None:
        """
        Se definen las funciones que van a realizar los botones
        :param buttons_actions: diccionario para añadir las buttons_actions extras que se indiquen 
            al instanciar la clase
        :return:
        """
        self._buttons_actions = {'{}accept'.format(self.nm): [self._accept_form, ],
                                 '{}clear'.format(self.nm): [self._clear_form, ],
                                 '{}cancel'.format(self.nm): [self._cancel_form, ]}
        keys_ba = list(self._buttons_actions.keys())
        if buttons_actions:
            for _kba in buttons_actions:
                for _kaction in keys_ba:
                    if _kba in _kaction:
                        for _fun in buttons_actions[_kba]:
                            self._buttons_actions[_kaction].insert(0, _fun)

    def add_default_response(self, **kwargs):
        """
        Add default arguments
        :param kwargs:
        :return:
        """
        self.response['message'] = ''
        self.response['open_alert'] = False
        self.response['color_alert'] = 'success'

        for _k in self.response.keys():
            kwargs[_k] = self.response[_k]

        return kwargs

    def add_custom_action_to_item(self, id_in_item: str,
                                  in_property: str = None,
                                  id_out_item: str = None,
                                  out_property: str = None,
                                  fun_item=None):
        """
        Add a custom action to an item
        :param id_in_item:
        :param in_property:
        :param id_out_item:
        :param out_property:
        :param fun_item:
        :return:
        """
        id_in_element = self.find_id_item(id_in_item)

        id_out_element = self.find_id_item(id_out_item)

        if id_out_element and id_in_element:
            out_name_property = '{}.{}'.format(self.short_name(id_out_element), out_property)
            if out_name_property not in self.outputs.keys():
                self.outputs[out_name_property] = Output(component_id=id_out_element,
                                                         component_property=out_property)
                self.inputs_and_states[out_name_property] = State(component_id=id_out_element,
                                                                  component_property=out_property)

            abrev = self.short_name(id_in_element)
            _p = self._get_property(in_property)
            abrev = '{}.{}'.format(abrev, _p)
            self.inputs_and_states[abrev] = Input(component_id=id_in_element,
                                                  component_property=_p)

            self._element_actions[abrev] = [fun_item, self.add_default_response, ]
            self._element_past_values[abrev] = str(datetime.date.today())

    def _add_callback(self):
        """
        add the callback to the form
        :return:
        """
        @callback(
            list(self.outputs.values()),
            list(self.inputs_and_states.values()),
            prevent_initial_call=True,
        )
        def function(*args, **kwargs):

            fun_kwargs = self.set_kwarg_to_args(*args)

            response = self._action_button(**fun_kwargs)

            return response

