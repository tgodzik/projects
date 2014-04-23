# coding=utf-8
__author__ = 'Tomasz Godzik'
from multiwords import Multisegment
from collections import defaultdict
import re

# load possible classes from file
segments = Multisegment("plp/clp/lib/libclp_2.6.so")
segments.load_classes_from_file("types.txt")

# search file for possible candidates
#names of files to look in
filenames = ["data/tekst"+str(j)+".txt" for j in range(10, 16)]

candidates, words = segments.find_candidates_in_files(filenames)


# generate neighbours dict

neighbours = defaultdict(int)
# ok map

for j in filenames:
    doc = open(j).read()
    ws = re.findall("[A-Z0-9a-zóęąśłżźćńĘÓĄŚŁŻŹĆŃ]+", doc, re.UNICODE)
    w0 = segments.find_base(ws[0])
    if w0 in words:
        neighbours[w0] += 1
    wn = segments.find_base(ws[len(ws)-1])
    if wn in words:
        neighbours[wn] += 1
    for i in range(1, len(ws)-1):
        cur = segments.find_base(ws[i])
        if cur in words:
            neighbours[cur] += 2


def score(one, other):
    # If does not exist with other words
    if other == 0:
        other = 1
    return 100.0 * float(one)/float(other)

for k, v in candidates.items():
    other = 0
    for i in re.findall("[A-Z0-9a-zóęąśłżźćńĘÓĄŚŁŻŹĆŃ]+", k, re.UNICODE):
        other += neighbours[i]
    res = score(v, other)
    if res > 0.5:
        print(k, " : ", res)

