csv_to_model_map = {
    'NameOfTheTopic': 'topic',
    'Year': 'year',
    'Level': 'level',
    'IntroductionSummary': 'introductionSummary',
    'LearningOutcomes': 'learningOutcomes',
    'Summary': 'summary',
    'SummaryPageLink': 'summaryPageLink',
    'PDFFileLink': 'pdfFileLink',
    'Article_Name': 'articleName',
    'Topic': 'topic'
}

def convertRomanToInt(s):
  map = {'I':1, 'II': 2, 'III':3}
  return map[s]