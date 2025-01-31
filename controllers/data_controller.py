from controllers.base_controller import BaseController
from controllers.project_controller import ProjectController
from enums.constants import Constants
from fastapi import UploadFile
from typing import Union
import os
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from helpers.pydantic_schemas_for_validation import FileProcessRequestSchema

class DataController(BaseController):
    def __init__(self, project_id: int):
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(self.project_id)  # absolute path excluding the terminal file names.  

    async def check_file_validity(self, file: UploadFile) -> dict:
        """
        # Alternative code to get th type content:
        import mimetypes
        mimetypes.types_map # outputs dict['content_type','file_extension']
        mimetypes.guess_type('file_path') # outputs the content_type of the file   
        #or 
        print(mimetypes.types_map['.txt']) -> 'text/plain'
        """

        if (file.content_type not in self.app_settings.ALLOWED_MIME_TYPES):
            signal = Constants.InvalidFileTypeResponse.value.format(file.content_type, self.app_settings.ALLOWED_MIME_TYPES)
            self.app_settings.logger.info(signal)
            return {
                    "valid": False,
                    "signal" : signal
                }
            # raise ValueError(f"this file type {file.content_type} is not supported. Here are the supported file types {self.app_settings.ALLOWED_MIME_TYPES}")
            # if we typed this raise, we got error from the code ... and in request, error in code is seen as internal server error
        
        elif (file.size  > self.app_settings.MAX_FILE_SIZE * 1024 * 1024):
            signal = Constants.InvalidFileSizeResponse.value.format(file.size, self.app_settings.MAX_FILE_SIZE)
            self.app_settings.logger.info(signal)
            return {
                    "valid": False,
                    "signal" : signal
                }            
        else:
            write_signal, written_file_path = await ProjectController().write_uploaded_file_and_return_signal(file ,self.project_id) # write the uploaded file in the folders directory
            written_file_name = os.path.split(written_file_path)[-1] # in order not to show the whole path to the user
            signal = Constants.SuccessUploadResponse.value.format(written_file_name) if not write_signal else write_signal
            self.app_settings.logger.info(signal) if not write_signal else None  # as write_signal is already logged in project_controller.py as error when there was an exception. 
            return {
                    "valid": True,
                    "written_file_name" : written_file_name,
                    "signal" : signal
                }
    
    def load_documents(self, file_path: str) -> Union[None, list[PyMuPDFLoader], list[TextLoader]]:
        try:
            if file_path.endswith(".txt"):
                return TextLoader(file_path=file_path, encoding='utf-8').load()
            elif file_path.endswith(".pdf"):
                return PyMuPDFLoader(file_path=file_path).load()  # Use PyMuPDFLoader for PDF files
            else:
                return None
        except Exception as e:
            self.app_settings.logger.error(f"Error loading document: {e}")
            return None

    
    def split_documents_and_get_chunks_for_each_doc(self,
                                                    docs: list[PyMuPDFLoader.load] | list[TextLoader.load],
                                                    request_process_schema: FileProcessRequestSchema
                                                    ) -> list[RecursiveCharacterTextSplitter.create_documents]:
        doc_text_chunks = [doc.page_content for doc in docs]
        doc_metadats = [doc.metadata for doc in docs]

        if doc_text_chunks:
            try :
                return RecursiveCharacterTextSplitter(
                            chunk_size = request_process_schema.chunk_size,
                            chunk_overlap = request_process_schema.overlap_size,
                            length_function=len
                        ).create_documents(
                            doc_text_chunks,
                            metadatas = doc_metadats
                        )
            except Exception as e:
                self.app_settings.logger.error(e)
                return None
        else:
            return None
            
    def process_single_file(self, 
                            process_request_schema: FileProcessRequestSchema
                            ) -> Union[RecursiveCharacterTextSplitter.create_documents, None]:
        
        self.file_empty_msg_or_cannot_parsed_msg = Constants.EmptyDocumentResponse.value.format(process_request_schema.written_file_name)
        
        written_file_path = os.path.join(self.project_path, process_request_schema.written_file_name)
        if os.path.exists(written_file_path):
            docs = self.load_documents(written_file_path) 
            doc_chunks = self.split_documents_and_get_chunks_for_each_doc(docs, process_request_schema) 
            response_list = doc_chunks if doc_chunks else self.file_empty_msg_or_cannot_parsed_msg
            return response_list
        else:
            self.app_settings.logger.info(self.file_empty_msg_or_cannot_parsed_msg)
            return None
        