# import setting
import streamlit as st
import pandas as pd
import time
import random

df = pd.read_csv("csv\keypoint.csv")
dict_df = df.to_dict(orient='records')

with st.expander("这是对这个网站的一些解释"):
        st.markdown("主要的做题方式是选择**start**的按钮，获得5个随机的题目，但是这五个题目可能会出现一个或者两个一样的题目\
当做完题后使用**submit**来提交题目，并获得每个题目的解释，最后使用**reload**重新获得题目")

st.title("知识点刷题网站")


# 定义空白页面
def nl(num_of_lines):
    for i in range(num_of_lines):
        st.write(" ")


st.markdown("*问题描述* ")
scorecard_placeholder = st.empty()

# Activate Session States
ss = st.session_state
# Initializing Session States
if 'counter' not in ss:
    ss['counter'] = 0
if 'start' not in ss:
    ss['start'] = False
if 'stop' not in ss:
    ss['stop'] = False
if 'refresh' not in ss:
    ss['refresh'] = False
if "button_label" not in ss:
    ss['button_label'] = ['START', 'SUBMIT', 'RELOAD']
if 'current_quiz' not in ss:
    ss['current_quiz'] = {}
if 'user_answers' not in ss:
    ss['user_answers'] = []
if 'grade' not in ss:
    ss['grade'] = 0


# Function for button click
def btn_click():
    ss.counter += 1
    if ss.counter > 2:
        ss.counter = 0
        ss.clear()
    else:
        update_session_state()
        with st.spinner("*this may take a while*"):
            time.sleep(2)


# Function to update current session
def update_session_state():
    if ss.counter == 1:
        ss['start'] = True
        ss.current_quiz = random.sample(dict_df, 1)
    elif ss.counter == 2:
        # Set start to False
        ss['start'] = True
        # Set stop to True
        ss['stop'] = True


st.button(label=ss.button_label[ss.counter], key='button_press', on_click=btn_click)


# Function to display a question
def quiz_app():
    # create container
    with st.container():
        if (ss.start):
            for i in range(len(ss.current_quiz)):
                number_placeholder = st.empty()
                question_placeholder = st.empty()
                results_placeholder = st.empty()
                expander_area = st.empty()
                # Add '1' to current_question tracking variable cause python starts counting from 0
                current_question = i + 1
                # display question_number
                number_placeholder.write(f"*问题{current_question}*")
                # display question based on question_number
                question_placeholder.write(f"**{ss.current_quiz[i].get('question')}**")
                nl(2)
                # Grade Answers and Return Corrections
                if ss.stop:
                    # Track length of user_answers
                    if len(ss.user_answers) < 10:
                        # comparing answers to track score
                        if True:
                            ss.user_answers.append(True)
                        else:
                            ss.user_answers.append(False)
                    else:
                        pass
                    # Results Feedback
                    if ss.user_answers[i] == True:
                        results_placeholder.success("恭喜你做完啦，快看看和你心中的答案是不是符合吧")
                    else:
                        results_placeholder.error("INCORRECT")
                    # Explanation of the Answer
                    expander_area.write(f"*{ss.current_quiz[i].get('explanation')}*")

    # calculate score
    if ss.stop:
        ss['grade'] = ss.user_answers.count(True)
        scorecard_placeholder.write(f"### **你答对的题目有: {ss['grade']} / {len(ss.current_quiz)}**")


quiz_app()
