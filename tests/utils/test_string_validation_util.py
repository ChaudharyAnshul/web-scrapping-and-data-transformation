from unittest import TestCase
from parameterized import parameterized

from utils.string_validation_util import validate_string_spaces, Validate_string_line_space_char, Validate_topic_test_rr

class DataCleanerUtilTestClass(TestCase):
  
  @parameterized.expand([
    ("test string ",False),
    ("test string",True),
    (" test string ",False),
    ("test          string",False),
    ("test  string",False),
  ])
  def test_string_validation_space(self, string, result):
    ''' test for white space in string '''
    res = validate_string_spaces(string)
    self.assertEqual(res, result)
  
  @parameterized.expand([
    ("test string",True),
    ("test \n string",False),
    ("test □ string",False),
  ])
  def test_Validate_string_line_space_char(self, string, result):
    ''' test for line space in string '''
    res = Validate_string_line_space_char(string)
    self.assertEqual(res, result)
    
  @parameterized.expand([
    ("test Test RR string",False),
    ("test string",True),
  ])
  def test_Validate_topic_test_rr(self, string, result):
    ''' test for Test RR in string '''
    res = Validate_topic_test_rr(string)
    self.assertEqual(res, result)