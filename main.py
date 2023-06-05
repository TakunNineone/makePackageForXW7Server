import os,warnings,json,shutil
from bs4 import BeautifulSoup


warnings.filterwarnings("ignore")

base_path=os.getcwd()
os.chdir('data/')
listdir=os.listdir()

def make_json(path,name,ep,ii):
	json_dict={
		"settings": {"reportId":ii},
		"offline": {
			"instance": name,"epUri": ep,"taxLocationRoot": "2023-03-31"
		},"orderList": [
			{
				"order": 0,"command":{
				"name": "controlCore",
				"renderingType": "file",
				"stopIfError": "false",
				"stepOverIfErrorLoadInstance": "true",
				"filterList": ["enum2"]
			}
			}
		]
	}
	with open(f'{path}\\jsons\\{ii}.json', 'w',) as f:
		json.dump(json_dict, f,ensure_ascii=False, indent=4)
i=0
run_str='chcp 65001\nset JAVA=java\n'
for xx in listdir:
	print(xx)
	i += 1
	with open(xx,'r',encoding='utf-8') as f:
		file_data=f.read()
	soup=BeautifulSoup(file_data,'lxml')
	soup_root=soup.contents[1]
	if soup_root.find_next('xbrl'):
		ep = soup_root.find_next('xbrl').find('link:schemaref')['xlink:href']
	else:
		ep = soup_root.find_next('xbrli:xbrl').find('link:schemaref')['xlink:href']
	ii=f'{i}'
	run_str=run_str+f"%JAVA% -Xms2048M -Xmx32000M -Dfile.encoding=UTF-8 -jar xwand7-adapter.jar --launch {ii} --config {ii}.json > {ii}.log 2>&1\n"
	make_json(base_path,xx,ep,ii)
	path_folder=f'{base_path}\\datas\\{ii}\\'
	os.mkdir(f'{base_path}\\datas\\{ii}\\')
	shutil.copy2(xx, f'{path_folder}\\{xx}')

run_str=run_str+'pause'
os.chdir(base_path)
with open(f'run_enum.bat','w') as r:
    r.write(run_str)