# -*- coding: utf-8 -*-
# @Time    : 2024/12/27 15:15
# @Author  : Junzhe Yi
# @File    : local_llm.py
# @Software: PyCharm

from langchain_community.llms import CTransformers
from libs.read_config import ReadConfig

# Local CTransformers wrapper for Llama-2-7B-Chat
my_config = ReadConfig("config/config.ini")
try:
    local_llm = CTransformers(model=my_config.llm_path,
                          model_type='llama',  # Model type Llama
                          config={'max_new_tokens': int(my_config.max_new_tokens),
                                  'temperature': float(my_config.temperature),
                                  'context_length': int(my_config.context_length)})
    # local_llm = None
except Exception as err:
    local_llm = None
    pass

if __name__ == '__main__':
    print(type(local_llm))