import dash_bootstrap_components as dbc
from dash import dcc


class Slider:
    def __init__(self,
                 label_name: str,
                 item_name: str,
                 value: int,
                 max_value: int = 120,
                 min_value: int = 0,
                 *args, **kwargs):
        self._label_name = label_name
        self._item_name = item_name
        if type(value) == list:
            value = value[0]

        if type(value) == str:
            value = int(value)

        self._value = value
        self._max_value = max_value
        self._min_value = min_value
        self.layout = self._layout()

    def __repr__(self):
        return f'{self._label_name!r}'

    def _layout(self):
        slider_layout = dbc.Row(
            [
                dbc.Label(self._label_name,
                          html_for="{}-label".format(self._item_name),
                          width=2),
                dbc.Col(
                    dcc.Slider(self._min_value, self._max_value, 1,
                               value=self._value,
                               id=self._item_name),
                    width=10,
                ),
            ],
            className="mb-3",
        )
        return slider_layout