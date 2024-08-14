from IPython.display import display
import logging

def customLogger(file_name: str,):
  # Configure logging
  file_name = "logs/" + file_name
  
  logger = logging.getLogger(__name__)
  logger.setLevel(logging.DEBUG)
  if not logger.handlers:
    handler = logging.FileHandler(file_name)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

  # display log message in-line 
  class NotebookHandler(logging.Handler):
    def emit(self, record):
      display(self.format(record))
  logger.addHandler(NotebookHandler())
  # set the file to empty at start
  with open(file_name, 'w'):
    pass
  
  return logger