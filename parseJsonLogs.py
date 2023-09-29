import json,zipfile, os, gc
import pandas as pd

class parseJson():
    def __init__(self):
        self.project_path = os.getcwd()
        os.chdir(f'{os.getcwd()}/logs')
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

    def read_zip(self,filename):
        list_read=[]
        temp_dict={}
        with zipfile.ZipFile(filename) as z:
            for item in z.infolist():
                if item.is_dir():
                    temp_dict[item.filename.split('/')[0]]={}

        with zipfile.ZipFile(filename) as z:
            for item in z.infolist():
                if '.txt' in item.filename:
                    folder = item.filename.split('/')[0]
                    temp_dict[folder]['package_name']=item.filename
                    # package_name = z.read(item.filename).decode('utf-8')
                elif 'evaluateAssertions_rend' in item.filename and 'skip' not in item.filename:
                    folder = item.filename.split('/')[0]
                    temp_dict[folder]['json_r'] = item.filename

        with zipfile.ZipFile(filename) as z:
            for xx in temp_dict.keys():
                print(temp_dict[xx]['package_name'],'  ',temp_dict[xx]['json_r'])
                package_name = z.read(temp_dict[xx]['package_name']).decode('utf-8')
                json_r = json.loads(z.read(temp_dict[xx]['json_r']).decode('utf-8'))
                self.parse_json(package_name,json_r)


    def list_to_str(self,list_):
        str=''
        for xx in list_:
            str=str+xx+';'
        return str

    def save_to_excel(self,df,name):
        os.chdir(self.project_path)
        with pd.ExcelWriter(f"{name}.xlsx") as writer:
            df.to_excel(writer,index=False,sheet_name='result')

    def parse_json(self,package_name,json_):
        temp_list=[]
        columns=['package_name','id','severity','result','time','test','qnames','values','elements','message']
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
        df=pd.DataFrame(data=temp_list,columns=columns)
        self.df_Dic.append(df)
        del json_,temp_list,df
        gc.collect()



if __name__ == "__main__":
    ss=parseJson()
    print(ss.filelist)
    ss.read_zip('4.zip')
    df_final=ss.concatDfs(ss.df_Dic)
    del ss.df_Dic
    ss.save_to_excel(df_final,'5_package')
    del df_final
    gc.collect()


    # for xx in ss.filelist:
    #     ss.parse_json(ss.read_one_zip(xx))
    # df_final=ss.concatDfs(ss.df_Dic)
    # del ss.df_Dic
    # ss.save_to_excel(df_final,'result')
    # del df_final
    # gc.collect()
