import logging
import random

import dash_bootstrap_components as dbc
from dash import html, Input, Output

from .form_interface import FormInterface


class ModalForm(FormInterface):
    """
    Abre un modal con el formulario
    """
    __slots__ = ['id_modal_name', '_body_modal_name',
                 'size', 'scrollable', 'keyboard',
                 'backdrop', 'centered', 'button_name',
                 'id_open_modal_button', 'open_modal_button']

    def __init__(self, form_name: str,
                 logger: logging.Logger = None,
                 path: str = None,
                 **kwargs):
        action_open_modal = self.get_open_modal_action(**kwargs)

        super(ModalForm, self).__init__(form_name=form_name,
                                        logger=logger, path=path, **kwargs)

        if action_open_modal:
            self._add_open_modal_action(action_open_modal)

        self.id_modal_name = '{}{}'.format(self.form_name,
                                           str(int(random.random() * 1000)).zfill(3))
        self._body_modal_name = '{}{}-alert'.format(self.form_name,
                                                    str(int(random.random() * 1000)).zfill(3))
        self.id_open_modal_button = '{}buttonopen_modal{}'.format(self.nm,
                                                                  str(int(random.random() * 1000)).zfill(3))

        self.open_modal_button = None
        self.default_parameters()
        self.read_kwargs(**kwargs)
        self._update_actions()

    def _add_open_modal_action(self, functions: list):
        """
        añade las funciones al abrir el open modal
        :param functions: lista de funciones a añadir
        :return:
        """
        self._buttons_actions['{}open_modal'.format(self.nm)] = functions

    def _add_open_modal_button(self):
        """
        crea el boton open modal y lo añade a la lista de inputs y states
        :return:
        """
        if self.button_name:
            self.open_modal_button = dbc.Button(self.button_name,
                                                id=self.id_open_modal_button, n_clicks=0,
                                                className='open_modal_button1')
        else:
            self.open_modal_button = dbc.Button(html.I(className="bi bi-gear-wide-connected"),
                                                id=self.id_open_modal_button, n_clicks=0,
                                                className='open_modal_button1')
        self.buttons[self.id_open_modal_button] = (self.open_modal_button, 0)

        _p = self._get_property(self.id_open_modal_button)
        name = '{}{}.{}'.format(self.nm,
                                self.id_open_modal_button,
                              _p)
        self.inputs_and_states[name] = Input(component_id=self.id_open_modal_button,
                                             component_property=_p)

    def _update_actions(self):
        """
        Actualiza las acciones asociadas a los botones
        :return:
        """
        if '{}open_modal'.format(self.nm) in self._buttons_actions.keys():
            self._buttons_actions['{}open_modal'.format(self.nm)].append(self._open_modal)
        else:
            self._buttons_actions['{}open_modal'.format(self.nm)] = [self._open_modal, ]
        self._buttons_actions['{}accept'.format(self.nm)].append(self._accept_form_modal)
        self._buttons_actions['{}clear'.format(self.nm)].append(self._clear_form_modal)
        self._buttons_actions['{}cancel'.format(self.nm)].append(self._cancel_form_modal)

    @staticmethod
    def _accept_form_modal(**kwargs):
        """
        Acción que se ejecuta al aceptar el form

        :param kwargs: argumentos variables que corresponden con los items que se estan
            controlando

        :return:
        """
        kwargs['open_modal'] = False
        return kwargs

    @staticmethod
    def _clear_form_modal(**kwargs):
        """
        Acción que se ejecuta al limpiar el form

        :param kwargs: argumentos variables que corresponden con los items que se estan
            controlando

        :return:
        """
        kwargs['open_modal'] = True
        return kwargs

    @staticmethod
    def _cancel_form_modal(**kwargs):
        """
        Acción que se ejecuta al cancelar el form

        :param kwargs: argumentos variables que corresponden con los items que se estan
            controlando

        :return:
        """
        kwargs['open_modal'] = False
        return kwargs

    def _open_modal(self, **kwargs):
        """
        :param kwargs: argumentos variables que corresponden con los items que se estan
            controlando

        :return:
        """
        self.response['message'] = 'Ha abierto el modal'
        self.response['open_alert'] = True
        self.response['color_alert'] = 'primary'
        self.response['open_modal'] = True

        for _k in self.response.keys():
            kwargs[_k] = self.response[_k]

        return kwargs

    def _add_output_open_modal(self):
        """
        Añade el boton de open modal a los outputs
        :return:
        """
        self.outputs['open_modal'] = Output(component_id=self.id_modal_name,
                                            component_property="is_open")
        self.response['open_modal'] = False

    @staticmethod
    def get_open_modal_action(**kwargs):
        """
        :param kwargs: argumentos variables que corresponden con los items que se estan
            controlando

        :return:
        """
        aux = None
        if 'buttons_actions' in kwargs.keys():
            if 'open_modal' in kwargs['buttons_actions']:
                aux = kwargs['buttons_actions']['open_modal']
        return aux

    def default_parameters(self):
        """
        Pasea los kwargs de entrada para la clase modal y añade los parametros por default
        :return:
        """
        default_values = {
            'size': 'lg',
            'scrollable': True,
            'keyboard': False,
            'backdrop': 'static',
            'centered': True,
            'button_name': None
        }
        self.read_kwargs(**default_values)

    def read_kwargs(self, **kwargs):
        """

        :param kwargs: argumentos variables que corresponden con los items que se estan
            controlando

        :return:
        """
        for key in self.__slots__:
            if key in kwargs:
                setattr(self, key, kwargs[key])

    def reload_layout(self, state=True):
        self.splits_elements()

        buttons_layout = [_b[0] for _b in self.buttons.values()]
        extra_elements = self.add_extra_element()

        self._layout = dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle(self._title_form),
                                close_button=True),
                dbc.ModalBody([self._line_alert,
                               *list(self.others_elements.values()),
                               *extra_elements],
                              id=self._body_modal_name),
                dbc.ModalFooter(
                    buttons_layout
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
        if state:
            self._add_callback()


