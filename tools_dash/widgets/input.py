import dash_bootstrap_components as dbc

modes = ['text', 'number', 'time']


class ErrorMode(Exception):
    def __init__(self):
        self.message = f'Please select one of this modes: {modes}'

    def __str__(self):
        return self.message


class InputWidget:
    def __init__(self,
                 label_name: str,
                 item_name: str,
                 value: str,
                 input_type: str = 'text',
                 floating_label: bool = False,
                 *args, **kwargs):
        self._label_name = label_name
        self._item_name = item_name
        self._value = value
        self._input_type = input_type
        self._floating_label = floating_label
        self._check_input()
        self.layout = self._layout()

    def __repr__(self):
        return f'{self._label_name!r}'

    def _check_input(self):
        if type(self._value) == list:
            self._value = self._value[0]

        if self._input_type not in modes:
            raise ErrorMode

    def _get_input(self):
        switch = {
            'time': dbc.Input(type="time",
                              id="{}".format(self._item_name),
                              min="00:00", max="23:59",
                              value=self._value,),
            'text': dbc.Input(type="text",
                              id="{}".format(self._item_name),
                              placeholder="Enter value",
                              value=self._value, ),
            'number': dbc.Input(type="number",
                                id="{}".format(self._item_name),
                                value=self._value,)
        }
        return switch[self._input_type]

    def _layout(self):
        if self._floating_label:
            line_input = dbc.FormFloating(
                [
                    self._get_input(),
                    dbc.Label(self._label_name),
                ]
            )
        else:
            line_input = dbc.Row(
                [
                    dbc.Label(self._label_name,
                              html_for="{}-label".format(self._item_name),
                              width=2),
                    dbc.Col(
                        self._get_input(),
                        width=10,
                    ),
                ],
                className="mb-3",
            )
        return line_input
