from unittest import TestCase
from unittest.mock import patch
import pandas as pd
from scripts.data_cleaner import cleanDataWebScrape, convertDFtoCSV, cleanDataPDF

class DataCleanTestClass(TestCase):
  @patch('scripts.data_cleaner.pd.read_csv')
  @patch('scripts.data_cleaner.pd.DataFrame.to_csv')
  def test_cleanDataWebScrape(self, mock_write_csv, mock_read_csv):
    # Mocking read csv
    mock_read_csv.return_value = pd.DataFrame({
      'NameOfTheTopic': ['Topic 1 ', 'Topic Test RR'],
      'Year': [2020, 2021],
      'Level': ['I', 'II'],
      'IntroductionSummary': ['Intro 1 ', 'Intro 2'],
      'LearningOutcomes': ['Outcome 1', ' Outcome 2'],
      'Summary': ['Summary        1', ' Summary  2 '],
      'SummaryPageLink': ["https://www.cfainstitute.org/membership/professional-development/refresher-readings/test-reading-path-1", "https://www.cfainstitute.org/membership/professional-development/refresher-readings/test-reading-path-1"],
      'PDFFileLink': ["some random string", 'https://www.cfainstitute.org/-/media/documents/protected/refresher-reading/2024/level2/level2a/RR_2024_L2V1R5-1.pdf']
    })
    # Mocking Write csv
    mock_write_csv.return_value = True
    
    df = cleanDataWebScrape("some-path/to-read.csv")
    self.assertIsNotNone(df)
    self.assertIsNone(convertDFtoCSV(df, "/some/location.logs"))


  @patch('scripts.data_cleaner.pd.read_csv')
  @patch('scripts.data_cleaner.pd.DataFrame.to_csv')
  def test_cleanDataPDF(self, mock_write_csv, mock_read_csv):
    # Mocking read csv
    mock_read_csv.return_value = pd.DataFrame({
      'topic': ['Topic 1 ', 'Topic Test RR'],
      'year': [2020, 2021],
      'level': ['I', 'II'],
      'articleName': ['Intro 1 ', 'Intro 2'],
      'Summary': [' □ Summary □    1', ' Summary  2 ']
    })
    # Mocking Write csv
    mock_write_csv.return_value = True
    
    df = cleanDataPDF("some-path/to-read.csv")
    self.assertIsNotNone(df)
    self.assertIsNone(convertDFtoCSV(df, "/some/location.logs"))

