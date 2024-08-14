import pandas as pd
import numpy as np
from models_py.cfa_data_model import CFADataModel
from models_py.pdf_data_model import PDFDataModel
from scripts.custom_logger import customLogger
from utils.data_cleaner_util import convertRomanToInt, csv_to_model_map
import re
import sys
import logging


if 'unittest' in sys.modules.keys():
  logger = logging  
else:
  logger = customLogger('data-validation-cleaning.log')

def validate_function(model, max_attempts=3, **kwargs):
  ''' function to validate the raw data, and then try to fix the data if any validation is hit '''
  attempts = 0
  if "topic" not in kwargs:
    return None
  logger.info("Validating {} --------------".format(kwargs["topic"]))
  while attempts < max_attempts:
    try:
      m = model(**kwargs)
      logger.info("Succesfully validated {}".format(kwargs["topic"]))
      return m.model_dump()
    except Exception as e:
      for error in e.errors():
        field_name = error['loc'][0]
        msg = error["msg"]
        logger.info("Attempting to fix the error {}".format(field_name))
        if field_name == "topic":
          if kwargs["topic"] == None:
            kwargs["topic"] = None
          elif "Test RR page" in msg:
            break
          else:
            kwargs["topic"] = kwargs["topic"].strip()
        elif field_name == "level":
          kwargs["level"] = convertRomanToInt(kwargs["level"])
        elif field_name in ["introductionSummary", "learningOutcomes", "summary"]:
          temp = kwargs[field_name].strip(" ")
          temp_list = [s.strip() for s in temp.split("\n")]
          temp = ' '.join(temp_list)
          temp = re.sub(r'\s+', ' ', temp)
          temp = temp.replace("□", "", 1)
          temp = temp.replace("□", ";")
          kwargs[field_name] = temp
        elif field_name == "pdfFileLink":
          kwargs["pdfFileLink"] = None
      attempts += 1
      logger.info("Retrying running model...")
  logger.error("could not fix csv entry for {}".format(kwargs['topic']))


def cleanDataWebScrape(csv_path):
  ''' function to pass values to validator and clean web scrapping data '''
  logger.info("------- Starting validating dataframe data -------")
  logger.info("Validating data using CFADataModel")
  df = pd.read_csv(csv_path, sep="\t")
  df = df.replace(np.nan, None)
  result_list = []
  for _, row in df.iterrows():
    topic_data = {}
    for column, field in csv_to_model_map.items():
      if column in row:
        topic_data[field] = row[column]
    res = validate_function(CFADataModel, max_attempts=4, **topic_data)
    if res:
      result_list.append(res)

  df_clean = pd.DataFrame(result_list)
  logger.info("------- Ending validating dataframe data -------")
  return df_clean

def cleanDataPDF(csv_path):
  ''' function to pass values to validator and clean pdf data'''
  logger.info("------- Starting validating dataframe data -------")
  logger.info("Validating data using PDFDataModel")
  df = pd.read_csv(csv_path)
  print(df)
  print(df.isnull().sum())

  df = df.replace(np.nan, None)
  result_list = []
  for _, row in df.iterrows():

    topic_data = {}
    for column, field in csv_to_model_map.items():
      if column in row:
        topic_data[field] = row[column]
    res = validate_function(PDFDataModel, max_attempts=4, **topic_data)
    if res:
      result_list.append(res)

  df_clean = pd.DataFrame(result_list)
  logger.info("------- Ending validating dataframe data -------")
  return df_clean


def convertDFtoCSV(df, csv_location):
  ''' function to store DF locally '''
  logger.info("-------Starting Writing to CSV -------")
  df.to_csv(csv_location, index=False, sep="\t", float_format='%d')
  logger.info("------- Ending Writing to CSV -------")
  
if __name__ == '__main__': 
  df_cfa = cleanDataWebScrape(csv_path="data/raw-data/cfa-data.csv")
  convertDFtoCSV(df_cfa, csv_location = "data/clean-data/cfa-data-clean.csv")
  
  df_pdf_grobid = cleanDataPDF(csv_path="data/pdf_raw_output/grobid_output.csv")
  convertDFtoCSV(df_pdf_grobid, csv_location = "data/clean-data/pdf-data-grobid-clean.csv")
  
  df_pdf_pypdf = cleanDataPDF(csv_path="data/pdf_raw_output/pypdf_output.csv")
  convertDFtoCSV(df_pdf_pypdf, csv_location = "data/clean-data/pdf-data-pypdf-clean.csv")