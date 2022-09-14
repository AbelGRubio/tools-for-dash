import configparser

from dash import html

from tools_dash.functions import define_id
from tools_dash.widgets import *


def get_values(parameter: str):

    splitted = parameter.replace(' ', '')
    val_parameter = splitted.split(';')

    return val_parameter


def short_name(name: str):
    name_split = name.split('_')
    return ''.join([nm[:1] for nm in name_split])


def generate_form_from_parser(pre_name: str,
                              reader_config: configparser.ConfigParser,
                              all_text: bool = False) -> dict:
    """
    Genera los elementos que se van a incluir en el formulario
    :param pre_name: es el prefijo que se va a añadir a los elementos del formualrio
    :param reader_config: es el parser del .ini leido
    :param all_text: sirve para indicar que tipo de .ini hay que mostrar
    :return: generators and inputs for callbacks
    """
    list_elements = {}

    generators_fun = {
        'dropdown': Dropdown,
        'switch': Switches,
        'text': InputWidget,
        'number': InputWidget,
        'button': generate_button,
        'date': DatePicker,
        'time': InputWidget,
        'slider': Slider,
        'header': Header2,
    }

    # cnt = 1
    for _k in list(reader_config.keys()):
        if _k not in ['DEFAULT', 'Struct_form']:
            first_time = True
            for _kk in reader_config[_k].keys():
                _vv = reader_config[_k][_kk]
                para_val = get_values(_vv)
                name = _kk.replace('_', ' ').capitalize()
                if all_text and first_time and _k != 'button':
                    id_values = define_id(pre_id=pre_name,
                                          widget_type='title',
                                          extra=_k)
                    name_title = _k.replace('_', ' ').capitalize()
                    element_value = html.H2('{}'.format(name_title), id=id_values)
                    list_elements[id_values] = element_value
                    first_time = False

                if all_text:
                    id_values = define_id(pre_id=pre_name,
                                          widget_type=_k,
                                          extra=_kk)
                    type_generator = 'button'
                    if _k != 'button':
                        type_generator = 'text'
                        id_values = define_id(pre_id=pre_name,
                                              widget_type=type_generator,
                                              extra=short_name(_kk))

                    kwargs = {'input_type': type_generator}
                    element_value = generators_fun[type_generator](label_name=name,
                                                                   item_name=id_values,
                                                                   value=para_val, **kwargs)
                    if type_generator != 'button':
                        element_value = element_value.layout

                else:
                    id_values = define_id(pre_id=pre_name,
                                          widget_type=_k,
                                          extra=_kk)
                    if _k != 'button':
                        id_values = define_id(pre_id=pre_name,
                                              widget_type=_k,
                                              extra=short_name(_kk))

                    if _k == 'number':
                        if para_val[0] == '':
                            para_val = para_val[0]
                        else:
                            para_val = float(para_val[0])

                    if _k == 'header':
                        para_val = _vv

                    kwargs = {'input_type': _k}
                    element_value = generators_fun[_k](label_name=name,
                                                       item_name=id_values,
                                                       value=para_val, **kwargs)
                    if _k != 'button':
                        element_value = element_value.layout

                list_elements[id_values] = element_value

    return list_elements
