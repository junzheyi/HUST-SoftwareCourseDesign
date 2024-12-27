# -*- coding: utf-8 -*-
# @Time    : 2024/12/27 14:07
# @Author  : Junzhe Yi
# @File    : ask_questions_online.py
# @Software: PyCharm
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Milvus
from langchain.chains import RetrievalQA
from libs import qa_template, qa_template_zephyr, qa_template_phi
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import streamlit as st
from langchain_community.llms import HuggingFaceHub
from langchain_ibm import WatsonxLLM

def set_qa_prompt():
    prompt = PromptTemplate(template=qa_template,
                            input_variables=['context', 'question'])
    return prompt


def set_qa_prompt_zephyr():
    prompt = PromptTemplate(template=qa_template_zephyr,
                            input_variables=['context', 'question'])
    return prompt


def set_qa_prompt_phi():
    prompt = PromptTemplate(template=qa_template_phi,
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


def ask_question_openai(query_text, api_key):
    top_k = 3
    search_parameters = {
        "metric_type": "COSINE",
        "offset": 0,
        "ignore_growing": False,
        "params": {"ef": 32}
    }
    model_name = st.secrets.LLM.SentenceTransformer_model
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    connection_args = {"uri": st.secrets.MILVUS.public_end_point,
                       "token": st.secrets.MILVUS.zila_api_key,
                       "user": st.secrets.MILVUS.zila_cloud_user,
                       "password": st.secrets.MILVUS.zila_cloud_password
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


    retriever = vector_db.as_retriever(search_kwargs={'k': top_k,
                                                      "additional": ["certainty"],
                                                      "score_threshold": 0.9
                                                      },
                                       search_type="similarity"
                                       )
    qa_prompt = set_qa_prompt()

    openai_llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                            temperature=0,
                            openai_api_key=api_key
                            )
    dbqa = build_retrieval_qa(openai_llm, qa_prompt, retriever)
    llm_response = dbqa.invoke(query_text)
    return llm_response


def ask_question_zephyr(query_text):
    top_k = 3
    search_parameters = {
        "metric_type": "COSINE",
        "offset": 0,
        "ignore_growing": False,
        "params": {"ef": 32}
    }
    model_name = st.secrets.LLM.SentenceTransformer_model
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    connection_args = {"uri": st.secrets.MILVUS.public_end_point,
                       "token": st.secrets.MILVUS.zila_api_key,
                       "user": st.secrets.MILVUS.zila_cloud_user,
                       "password": st.secrets.MILVUS.zila_cloud_password
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

    retriever = vector_db.as_retriever(search_kwargs={'k': top_k,
                                                      "additional": ["certainty"],
                                                      "score_threshold": 0.9
                                                      },
                                       search_type="similarity"
                                       )
    qa_prompt = set_qa_prompt()

    zephyr_llm = HuggingFaceHub(repo_id="HuggingFaceH4/zephyr-7b-beta",
                                model_kwargs={"temperature": 0.001,
                                              "max_new_tokens": 512,
                                              "repetition_penalty": 1.1,
                                              "max_length": 64,
                                              "top_p": 0.9,
                                              "return_full_text": False
                                              },
                                huggingfacehub_api_token=st.secrets.HUGGINGFACE.hf_api_token
                                )
    dbqa = build_retrieval_qa(zephyr_llm, qa_prompt, retriever)
    llm_response = dbqa.invoke(query_text)
    return llm_response


def ask_question_mistral(query_text):
    top_k = 3
    search_parameters = {
        "metric_type": "COSINE",
        "offset": 0,
        "ignore_growing": False,
        "params": {"ef": 32}
    }
    model_name = st.secrets.LLM.SentenceTransformer_model
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    connection_args = {"uri": st.secrets.MILVUS.public_end_point,
                       "token": st.secrets.MILVUS.zila_api_key,
                       "user": st.secrets.MILVUS.zila_cloud_user,
                       "password": st.secrets.MILVUS.zila_cloud_password
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

    retriever = vector_db.as_retriever(search_kwargs={'k': top_k,
                                                      "additional": ["certainty"],
                                                      "score_threshold": 0.9
                                                      },
                                       search_type="similarity"
                                       )
    qa_prompt = set_qa_prompt()

    mistral_llm = HuggingFaceHub(repo_id="mistralai/Mistral-7B-Instruct-v0.2",
                                 model_kwargs={"temperature": 0.001,
                                               "max_new_tokens": 512,
                                               "repetition_penalty": 1.1,
                                               "max_length": 64,
                                               "top_p": 0.9,
                                               "return_full_text": False
                                               },
                                 huggingfacehub_api_token=st.secrets.HUGGINGFACE.hf_api_token
                                 )
    dbqa = build_retrieval_qa(mistral_llm, qa_prompt, retriever)
    llm_response = dbqa.invoke(query_text)
    return llm_response


def ask_question_phi3(query_text):
    top_k = 3
    search_parameters = {
        "metric_type": "COSINE",
        "offset": 0,
        "ignore_growing": False,
        "params": {"ef": 32}
    }
    model_name = st.secrets.LLM.SentenceTransformer_model
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    connection_args = {"uri": st.secrets.MILVUS.public_end_point,
                       "token": st.secrets.MILVUS.zila_api_key,
                       "user": st.secrets.MILVUS.zila_cloud_user,
                       "password": st.secrets.MILVUS.zila_cloud_password
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

    retriever = vector_db.as_retriever(search_kwargs={'k': top_k,
                                                      "additional": ["certainty"],
                                                      "score_threshold": 0.9
                                                      },
                                       search_type="similarity"
                                       )
    qa_prompt = set_qa_prompt_phi()

    phi3_llm = HuggingFaceHub(repo_id="microsoft/Phi-3-mini-4k-instruct",
                              model_kwargs={"temperature": 0.001,
                                            "max_new_tokens": 512,
                                            "trust_remote_code": True,
                                            "repetition_penalty": 1.1,
                                            "max_length": 64,
                                            "return_full_text": False
                                            },
                              huggingfacehub_api_token=st.secrets.HUGGINGFACE.hf_api_token
                              )
    dbqa = build_retrieval_qa(phi3_llm, qa_prompt, retriever)
    llm_response = dbqa.invoke(query_text)
    return llm_response


def ask_question_granite(query_text):
    top_k = 3
    search_parameters = {
        "metric_type": "COSINE",
        "offset": 0,
        "ignore_growing": False,
        "params": {"ef": 32}
    }

    parameters = {
        "temperature": 0.001,
        "decoding_method": "greedy",
        "max_new_tokens": 512,
        "min_new_tokens": 1,
        "stop_sequences": [],
        "repetition_penalty": 1.05

    }

    model_name = st.secrets.LLM.SentenceTransformer_model
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    connection_args = {"uri": st.secrets.MILVUS.public_end_point,
                       "token": st.secrets.MILVUS.zila_api_key,
                       "user": st.secrets.MILVUS.zila_cloud_user,
                       "password": st.secrets.MILVUS.zila_cloud_password
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

    retriever = vector_db.as_retriever(search_kwargs={'k': top_k,
                                                      "additional": ["certainty"],
                                                      "score_threshold": 0.9
                                                      },
                                       search_type="similarity"
                                       )
    qa_prompt = set_qa_prompt()

    project_id = st.secrets.WATSONX.project_id
    credentials = {
        "url": st.secrets.WATSONX.url,
        "apikey": st.secrets.WATSONX.apikey
    }
    watsonx_granite = WatsonxLLM(
        model_id="ibm/granite-13b-chat-v2",
        url=credentials.get("url"),
        apikey=credentials.get("apikey"),
        project_id=project_id,
        params=parameters
    )
    dbqa = build_retrieval_qa(watsonx_granite, qa_prompt, retriever)
    llm_response = dbqa.invoke(query_text)
    return llm_response