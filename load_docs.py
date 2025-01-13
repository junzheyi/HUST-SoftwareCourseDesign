# -*- coding: utf-8 -*-
# @Time    : 2024/12/27 17:15
# @Author  : Junzhe Yi
# @File    : load_docs.py
# @Software: PyCharm
from libs import load_python_book_into_milvus
import sys
# this script is used to load the docs into milvus vector store, three argv needed to be input.
# for example "C:\junzheyi\python_tutorial.docx" "Python Tutorial" "Junzhe Yi"

if __name__ == '__main__':
    help_text = """ 
                You have to pass at least one parameter. Three parameters can be passed.
                They are filename with path, book name and author. 
                If you don't know the book name and author please pass it as "Unknown"
                Example: python load_docs.py "C:\\xyz.docx" "My Book" "junzheyi" 
                         python load_docs.py "C:\\xyz.docx" "Unknown" "yijunzhe"
                """
    # At least one parameter is required.
    if len(sys.argv[1:]) == 0:
        print(help_text)
        sys.exit(0)

    # Exactly three parameters expected.
    if len(sys.argv[1:]) != 3:
        print(help_text)
        sys.exit(0)

    if len(sys.argv[1:]) == 3:
        print(sys.argv[1])
        print(sys.argv[2])
        print(sys.argv[3])
    load_python_book_into_milvus(sys.argv[1],
                                 sys.argv[2],
                                 sys.argv[3]
                                 )
