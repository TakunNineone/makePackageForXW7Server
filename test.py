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
os.chdir('data/')
run_str_line=[]

with zipfile.ZipFile('data_test.zip') as z:
    for filename in z.namelist():
        i += 1
        if not os.path.isdir(filename):
            with z.open(filename) as f:
                check = False
                for item,next_ in neighborhood(f):
                    if re.findall('xlink:href="(.+?)"', item.decode("utf-8")):
                        ff=re.search(r'(xlink:href=")(.+?)(")', item.decode("utf-8"))
                        ep=item.decode("utf-8")[ff.start()+12:ff.end()-1].replace('" xlink:type="simple','')
                        run_str_line.append(f"%JAVA% -Xms2048M -Xmx32000M -Dfile.encoding=UTF-8 -jar xwand7-adapter.jar --launch {i} --config {i}.json > {i}.log 2>&1")
                        path_folder = f'{base_path}\\datas\\{i}'
                        path_copy=  f'{base_path}\\data'
                        check=True
                        break
                if check==False:
                    print(filename,'NO')