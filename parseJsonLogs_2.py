import json,zipfile, os, gc
import pandas as pd

class parseJson():
    def __init__(self):
        self.project_path = os.getcwd()
        os.chdir(f'C:\\XBRL\\xw7 server 2\\data\\')
        self.path_=os.getcwd()
        self.filelist = os.listdir()
        self.df_Dic=[]

    def concatDfs(self,dfs):
        try: ret=pd.concat(dfs).reset_index(drop=True)
        except: ret=None
        return ret

    def neighborhood(self,iterable):
        iterator = iter(iterable)
        current_item = next(iterator) # throws StopIteration if empty.
        for next_item in iterator:
            yield (current_item, next_item)
            current_item = next_item
        yield (current_item, None)

    def read_folders(self):
        list_read=[]
        temp_dict={}

        for xx in self.filelist:
            os.chdir(f'{self.path_}\\{xx}')
            temp_path=f'{self.path_}\\{xx}'
            files=os.listdir()
            temp_dict[xx]={}
            for yy in files:
                try:
                    if '.txt' in yy:
                        temp_dict[xx]['package_name']=f'{temp_path}\\{yy}'
                        # package_name = z.read(item.filename).decode('utf-8')
                    elif 'evaluateAssertions_rend' in yy and 'skip' not in yy:
                        temp_dict[xx]['json_r'] = f'{temp_path}\\{yy}'
                except:
                    print(f'Ошибка в пакете {xx}, файл: {yy}')


        for xx in temp_dict.keys():
            try:
                print(temp_dict[xx]['package_name'],'  ',temp_dict[xx]['json_r'])
                with open(temp_dict[xx]['package_name'],'r',encoding='utf-8') as f:
                    package_name=f.read()
                with open(temp_dict[xx]['json_r'],'r',encoding='utf-8') as f:
                    json_r =json.loads(f.read())
                self.parse_json(package_name,json_r)
            except:
                print(f'Ошибка в пакете {xx}, файл: {temp_dict[xx]["package_name"]}')



    def list_to_str(self,list_):
        str=''
        for xx in list_:
            str=str+xx+';'
        return str

    def save_to_excel(self,df,name):
        os.chdir(self.project_path)
        with pd.ExcelWriter(f"{name}.xlsx") as writer:
            if len(df)>1048575:
                df[:1048575].to_excel(writer, index=False, sheet_name='result_1')
                df[1048575:].to_excel(writer, index=False, sheet_name='result_2')
            else:
                df.to_excel(writer,index=False,sheet_name='result')


    def parse_json(self,package_name,json_):
        temp_list=[]
        columns=['package_name','id','severity','result','time','test','qnames','values','elements','message']
        if 'assertions' in json_.keys():
            for ks in json_['assertions']:
                if 'getExpandedValidationMessages' in ks.keys():
                    message=ks['getExpandedValidationMessages']
                else:
                    message=None
                id=ks['id']
                severity=ks['severityLevel']
                tab=ks['xLinkRole']
                result=str(ks['result'])
                time=ks['evaluateTime']
                test=ks['test']
                qnames=[]
                values=[]
                elements=[]
                for var in ks['boundVariables']:
                    qnames.append(var['qname'])
                    for var_attr in var['values']:
                        values.append(var_attr['valueAsString'])
                        elements.append(var_attr['elemDeclId'])
                temp_list.append([package_name,id,severity,result,int(time),test,self.list_to_str(qnames),self.list_to_str(values),self.list_to_str(elements),message])
        else:
            print(f'Ошибка по пакету {package_name}, нет лога по КС\n {json_}')
        df=pd.DataFrame(data=temp_list,columns=columns)
        self.df_Dic.append(df)
        del json_,temp_list,df
        gc.collect()



if __name__ == "__main__":
    ss=parseJson()
    print(ss.filelist)
    ss.read_folders()
    df_final=ss.concatDfs(ss.df_Dic)
    del ss.df_Dic
    ss.save_to_excel(df_final,'59_package')
    del df_final
    gc.collect()
