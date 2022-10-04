import pandas as pd
import os
import pathlib


class DataDriver:
    def __init__(self, root, module_name) -> None:
        self.root = root
        self.module_name = module_name

    def get_data(self) -> pd.DataFrame:
        if self.module_name == 'Ems1' or self.module_name == 'Ems2':
            months = list(os.walk(f'{self.root}/{self.module_name}/'))[0][1]
            data = 0
            for month in months:
                if isinstance(data, pd.DataFrame):
                    paths = [p for p in pathlib.Path(
                        f'{self.root}/{self.module_name}/{month}').glob('**/*.csv')]
                    data_temp = 0
                    for path in paths:
                        self.clean_html(path)
                        if isinstance(data_temp, pd.DataFrame):
                            try:
                                data_temp = pd.concat(
                                    [data_temp, pd.read_csv(path, delimiter=';', index_col='signaldate')], axis=1)
                            except:
                                with open(path, 'r') as f:
                                    f = f.readlines()[0].split(';')
                                data_temp = pd.concat(
                                    [data_temp, pd.read_csv(path, delimiter=';', index_col='signaldate', usecols=list(range(len(f))))], axis=1)
                        else:
                            try:
                                data_temp = pd.read_csv(path, delimiter=';',
                                                        index_col='signaldate')
                            except:
                                with open(path, 'r') as f:
                                    f = f.readlines()[0].split(';')
                                data_temp = pd.read_csv(path, delimiter=';',
                                                        index_col='signaldate', usecols=list(range(len(f))))
                    data = pd.concat([data, data_temp], axis=0)
                else:
                    paths = [p for p in pathlib.Path(
                        f'{self.root}/{self.module_name}/{month}').glob('**/*.csv')]
                    data_temp = 0
                    for path in paths:
                        self.clean_html(path)
                        if isinstance(data_temp, pd.DataFrame):
                            try:
                                data_temp = pd.concat(
                                    [data_temp, pd.read_csv(path, delimiter=';', index_col='signaldate')], axis=1)
                            except:
                                with open(path, 'r') as f:
                                    f = f.readlines()[0].split(';')
                                data_temp = pd.concat(
                                    [data_temp, pd.read_csv(path, delimiter=';', index_col='signaldate', usecols=list(range(len(f))))], axis=1)
                        else:
                            try:
                                data_temp = pd.read_csv(path, delimiter=';',
                                                    index_col='signaldate')
                            except:
                                with open(path, 'r') as f:
                                    f = f.readlines()[0].split(';')
                                data_temp = pd.read_csv(path, delimiter=';',
                                                    index_col='signaldate', usecols=list(range(len(f))))
                    data = data_temp
            return data
        else:
            paths = [p for p in pathlib.Path(
                f'{self.root}/{self.module_name}').glob('**/*.csv')]
            data = 0
            for path in paths:
                self.clean_html(path)
                if isinstance(data, pd.DataFrame):
                    try:
                        data = pd.concat(
                            [data, pd.read_csv(path, delimiter=';', index_col='signaldate')], axis=1)
                    except:
                        with open(path, 'r') as f:
                            f = f.readlines()[0].split(';')
                        data = pd.concat(
                            [data, pd.read_csv(path, delimiter=';', index_col='signaldate', usecols=list(range(len(f))))], axis=1)
                else:
                    try:
                        data = pd.read_csv(path, delimiter=';',
                                        index_col='signaldate')
                    except:
                        with open(path, 'r') as f:
                            f = f.readlines()[0].split(';')
                        data = pd.read_csv(path, delimiter=';',
                                        index_col='signaldate', usecols=list(range(len(f))))
            return data

    def get_duplicated_col(self,data:pd.DataFrame) -> dict:
        col_dict = {}
        for c in data.columns.to_list():
            if c not in col_dict:
                col_dict[c] = 1
            else:
                col_dict[c] = col_dict[c]+1
        col_dict = {k: v for k, v in col_dict.items() if v > 1}
        return col_dict
    
    def get_unique_col(self, data:pd.DataFrame) -> list:
        df = data.loc[:, ~data.columns.duplicated()].copy()
        updated_col = df.columns.tolist()
        updated_col = [" ".join(i.strip().split()) for i in updated_col]
        return updated_col
    
    def get_missing_col(self, updated_col:list) -> list:
        rem_col = pd.read_excel('All_columns.xlsx', sheet_name=self.module_name)
        col_list = []
        for c in updated_col:
            if c not in rem_col[self.module_name].apply(lambda x: " ".join(x[:-14].strip().split())).to_list():
                col_list.append(c)
        return col_list
    
    def clean_html(self, path:str) -> None:
        with open(path, 'r') as file:
            file = file.readlines()
            for line in file[-10:]:
                if line.startswith('<'):
                    file.pop(file.index(line))
            with open(path, 'w') as f:
                f.writelines(file)