from pydantic import BaseModel, Field

class FileProcessRequestSchema(BaseModel):
    written_file_name : str
    chunk_size : int = Field(default=100, description="the chunk size of the document that langchain uses while splitting")
    overlap_size : int = Field(default=20, description="the overlap size between two recursive chunks")
