from unittest import TestCase
from parameterized import parameterized

from models_py.metadata_data_model import PDFValidationClass

# dummy data
data = {
  'text' : "test topic 1",
  'para' : 2021,
  'bboxes' : [[{'page': '1', 'x': '84.00', 'y': '681.59', 'h': '136.31', 'w': '9.24'}]],
  'pages' : "('1', '1')",
  'section_title' : "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
  'section_number' : 0.1,
  'paper_title' : "amework and Macro Consideration",
  'file_path' : "./data/pdf_input/2024-l3-topics-combined-2.pdf",
}


data_no_text = {key: value for key, value in data.items() if key != "text"}
data_no_para = {key: value for key, value in data.items() if key != "para"}
data_no_bboxes = {key: value for key, value in data.items() if key != "bboxes"}
data_no_pages = {key: value for key, value in data.items() if key != "pages"}
data_no_section_title = {key: value for key, value in data.items() if key != "section_title"}
data_no_section_number = {key: value for key, value in data.items() if key != "section_number"}
data_no_paper_title = {key: value for key, value in data.items() if key != "paper_title"}
data_no_file_path = {key: value for key, value in data.items() if key != "file_path"}


class CFADataModelTestClass(TestCase):
  def setUp(self):
    ''' initialize data '''
    # all values populated
    self.data = data.copy()

  @parameterized.expand([
    (data,),
    (data_no_text,),
    (data_no_para,),
    
  ])
  def test_model_creation_correct_data(self, data):
    ''' test model creation with correct data (some optional fields missing) '''
    validate_res = PDFValidationClass.model_validate(data)
    self.assertIsNotNone(validate_res)
    
  @parameterized.expand([
    (data_no_bboxes,),
    (data_no_pages,),
    (data_no_section_title,),
    (data_no_section_number,),
    (data_no_paper_title,),
    (data_no_file_path,),
  ])
  def test_model_creation_incorrect_data(self, data):
    ''' test model creation with missing mandatory data '''
    with self.assertRaises(ValueError):
      PDFValidationClass.model_validate(data, strict=True)

