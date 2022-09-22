import random


def define_id(pre_id: str = '',
              widget_type: str = '',
              extra: str = '',
              number_of_digits: int = 5) -> str:
    """
    Create a unique id for the widgets

    :param pre_id:
    :param extra:
    :param widget_type:
    :param number_of_digits:

    :return:
    """
    max_number = int('1' + '0' * number_of_digits)

    random_number = str(int(random.random() * max_number)).zfill(number_of_digits)

    return '{}{}{}{}'.format(pre_id, extra, widget_type, random_number)


def short_id(id_widget: str = '', number_of_digits: int = 5):
    return id_widget[:-number_of_digits]





