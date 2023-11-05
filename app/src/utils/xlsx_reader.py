# --------------------------------------------------------------------------
# 유저의 선호 장소에 대한 격자 X, 격자 Y 값을 xlsx 파일에서 받아와 리턴하는 모듈입니다.
#
# 데이터 수가 많음에 따라 검색에 시간이 걸립니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import pandas
import os
import json


class XlsxReader:
    def __init__(self):
        self.target_nx = None
        self.target_ny = None

    @staticmethod
    def excel_parser():
        excel_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "resources",
            "기상청41_단기예보 조회서비스_오픈API활용가이드_격자_위경도(20220103).xlsx",
        )
        file_pointer = pandas.read_excel(
            excel_path,
            engine="openpyxl",
            header=0,
            names=["행정구역코드", "1단계", "2단계", "3단계", "격자 X", "격자 Y"],
            usecols="B:G",
        )

        return file_pointer

    @staticmethod
    def dataframe_to_json(dataframe):
        json_string = dataframe.to_json(orient="index", force_ascii=False)
        json_string_parsed = json.loads(json_string)

        return json_string_parsed

    def get_all_xlsx_data(self):
        file_pointer = self.excel_parser()

        self.set_nx_ny_with_data(file_pointer)

        return self.target_nx, self.target_ny

    def filter_xlsx_data(self, area_name):
        file_pointer = self.excel_parser()

        matches = file_pointer[
            file_pointer["1단계"].str.contains(area_name)
            | file_pointer["2단계"].str.contains(area_name)
            | file_pointer["3단계"].str.contains(area_name)
        ]

        if not matches.empty:
            file_pointer = matches

            self.set_nx_ny_with_data(file_pointer)

            return self.target_nx, self.target_ny
        else:
            print(f"No matches found for {area_name}")
            print("Returning default coordinates (60, 127)")
            return 60, 127

    def set_nx_ny_with_data(self, file_pointer):
        head_data_of_pointer = file_pointer.iloc[0]
        excel_json_parsed = self.dataframe_to_json(head_data_of_pointer)

        self.target_nx = excel_json_parsed.get("격자 X")
        self.target_ny = excel_json_parsed.get("격자 Y")
