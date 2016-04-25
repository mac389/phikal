import json

READ = 'rb'

def flatten(foo):
    for x in foo:
        if hasattr(x, '__iter__'):
            for y in flatten(x):
                yield y
        else:
            yield x

def find_ngrams(input_list, n):
  return zip(*[input_list[i:] for i in range(n)])
