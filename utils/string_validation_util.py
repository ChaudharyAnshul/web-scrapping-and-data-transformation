import re

# helper function to validate spaces in string 
def validate_string_spaces(v):
  if v:
    start = v.startswith(" ")
    end = v.endswith(" ")
    if start or end:
      return False
    if re.findall(r'\s{2,}', v):
      return False
  return True

def Validate_string_line_space_char(v):
  if v:
    if '\n' in v:
      return False
    if '□' in v:
      return False
    return True
  
def Validate_topic_test_rr(v):
  if v:
    if "test rr" in v.lower():
      return False
    return True