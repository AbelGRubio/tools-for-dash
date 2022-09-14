import dash_bootstrap_components as dbc
from dash import dcc


def dict_to_multiple_dicts(value: list) -> tuple:
    sel_cmd = "\\sel\\"
    selected = None
    list_dict = None
    value = [vl for vl in value if len(vl) > 0]
    for num, ky in enumerate(value):
        if sel_cmd in ky:
            ky = ky.split(sel_cmd)[0]
            if selected is None:
                selected = []
            selected.append(num + 1)
        _aux_dict = {"label": ky, "value": num + 1}
        if list_dict is None:
            list_dict = [_aux_dict]
        else:
            _aux_list = [_aux_dict]
            list_dict = [*list_dict, *_aux_list]

    return list_dict, selected


class Dropdown:
    def __init__(self,
                 label_name: str,
                 item_name: str,
                 value: list,
                 is_disabled: bool = False,
                 multi: bool = False,
                 *args, **kwargs):
        self._label_name = label_name
        self._item_name = item_name
        self._value = value
        self._is_disabled = is_disabled
        self._multi = multi
        self.layout = self._layout()

    def __repr__(self):
        return f'{self._label_name!r}'

    def _layout(self):
        all_true = False

        if 'multi_true' in self._value:
            self._value = [item for item in self._value if item != 'multi_true']
            self._multi = True
        if 'all_true' in self._value:
            self._value = [item for item in self._value if item != 'all_true']
            all_true = True

        list_dict, select_value = dict_to_multiple_dicts(self._value)

        if list_dict:
            options = [item['label'] for item in list_dict]
            if all_true:
                selected = options
            else:
                if select_value:
                    selected = [item['label'] for num, item in enumerate(list_dict)
                                if (num+1) in select_value]
                    if not self._multi:
                        selected = selected[0]
                else:
                    selected = None
        else:
            options = []
            selected = None

        dropdown = dcc.Dropdown(options=options, multi=self._multi,
                                id="{}".format(self._item_name),
                                disabled=self._is_disabled,
                                value=selected)

        select = dbc.Row(
            [
                dbc.Label(self._label_name,
                          html_for="{}-label".format(self._item_name),
                          width=2),
                dbc.Col(
                    dropdown,
                    width=10,
                ),
            ],
            className="mb-3",
        )
        return select

