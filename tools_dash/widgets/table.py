import pandas as pd
from dash import html, dash_table
import random


class Table:
    def __init__(self, only_table=False):
        self._only_table = only_table
        self.layout_table, self.table_name = None, None
        self._load_table()

    def _load_table(self):
        df_all = pd.read_csv(
            r'logEvents_2022_07_29.txt',
            sep='\t')
        df = df_all[df_all['id'] == 1252627563]
        style = {
        "overflow-x": "scroll",
        "background": "ivory"}

        self.table_name = 'table{}'.format(str(int(random.random() * 1000)).zfill(3))

        self.layout_table = html.Div(children=dash_table.DataTable(df.to_dict('records'),
                                                              [{"name": i, "id": i} for i in df.columns],
                                                              id=self.table_name ),
                                style=style,
                                )
        if self._only_table:
            self.layout_table = dash_table.DataTable(df.to_dict('records'),
                                                [{"name": i, "id": i} for i in df.columns],
                                                id=self.table_name )

        return self.layout_table, self.table_name
