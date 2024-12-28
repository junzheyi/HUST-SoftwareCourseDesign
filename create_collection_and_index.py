# -*- coding: utf-8 -*-
# @Time    : 2024/12/27 15:56
# @Author  : Junzhe Yi
# @File    : create_collection_and_index.py
# @Software: PyCharm

# this script is used to create collections and indexes in Milvus, you need to make sure
# - the config file has been set successfully.
from libs import (connect_to_milvus,
                  create_milvus_collection,
                  create_milvus_collection_v2,
                  create_vector_index,
                  disconnect_from_milvus
                  )
from pymilvus import utility

if __name__ == '__main__':
    milvus_connection = connect_to_milvus("default")
    milvus_collection = create_milvus_collection("PythonQA", milvus_connection)
    milvus_collection_v2 = create_milvus_collection_v2("PythonBooks", milvus_connection)
    print("Collections: ", utility.list_collections())
    index_params = {
        "metric_type": "COSINE",
        "index_type": "HNSW",
        "params": {"M": 16,
                   "efConstruction": 32
                   },
        "index_name": "PythonQA_HNSW"
    }
    create_vector_index(milvus_collection, "question_vec", index_params)
    index_params = {
        "metric_type": "COSINE",
        "index_type": "HNSW",
        "params": {"M": 16,
                   "efConstruction": 32
                   },
        "index_name": "PythonBooks_HNSW"
    }
    index_params_ivf = {
        'metric_type': 'L2',
        'index_type': "IVF_FLAT",
        'params': {'nlist': 1536}
    }
    create_vector_index(milvus_collection_v2, "book_chunk_vec", index_params)
    print("Indexes: ", utility.list_indexes("PythonQA"),
          utility.list_indexes("PythonBooks")
          )
    disconnect_from_milvus(milvus_connection)
