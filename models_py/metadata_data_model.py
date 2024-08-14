from typing import List, Optional, Tuple, Any, Union
import re
import ast
from pydantic import BaseModel, Field, field_validator

class PDFValidationClass(BaseModel):
    text: str = Field(default = None)
    para: int = Field(default = None)
    bboxes: List[List[dict]]
    pages: str
    section_title: str
    section_number: Optional[float]
    paper_title: Optional[Union[str, float]]
    file_path: str

    @field_validator("bboxes")
    def convert_and_validate_bboxes(cls, value: Any):
        if isinstance(value, str):
            try:
                # Convert string to list of lists of dictionaries
                bboxes_list = ast.literal_eval(value)
                if not isinstance(bboxes_list, list):
                    raise ValueError("Invalid format for bboxes.")
                return bboxes_list
            except (ValueError, SyntaxError):
                raise ValueError("Invalid format for bboxes.")
        return value
    
    @field_validator("pages")
    def validate_pages(cls, value):
        if not isinstance(ast.literal_eval(value), tuple):
            raise ValueError("Pages should be a tuple.")
        return value

    @field_validator("section_number")
    def validate_section_number(cls, value):
        if value is not None and not isinstance(value, (int, float)):
            raise ValueError("Section number must be a valid number.")
        return value

    @field_validator("paper_title")
    def validate_paper_title(cls, value):
        if value is not None and not isinstance(value, (str, float)):
            raise ValueError("Paper title can be either text, a number, or null.")
        return value

    @field_validator("file_path")
    def validate_file_path(cls, value):
        # Additional pattern check
        if not value.endswith(".pdf"):
            raise ValueError("File name must match the specified format.")
        return value