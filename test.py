import os,zipfile,re

def neighborhood(iterable):
    iterator = iter(iterable)
    current_item = next(iterator) # throws StopIteration if empty.
    for next_item in iterator:
        yield (current_item, next_item)
        current_item = next_item
    yield (current_item, None)

base_path=os.getcwd()
i=0
os.chdir('C:\\XBRL\\xw7 server 2\\')
path= f'{os.getcwd()}\\19.log'
with open(path) as f:
   for line in f:
       process(line)

print(f[-40:])