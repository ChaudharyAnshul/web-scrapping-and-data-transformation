from unittest import TestCase
from parameterized import parameterized
from models_py.metadata_data_model import PDFValidationClass  

# Dummy data
data = {
    'text': "Lorem ipsum dolor sit amet",
    'para': 1,
    'bboxes': [[{'x': 1, 'y': 2, 'width': 3, 'height': 4}]],
    'pages': "(1, 2)",
    'section_title': "Section",
    'section_number': None,
    'paper_title': "Paper Title",
    'file_path': "../data/pdf_input/2022-l1-topics-combined-123.pdf",
}


data_no_text = {key: value for key, value in data.items() if key != "text"}
data_no_para = {key: value for key, value in data.items() if key != "para"}
data_no_bboxes = {key: value for key, value in data.items() if key != "bboxes"}
data_no_pages = {key: value for key, value in data.items() if key != "pages"}
data_no_section_title = {key: value for key, value in data.items() if key != "section_title"}
data_no_section_number = {key: value for key, value in data.items() if key != "section_number"}
data_no_paper_title = {key: value for key, value in data.items() if key != "paper_title"}
data_no_file_path = {key: value for key, value in data.items() if key != "file_path"}

class PDFValidationClassTestCase(TestCase):
    def setUp(self):
        ''' initialize data '''
        # all values populated
        self.data = data.copy()

    @parameterized.expand([
        (data,),
        (data_no_para,),
        (data_no_text,),
    ])
    def test_model_creation_correct_data(self, data):
        ''' test model creation with correct data (some optional fields missing) '''
        validate_res = PDFValidationClass(**data)
        self.assertIsNotNone(validate_res)

    @parameterized.expand([
        (data_no_file_path,),
        (data_no_bboxes,),
        (data_no_pages,),
        (data_no_section_title,),
        (data_no_section_number,),
        (data_no_paper_title,),
    ])
    def test_model_creation_incorrect_data(self, data):
        ''' test model creation with missing mandatory data '''
        with self.assertRaises(ValueError):
            PDFValidationClass(**data)

    # Add more specific test cases for your validators as needed
