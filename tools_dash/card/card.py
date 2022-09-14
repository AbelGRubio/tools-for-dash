import configparser
import logging
import random

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc


class CardClass:
    _logger: logging.Logger

    def __init__(self, card_name: str,
                 logger: logging.Logger = None,
                 is_modal: bool = False,
                 slides: dict = None,
                 extra_button: dbc.Button = None):

        self._is_modal = is_modal
        self._extra_button = extra_button
        self._card_name = card_name
        self._slides = slides
        self.id_card_name = '{}{}-card'.format(card_name, str(int(random.random() * 1000)).zfill(3))
        self.generate_slides_list = {}
        self.id_card_slides = {}

        if logger is None:
            from configuration import LOGGER
            self._logger = LOGGER
        else:
            self._logger = logger

        self.layout = None
        self.name_items = []
        self.generate_default_slides()
        self._layout()

    def __repr__(self):
        return f'{self._card_name!r}'

    def __add__(self, other):
        """
        junta las dos cards
        :param other:
        :return:
        """
        pass

    def add_item(self, item: dict):
        """
        añade un nuevo item a la card
        :param item:
        :return:
        """
        pass

    def _empty_card(self):
        """
        vacia la card
        :return:
        """
        self.layout = html.Div(children=[html.H2("Empty form, please fill it")])

    def _get_row_align(self, title: str, button: dbc.Button = None):
        """
        Obtiene una linea con el titulo de la slide
        :param title:
        :param button:
        :return:
        """
        if button:
            return html.Div([html.Div(title),
                             html.Div(button)],
                            className="d-flex justify-content-between")
        else:
            return html.Div([html.Div(title),
                             html.Div(dbc.Button(html.I(className="bi bi-gear-wide-connected")))],
                            className="d-flex justify-content-between")

    def _slide(self, title: str,
               button: dbc.Button = None, fig=None,
               **kwargs):
        """
        Añade una card con sus botones para una grafica
        :param title:
        :param button:
        :param fig:
        :return:
        """
        name_id = '{}_{}-card'.format(title, str(int(random.random() * 1000)).zfill(3))
        return dbc.Card(children=[dbc.CardHeader(self._get_row_align(title, button)),
                                  dbc.CardBody(
                                      fig),
                                  ],
                        id=name_id,
                        )

    def _slide_collapse(self, title: str,
                        button: dbc.Button = None, fig=None,
                        **kwargs):
        """
        Añade una card con sus botones para una grafica
        :param title:
        :param button:
        :param fig:
        :return:
        """
        name_id = '{}_{}-collapse'.format(title, str(int(random.random() * 1000)).zfill(3))
        self.id_card_slides[title] = (name_id, False)
        item = dbc.Collapse(
            dbc.Card(children=[dbc.CardHeader(self._get_row_align(title, button)),
                               dbc.CardBody(fig),
                               ],
                     ),
            id=name_id,
            is_open=True)
        return item

    def generate_default_slides(self):
        self.generate_slides_list = {_k: self._slide_collapse(**self._slides[_k])
                                     for _k in self._slides.keys()}

    def show_hide_slides(self, **kwargs):
        list_to_show = None

        if 'filtdropdowntor.value' in kwargs or 'filtdropdowntom.value' in kwargs:
            if 'show_plot' in self.id_card_name:
                list_to_show = kwargs['filtdropdowntor.value']
            else:
                list_to_show = kwargs['filtdropdowntom.value']

        for _k in self.id_card_slides:
            name, state = self.id_card_slides[_k]
            if _k in list_to_show:
                state = True
            else:
                state = False
            kwargs['{}.is_open'.format(name)] = state
            self.id_card_slides[_k] = (name, state)

        return kwargs

    def generate_slides(self):
        list_slides = []

        if len(self._slides.keys()) > 0:
            for _k in self._slides:
                list_slides.append(self.generate_slides_list[_k])

        return list_slides

    def update_layout(self,
                      dict_slides: dict = None
                      ):
        self._slides = dict_slides

        style = {"margin-left": "10px",
                 "overflow": "scroll",
                 "max-height": "1200px"}

        self.layout = dbc.Card(children=self.generate_slides(),
                               style=style,
                               id=self.id_card_name)

    def _layout(self):
        """
        devuelve el layout del formulario
        :return:
        """

        style = {"margin-left": "10px",
                 "margin-bottom": "10px",
                 "overflow": "scroll",
                 "max-height": "1200px"}

        self.layout = dbc.Card(children=self.generate_slides(),
                               style=style,
                               id=self.id_card_name)


def short_name(name: str):
    name_split = name.split('_')
    return ''.join([nm[:1] for nm in name_split])

