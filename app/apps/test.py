class TestUtil():

    @classmethod
    def setup_class(cls):
        from .xlsx_reader import XlsxReader
        from .user_data_trimmer import UserDataTrimmer

        cls.xlsx_pointer = XlsxReader()
        cls.user_data_trimmer = UserDataTrimmer()

    def test_could_read_xlsx_file_to_json(self):
        result = self.xlsx_pointer.get_all_xlsx_data()

        assert 60 == (result[0])

    def test_could_get_filtered_location_data_to_json(self):
        filter_data = {"3단계":"백현동"}
        result = self.xlsx_pointer.filter_xlsx_data(filter_data)

        assert 62 == (result[0])

    def test_could_convert_pcp_value(self):
        test_value = '20.0mm'

        assert '20.0' == (test_value[:-2])

    def test_could_get_formatted_location_data_from_db(self):
        test_user_location_data = {'user_location_first':None, 'user_location_second':None, 'user_location_third':None}

        result = self.user_data_trimmer.convert_user_locations_into_readable_data(test_user_location_data.get('user_location_first'), test_user_location_data.get('user_location_second'), test_user_location_data.get('user_location_third'))
        
        assert {'1단계': '서울특별시'} == (result)

        test_user_location_data = {'user_location_first':'부산광역시', 'user_location_second':None, 'user_location_third':None}

        result = self.user_data_trimmer.convert_user_locations_into_readable_data(test_user_location_data.get('user_location_first'), test_user_location_data.get('user_location_second'), test_user_location_data.get('user_location_third'))
        
        assert {'1단계': '부산광역시'} == (result)

        test_user_location_data = {'user_location_first':'경기도', 'user_location_second':'성남시분당구', 'user_location_third':None}

        result = self.user_data_trimmer.convert_user_locations_into_readable_data(test_user_location_data.get('user_location_first'), test_user_location_data.get('user_location_second'), test_user_location_data.get('user_location_third'))
        
        assert {'2단계': '성남시분당구'} == (result)

    def test_could_get_nx_ny_from_formatted_user_location_data(self):
        test_user_location_data = {'user_location_first':'경기도', 'user_location_second':'성남시분당구', 'user_location_third':None}

        detailed_location_json = self.user_data_trimmer.convert_user_locations_into_readable_data(test_user_location_data.get('user_location_first'), test_user_location_data.get('user_location_second'), test_user_location_data.get('user_location_third'))
        
        nx, ny = self.xlsx_pointer.filter_xlsx_data(detailed_location_json)

        assert (62, 123) == (nx, ny)

        nx, ny = str(nx), str(ny)

        # cordinates value must be type string, because these values will be handled with json.
        assert ('62', '123') == (nx, ny)
