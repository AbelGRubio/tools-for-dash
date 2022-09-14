import dash_bootstrap_components as dbc
from dash import html


class Switches:

    def __init__(self,
                 label_name: str,
                 item_name: str,
                 value: bool or str,
                 in_row: bool = True,
                 *args, **kwargs):
        self._label_name = label_name
        self._item_name = item_name
        self._value = value
        self._in_row = in_row
        self._check_input()
        self.layout = self._layout()

    def __repr__(self):
        return f'{self._label_name!r}'

    def _check_input(self):
        if type(self._value) == str:
            states_true = ["True", "true"]
            states_false = ["False", "false"]
            if self._value in states_true:
                self._value = True
            elif self._value in states_false:
                self._value = False
            else:
                self._value = True

    def _layout(self):
        if self._in_row:
            switches = dbc.Row(
                [
                    dbc.Label(self._label_name,
                              id="{}-label".format(self._item_name),
                              align="upper",
                              width=2),
                    dbc.Col(
                        dbc.Switch(
                            id="{}".format(self._item_name),
                            value=self._value,
                        ),
                        width=2,
                    ),
                ],
                className="mb-3",
            )
        else:
            switches = html.Div(
                [
                    dbc.Label(self._label_name,
                              id="{}-label".format(self._item_name)),
                    dbc.Checkbox(
                        id="{}".format(self._item_name),
                        value=self._value,
                    ),
                ]
            )

        return switches
