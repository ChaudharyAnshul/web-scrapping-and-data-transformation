from unittest import TestCase
from parameterized import parameterized

from models_py.pdf_data_model import PDFDataModel

# dummy data
data = {
  'topic' : "test topic 1",
  'year' : "2021",
  'level' : 2,
  'summary' : "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
  'articleName' : "some random article"
}

data_no_topic = {key: value for key, value in data.items() if key != "topic"}
data_no_year = {key: value for key, value in data.items() if key != "year"}
data_no_level = {key: value for key, value in data.items() if key != "level"}
data_no_summary = {key: value for key, value in data.items() if key != "summary"}
data_no_articleName = {key: value for key, value in data.items() if key != "articleName"}

class PDFDataModelTestClass(TestCase):
  def setUp(self):
    ''' initialize data '''
    # all values populated
    self.data = data.copy()
    
  @parameterized.expand([
    (data,),
    (data_no_year,),
    (data_no_summary,),
  ])
  def test_model_creation_correct_data(self, data):
    ''' test model creation with correct data (some optional fields missing) '''
    validate_res = PDFDataModel.model_validate(data)
    self.assertIsNotNone(validate_res)
    
  @parameterized.expand([
    (data_no_topic,),
    (data_no_level,),
    (data_no_articleName,),
  ])
  def test_model_creation_incorrect_data(self, data):
    ''' test model creation with missing mandatory data '''
    with self.assertRaises(ValueError):
      PDFDataModel.model_validate(data, strict=True)
      
  def test_model_creation_incorrect_topic_data(self):
    ''' test model creation with incorrect level data '''
    self.data["topic"] = "this is not a topic "
    with self.assertRaises(ValueError) as err:
      PDFDataModel.model_validate(self.data)
    self.assertIn("Unwanted space", str(err.exception))
    
  def test_model_creation_incorrect_level_range_data(self):
    ''' test model creation with incorrect level data '''
    self.data["level"] = 4
    with self.assertRaises(ValueError) as err:
      PDFDataModel.model_validate(self.data)
    self.assertIn("level", str(err.exception))
    
  def test_model_creation_incorrect_level_data(self):
    ''' test model creation with incorrect level data '''
    self.data["level"] = "II"
    with self.assertRaises(ValueError) as err:
      PDFDataModel.model_validate(self.data)
    self.assertIn("level", str(err.exception))
    
  def test_model_creation_incorrect_year_data(self):
    ''' test model creation with incorrrect year (wrong data) '''
    self.data["year"] = "1930"
    with self.assertRaises(ValueError) as err:
      PDFDataModel.model_validate(self.data)
    self.assertIn("Year not in range", str(err.exception))
    
  def test_model_creation_incorrect_year_in_future_data(self):
    ''' test model creation with incorrrect year (wrong data) '''
    self.data["year"] = "2098"
    with self.assertRaises(ValueError) as err:
      PDFDataModel.model_validate(self.data)
    self.assertIn("Year is in Future", str(err.exception))
    
  def test_model_creation_incorrect_summart_data(self):
    ''' test model creation with space and new line space in string '''
    self.data["summary"] = " is there any test summary with \n character in string"
    with self.assertRaises(ValueError) as err:
      PDFDataModel.model_validate(self.data)
    self.assertIn("Unwanted space", str(err.exception))
    
  def test_model_creation_incorrect_article_data(self):
    ''' test model creation with space and new line space in string '''
    self.data["articleName"] = "test article name "
    with self.assertRaises(ValueError) as err:
      PDFDataModel.model_validate(self.data)
    self.assertIn("Unwanted space", str(err.exception))