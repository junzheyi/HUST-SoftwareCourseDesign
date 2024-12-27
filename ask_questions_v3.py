# -*- coding: utf-8 -*-
# @Time    : 2024/12/27 16:02
# @Author  : Junzhe Yi
# @File    : ask_questions_v3.py
# @Software: PyCharm

import timeit
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Milvus
from libs.read_config import ReadConfig
from langchain.chains import RetrievalQA
from libs import qa_template_zephyr
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceHub


def set_qa_prompt():
    prompt = PromptTemplate(template=qa_template_zephyr,
                            input_variables=['context', 'question'])
    return prompt


def build_retrieval_qa(_llm, prompt, _retriever):
    db_qa = RetrievalQA.from_chain_type(llm=_llm,
                                        chain_type='stuff',
                                        retriever=_retriever,
                                        return_source_documents=True,
                                        verbose=True,
                                        chain_type_kwargs={'prompt': prompt})
    return db_qa


def ask_question_zephyr(query_text):
    my_config = ReadConfig("config/config.ini")
    top_k = int(my_config.search_top_k)
    search_parameters = {
        "metric_type": "COSINE",
        "offset": 0,
        "ignore_growing": False,
        "params": {"ef": 32}
    }
    model_name = my_config.SentenceTransformer_model
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    connection_args = {"host": my_config.host,
                       "port": int(my_config.port),
                       "user": my_config.user,
                       "password": None
                       }

    vector_db: Milvus = Milvus(
        embedding_function=embeddings,
        collection_name="PythonBooks",
        search_params=search_parameters,
        connection_args=connection_args,
        text_field="book_chunk",
        vector_field="book_chunk_vec",
        consistency_level="Session"
    )
