from random import choice
from reportlab.lib.colors import HexColor


def get_random_colors(no_colors):
    # generate random hexa
    colors_list = []
    for i in range(no_colors):
        color = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colors_list.append(HexColor('#'+color))
    return colors_list


def get_percentage(values):
    total = sum(values)
    percentage = []
    for value in values:
        v = round(value*100.0/total, 2)
        percentage.append(str(v)+" %")
    return percentage