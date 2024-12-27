# -*- coding: utf-8 -*-
# @Time    : 2024/12/27 15:24
# @Author  : Junzhe Yi
# @File    : semantic_search.py
# @Software: PyCharm

from sentence_transformers import SentenceTransformer

from libs.read_config import ReadConfig
from pymilvus import (Collection, connections, utility)
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Milvus


def milvus_vector_search_book(user_query):
    my_config = ReadConfig("config/config.ini")
    model_name = my_config.SentenceTransformer_model
    model = SentenceTransformer(model_name)
    top_k = int(my_config.search_top_k)
    search_parameters = {
        "metric_type": "COSINE",
        "offset": 0,
        "ignore_growing": False,
        "params": {"ef": 32}
    }
    user_query_embedding = model.encode(user_query)
    connections.connect("default",
                        host=my_config.host,
                        port=int(my_config.port),
                        user=my_config.user,
                        password=None,
                        show_startup_banner=True
                        )
    print("Connected to Milvus!")
    print("Database Version: ", utility.get_server_version())
    milvus_collection = Collection("PythonBooks")
    milvus_collection.load()
    results = milvus_collection.search(
        data=[user_query_embedding],
        anns_field="book_chunk_vec",
        param=search_parameters,
        output_fields=["book_name", "book_author", "book_chunk"],
        limit=top_k
    )
    milvus_collection.release()
    connections.disconnect("default")
    return results


def milvus_vector_search_langchain_book(user_query):
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
    docs = vector_db.similarity_search_with_score(query=user_query, k=top_k)
    return docs


if __name__ == '__main__':
    my_query = input("What is your query:")
    search_results = milvus_vector_search_book(my_query)
    for hits_i, hits in enumerate(search_results):
        print('Results:')
        print("=============")
        for rank, hit in enumerate(hits):
            print("\033[92m Rank: \033[0;0m", rank+1)
            print("\033[92m========\033[0;0m")
            print("\033[92m Chunk: \033[0;0m", hit.entity.get('book_chunk'))
            print('\033[38;5;208mScore: ====>\033[0;0m', hit.distance)
            print("*"*40)