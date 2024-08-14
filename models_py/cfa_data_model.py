from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import re
from utils.string_validation_util import validate_string_spaces, Validate_string_line_space_char, Validate_topic_test_rr

class CFADataModel(BaseModel):
  topic: str
  year: Optional[int] = Field(default = None)
  level: int
  introductionSummary: Optional[str] = Field(default = None)
  learningOutcomes: Optional[str] = Field(default = None)
  summary: Optional[str] = Field(default = None)
  summaryPageLink: str = Field(pattern=r'^https:\/\/www\.cfainstitute\.org\/.*')
  pdfFileLink: Optional[str] = Field(default = None, pattern=r'^https://www\.cfainstitute\.org/-/media/documents/protected/.*\.pdf$')

  @field_validator("topic")
  @classmethod
  def topic_validator(cls, v):
    ''' check spaces in topic '''
    if v:
      if not Validate_topic_test_rr(v):
        raise ValueError("Test RR page")
      if not validate_string_spaces(v):
        raise ValueError('Unwanted spaces in the string')
      return v.title()

  @field_validator("year")
  @classmethod
  def year_validator(cls, v):
    ''' check year on the content '''
    if v:
      reg_pattern=r'^20\d{2}$'
      if not re.match(reg_pattern, str(v)):
        raise ValueError('Year not in range')
      if v > datetime.now().year:
        raise ValueError('Year is in Future')
      return v
    
  @field_validator("level")
  @classmethod
  def level_validator(cls, v):
    ''' check level digits '''
    if v:
      reg_pattern=r'^[123]$'
      if not re.match(reg_pattern, str(v)):
        raise ValueError('Level not in range')
      return v

  @field_validator("introductionSummary", "learningOutcomes", "summary", mode="before")
  @classmethod
  def introduction_validator(cls, v):
    ''' check all the text paragraphs for spaces and unwanted characters '''
    if v:
      if not validate_string_spaces(v):
        raise ValueError('Unwanted spaces in the string')
      if not Validate_string_line_space_char(v):
        raise ValueError('Unwanted line space character') 
      return v