import pandas
import os

def excel_reader():
    excel_path = os.path.abspath('../기상청41_단기예보 조회서비스_오픈API활용가이드_격자_위경도(20220701).xlsx')
    file_pointer = pandas.read_excel(excel_path, engine='openpyxl')
    print(file_pointer.columns)
