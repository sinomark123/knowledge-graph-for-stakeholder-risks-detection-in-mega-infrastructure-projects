import concurrent.futures
import pandas as pd
from typing import *
import numpy as np
import math

class Node:
  def __init__(self, name, embeddings):
    self.name: str =name
    self.embeddings: np.ndarray = embeddings

  def __call__(self):
    return self.embeddings
  
def embedding_value(dataset, model, col, max_lim=1000, threshold=200):
    lens = max_lim if max_lim > threshold else len(dataset[col])
    output_project = []
    for item in range(0, math.ceil(lens/threshold)):
        centre = dataset[col][item*threshold:(item+1)*threshold if (item+1)*threshold<lens-1 else lens-1]
        print(item, len(centre))
        # Tokenize the input texts
        res = model.encode(centre, batch_size=len(centre), convert_to_numpy=1) # return a numpy vector in threhold * embedding dim shape
        output_project.extend([Node(*new_one) for new_one in zip(centre, [*res])])
    return output_project # use multi-processing next time

def acc(columns: str, col_num: int, df, model, modelFunc: Callable = embedding_value):
    dataset = pd.DataFrame(columns=["name", *[f"embedding_{val}" for val in range(768)]])
    projectRes, newShape = [], 0
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        projectRes = executor.submit(modelFunc, dataset = df, model = model, col=columns[col_num], max_lim=10, threshold=200).result()
    newShape = len(projectRes)
    for items in range(newShape):
        pidx: Node = projectRes[items]
        data = [pidx.name, *pidx.embeddings]
        dataset.loc[items, ] = pd.Series(data, index=dataset.columns)
    return dataset