import pandas
import os
import json


class XlsxReader():
    
    def __init__(self):
        self.target_nx = None
        self.target_ny = None

    def excel_parser(self):
        excel_path = os.path.abspath('../../기상청41_단기예보 조회서비스_오픈API활용가이드_격자_위경도(20220103).xlsx')
        file_pointer = pandas.read_excel(excel_path, 
        engine='openpyxl', 
        header=0,
        names=['행정구역코드', '1단계', '2단계', '3단계', '격자 X', '격자 Y'],
        usecols="B:G")

        return file_pointer

    def dataframe_to_json(self, dataframe):
        json_string = dataframe.to_json(orient = 'index', force_ascii = False)
        json_string_parsed = json.loads(json_string)

        return json_string_parsed

    def get_all_xlsx_data(self):
        file_pointer = self.excel_parser()
        
        self.set_nx_ny_with_data(file_pointer)

        return self.target_nx, self.target_ny

    def filter_xlsx_data(self, *args):
        file_pointer = self.excel_parser()
        for key, value in args[-1].items():
            file_pointer = file_pointer[file_pointer[str(key)]==str(value)]

        self.set_nx_ny_with_data(file_pointer)

        return self.target_nx, self.target_ny

    def set_nx_ny_with_data(self, file_pointer):
        head_data_of_pointer = file_pointer.iloc[0]
        excel_json_parsed = self.dataframe_to_json(head_data_of_pointer)

        self.target_nx = excel_json_parsed.get('격자 X')
        self.target_ny = excel_json_parsed.get('격자 Y')
