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
                                huggingfacehub_api_token=my_config.hf_api_token
                                )
    dbqa = build_retrieval_qa(zephyr_llm, qa_prompt, retriever)
    llm_response = dbqa.invoke(query_text)
    return llm_response


if __name__ == '__main__':
    query = input("Please enter the question: ")
    start_time = timeit.default_timer()
    response = ask_question_zephyr(query)

    # Displaying the outcome.
    print(f'\n\033[92m Answer: \033[0;0m {response["result"]}')
    print("\033[38;5;208m*******************************\033[0;0m")
    source_docs = response['source_documents']
    for i, doc in enumerate(source_docs):
        print(f'\nSource Document {i + 1}\n')
        print(f'Source Text: {doc.page_content}')
        print("\033[38;5;208m*******************************\033[0;0m")
    print('=' * 50)
    end_time = timeit.default_timer()
    total_time = (end_time - start_time) / 60
    print("Time to retrieve response %.2f(minute(s)):" % total_time)

