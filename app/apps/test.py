class TestUtil():

    @classmethod
    def setup_class(cls):
        from .xlsx_reader import XlsxReader

        cls.xlsx_pointer = XlsxReader()

    def test_could_read_xlsx_file_to_json(self):

        result = self.xlsx_pointer.get_all_xlsx_data()

        assert 60 == (result[0])

    def test_could_get_filtered_location_data_to_json(self):
        filter_data = {"3단계":"백현동"}
        result = self.xlsx_pointer.filter_xlsx_data(filter_data)

        assert 62 == (result[0])
