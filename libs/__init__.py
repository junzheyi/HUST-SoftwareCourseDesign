# -*- coding: utf-8 -*-
# @Time    : 2024/12/27 13:54
# @Author  : Junzhe Yi
# @File    : __init__.py
# @Software: PyCharm

from libs.flush_all_milvus_collection import flush_all_milvus_collection
import libs.read_config as read_config
from libs.milvus_utils import (connect_to_milvus,
                               create_milvus_collection,
                               create_milvus_collection_v2,
                               create_vector_index,
                               create_scalar_index,
                               disconnect_from_milvus,
                               connect_to_milvus_zila
                               )
from libs.load_books import load_python_book_into_milvus
from libs.semantic_search import milvus_vector_search_book, milvus_vector_search_langchain_book
from libs.prompts import qa_template, qa_template_zephyr, qa_template_phi
from libs.local_llm import local_llm
from libs.upload_s3 import upload_file
from libs.load_books_zila import load_python_book_into_milvus as load_python_book_into_zila
from libs.ask_questions_online import (ask_question_openai, ask_question_zephyr,
                                       ask_question_mistral, ask_question_phi3,
                                       ask_question_granite)
