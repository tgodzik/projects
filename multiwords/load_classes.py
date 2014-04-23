# coding=utf-8
__author__ = 'Tomasz Godzik'

import pickle
from multiwords import Multisegment

extractor = Multisegment("plp/clp/lib/libclp_2.6.so")

ret_set = extractor.load_classes_from_file("types.txt")

save_dict_file = open("types", 'wb')
pickle.dump(ret_set, save_dict_file)

print("Found multisegment words classes : ")
for i in ret_set:
    print(i)