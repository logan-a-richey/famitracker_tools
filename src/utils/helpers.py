# helpers.py

from typing import List, Tuple

def get_token_key(pattern: int, row: int, col: int) -> Tuple[int, int, int]:
    ''' Generate key for Track.tokens dictionary '''
    #return "PAT={}::ROW={}::COL={}".format(pattern, row, col)
    res = tuple([pattern, row, col])
    return res

def get_next_item(item: int, lst: List[int]) -> int:
    ''' get the next item of a lst, given an input item. Used to find the next order. '''

    if item not in lst:
        raise ValueError("Item {} not in List {}".format(item, lst))
    idx = lst.index(item)
    ndx = (idx + 1) % len(lst)
    return lst[ndx]

def generate_macro_label(chip: str, macro_type: int, macro_index: int) -> str:
    valid_chips = ["MACRO", "MACROVRC6", "MACRON163", "MACROSB5"]
    valid_macro_types = [i for i in range(5)]
    
    if chip not in valid_chips:
        raise ValueError("{} is not in valid_chips: {}".format(chip, valid_chips))
    if macro_type not in valid_macro_types:
        raise ValueError("{} is not in valid_chips: {}".format(macro_type, valid_macro_types))

    return "{}.{}.{}".format(chip, macro_type, macro_index)

