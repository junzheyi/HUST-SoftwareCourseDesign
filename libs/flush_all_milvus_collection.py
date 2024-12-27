# -*- coding: utf-8 -*-
# @Time    : 2024/12/27 14:55
# @Author  : Junzhe Yi
# @File    : flush_all_milvus_collection.py
# @Software: PyCharm

from pymilvus import (Collection, connections, utility)
import sys

def flush_all_milvus_collection():
    try:
        connections.connect("default",
                            host="localhost",
                            port=19530,
                            user="root",
                            password=None,
                            show_startup_banner=True
                            )
        print("Connected to Milvus")
    except Exception as e:
        print("Problem in connecting to Milvus")
        print(e)
        sys.exit(0)

    all_collections = utility.list_collections()

    try:
        for collection in all_collections:
            print("Flushing & Compacting collection name: ", collection)


            milvus_collection = Collection(collection)

            print("\033[91m Load state before:\033[00m ", str(utility.load_state(collection)))
            if str(utility.load_state(collection)).strip() == "Loaded":
                print(utility.loading_progress(collection))
                print("Trying to unload...")
                milvus_collection.release()
                print("\033[92m Load state after:\033[00m ", utility.load_state(collection))

            milvus_collection.flush(timeout=None)
            milvus_collection.release()
            print("Finished flushing: ", collection)
            print("*"*40)
    except Exception as e:
        print("Problem in Flushing")
        print(e)


if __name__ == '__main__':
    flush_all_milvus_collection()