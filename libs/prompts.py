# -*- coding: utf-8 -*-
# @Time    : 2024/12/27 15:20
# @Author  : Junzhe Yi
# @File    : prompts.py
# @Software: PyCharm
qa_template = """Use the following pieces of context to answer the user's question.
If you don't know the answer based on the context only, just say that you don't know, don't try to make up an answer.
Give the reference document or link if available. Give explanation if available. Think step by step.

Context: {context}
Question: {question}

Only return the helpful answer then reference / explanation each in new line below and nothing else.
If you don't know the answer based on the context say you don't know.
Helpful answer:

"""
qa_template_zephyr = """
<|system|>
Using the information contained in the context, 
give a concise answer to the question, If the answer is contained in the context, also report the reference URL.
If the answer cannot be deduced from the context say I don't know.
</s>
<|user|>
Context: {context}
Question: {question}
Remember only return AI answer
</s>
<|assistant|>
"""

qa_template_phi = """
<|system|>
Using the information contained in the context, 
give a concise answer to the question, If the answer is contained in the context, also report the reference URL.
If the answer cannot be deduced from the context say I don't know.
<|end|>
<|user|>
Context: {context}
Question is below. Remember only return AI answer
Question: {question}
<|end|>
<|assistant|>
"""