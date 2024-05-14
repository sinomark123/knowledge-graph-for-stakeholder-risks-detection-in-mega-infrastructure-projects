""
import pandas as pd
from typing import *
import re
import numpy as np
import matplotlib.pyplot as plt

files = pd.read_csv(r"Generated_Result/10k.csv", sep=";").fillna("None")
obj = files.iloc[:, :3]
for col in obj.columns:
    obj[col] = obj[col].apply(lambda x: np.nan if "none" in x.lower() else x)

sets = obj.values.tolist()
np.isnan(sets[0][-1])
# print(sets[0])

for idx, subset in enumerate(sets):
    subset = [val.split("|") for val in subset if not pd.isnull(val)]
    subset = [item.strip() for yitem in subset for item in yitem]
    sets[idx] = subset

from functools import singledispatch

@singledispatch
def myFunc(marker, val):
    print("This is the default function")

@myFunc.register(float)
def _(marker: float, val: List[str]):
    pattern = r'\b(?:yes|Yes|etc|-?\d+\.\d+|000)\b'
    processed_list = [item for item in val if not re.search(pattern, item)]
    return processed_list

@myFunc.register(int)
def _(marker: int, val: List[str]):
    print(fr"the marker type is {type(marker)}, it will clean the duplicated value.")
    pattern = r'\b(?:yes|Yes|etc|-?\d+\.\d+|000)\b'
    processed_list = [item for item in val if not re.search(pattern, item)]
    return list(set(processed_list))

testing_pattern = r"\b(?:yes|Yes|etc|-?\d+\.\d+|000)\b"
words1, word2, word3, word4 = "here is a pattern owns 1.0 and 2.0", \
                          "here is a pattern owns 1 and 2", \
                          "here is a pattern owns no number",\
                          "000"
for word in [words1, word2, word3, word4]:
    print(re.search(testing_pattern, word))

sets_proper = [myFunc(1.0, val) for val in sets if val ]

import time
from utils import *
from my_fpgrowth import *
if __name__ == "__main__":
    test_set = sets_proper[:1000]
    # time1 = time.time()
    # root = SycNode("root", None)
    # headerTable, root = general_call(sets_proper, 4, root=root)
    # print(f"Time taken is {time.time() - time1}")
    # innerTreeHook(root)
    # innerHeaderTableHook(headerTable)

    time2 = time.time()
    ht, root = fpgrowth(sets_proper, 0.00001, 0.5)
    print(f"Time taken is {time.time() - time2}")
    innerTreeHook(root)




