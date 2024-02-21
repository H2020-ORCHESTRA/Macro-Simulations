"""utils"""

from helpers import *
import typing


def list_to_string(list_int: typing.List[int], separator: str = ",") -> str:
    if len(list_int):
        string_list = separator.join(str(l) for l in list_int)
    else:
        string_list = ""

    return string_list


def string_to_list(string: str, separator: str = ",") -> typing.List[int]:
    if string:
        list_str = string.split(separator)
        list_int = [int(l) for l in list_str]
    else:
        list_int = []
        
    return list_int