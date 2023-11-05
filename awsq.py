import time
import pandas as pd
from collections import Counter

def pop_tags():
    counter = Counter()

    with pd.read_json("/Users/gianluca/Desktop/magistrale/primo anno/Primo semestre/Algorithmic methods/Homework/hw2/data/list.json", lines=True, chunksize=100) as jreader:
        for chunk in jreader:
            for x in chunk['tags']:
                if type(x) == list:
                    counter.update(x)
            
    for tags, count in counter.most_common(5):
        print(tags + ', ' + str(count))

start = time.time()
pop_tags()
print(time.time() - start)