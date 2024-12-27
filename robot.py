# -*- coding: utf-8 -*-
# @Time    : 2024/12/27 15:59
# @Author  : Junzhe Yi
# @File    : robot.py
# @Software: PyCharm

import streamlit as st
from libs import upload_file
from ask_questions_v1 import ask_question
from ask_questions_v2 import ask_question_openai
from ask_questions_v3 import ask_question_zephyr
import timeit


def main():
    st.set_page_config(page_title="Junzhe Yi!", page_icon=":books:")
    st.header("husteic-LawBot :books:")
    select_option = st.selectbox(
        r'$\textsf{\large What is the preferred LLM?}$',
        ('Local Llama2 - Run locally free but slower!', 'OpenAI - Faster and efficient - NOT free!',
         'HuggingFaceHub - zephyr-7b-beta'
         ),
        index=None,
        placeholder="Select your LLM..."
    )
    user_question = st.text_area(r"$\textsf{\large Ask LawBot a question:}$")
    if st.button("Ask LawBot", type="primary"):
        if user_question:
            st.write(user_question)
            start_time = timeit.default_timer()  # Start timer
            with st.spinner("LawBot is searching.."):
                if select_option == 'Local Llama2 - Run locally free but slower!':
                    response = ask_question(user_question)
                elif select_option == 'OpenAI - Faster and efficient - NOT free!':
                    response = ask_question_openai(user_question)
                elif select_option == 'HuggingFaceHub - zephyr-7b-beta':
                    response = ask_question_zephyr(user_question)
                else:
                    response = ask_question(user_question)
            with st.chat_message("assistant"):
                st.markdown(response["result"])
                end_time = timeit.default_timer()  # End timer
                total_time = (end_time - start_time) / 60
                st.markdown("Time to retrieve response %.2f minutes" % total_time)
            source_docs = response['source_documents']
            for i, doc in enumerate(source_docs):
                st.info(f'\nSource Document {i + 1}\n')
                st.info(f'Source Text: {doc.page_content}')

    with st.sidebar:
        st.subheader("You can upload you document here:")
        st.subheader("This will be uploaded to S3 for review. I will"
                     " upload the document if it passes my sanity check"
                     )
        upload_docs = st.file_uploader("Upload your Python pdf/docx books:",
                                       accept_multiple_files=True,
                                       type=["xlsx", "pdf", "doc", "docx", "md"]
                                       )
        if st.button("Submit for Review"):
            with st.spinner("Uploading to S3"):
                if upload_docs is not None:
                    for doc in upload_docs:
                        upload_file(doc)


if __name__ == '__main__':
    main()