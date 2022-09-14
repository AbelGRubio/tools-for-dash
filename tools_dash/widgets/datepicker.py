import datetime

import dash_bootstrap_components as dbc
from dash import dcc


class DatePicker:

    def __init__(self,
                 label_name: str,
                 item_name: str,
                 value,
                 *args, **kwargs):
        self._label_name = label_name
        self._item_name = item_name
        self._value = value
        self.layout = self._layout()

    def __repr__(self):
        return f'{self._label_name!r}'

    def _layout(self):
        today = str(datetime.date.today())
        select = dbc.Row(
            [
                dbc.Label(self._label_name,
                          html_for="{}-label".format(self._item_name),
                          width=2),
                dbc.Col(
                    dcc.DatePickerSingle(
                        id='{}'.format(self._item_name),
                        min_date_allowed=datetime.date(1995, 8, 5),
                        initial_visible_month=today,
                        date=datetime.date.today()
                    ),
                ),
            ],
            className="mb-3",
        )
        return select

