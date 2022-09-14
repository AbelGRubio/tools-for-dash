from dash import html


class Header2:
    def __init__(self,
                 label_name: str,
                 item_name: str,
                 value: list,
                 *args, **kwargs):
        self._label_name = label_name
        self._item_name = item_name
        self._value = value
        self.layout = self._layout()

    def __repr__(self):
        return f'{self._label_name!r}'

    def _layout(self):
        line_input = html.H2(children=self._value,
                             id=self._item_name)
        return line_input

