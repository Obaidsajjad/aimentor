import streamlit as st
from itertools import zip_longest
from streamlit_chat import message
from langchain.schema import ( HumanMessage, SystemMessage, AIMessage)
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv('.env')
st.set_page_config(page_title="ubaisters")
st.title("AI Mentor")

if "entered_prompt" not in st.session_state:
    st.session_state["entered_prompt"]=""
if "generated" not in st.session_state:
    st.session_state["generated"]=[]
if "past" not in st.session_state:
    st.session_state["past"]=[]

chat=ChatGroq(
    model_name="Llama3-70b-8192",temperature=0.5,
    api_key="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",
    max_tokens=500,
    model_kwargs={
                    "top_p": 1,
                    "frequency_penalty": 0.5,
                    "presence_penalty": 0.5
                }
)

def build_message():
    zip_message=[SystemMessage(
        content="""your name is AI Mentor. You are an AI Technical Expert for Artificial Intelligence, here to guide and assist students with their AI-related questions and concerns. Please provide accurate and helpful information, and always maintain a polite and professional tone.

        1. Greet the user politely ask user name and ask how you can assist them with AI-related queries only for the first time.
        2. Provide informative and relevant responses to questions about artificial intelligence, machine learning, deep learning, natural language processing, computer vision, and related topics.
        3. you must Avoid discussing sensitive, offensive, or harmful content. Refrain from engaging in any form of discrimination, harassment, or inappropriate behavior.
        4. If the user asks about a topic unrelated to AI, politely steer the conversation back to AI or inform them that the topic is outside the scope of this conversation.
        5. Be patient and considerate when responding to user queries, and provide clear explanations.
        6. If the user expresses gratitude or indicates the end of the conversation, respond with a polite farewell.
        7. Do Not generate the long paragarphs in response. Maximum Words should be 100.

        Remember, your primary goal is to assist and educate students in the field of Artificial Intelligence. Always prioritize their learning experience and well-being."""
    )]
    for human_msg,ai_msg in zip_longest(st.session_state["past"], st.session_state["generated"]):
        if human_msg is not None:
            zip_message.append(HumanMessage(content=human_msg))
        if ai_msg is not None:
            zip_message.append(AIMessage(content=ai_msg))

    return zip_message

def generate_response():
    zip_messages=build_message()
    ai_res=chat(zip_messages)
    response=ai_res.content
    return response
# st.write(generate_res())

def submit():
    st.session_state.entered_prompt=st.session_state.prompt_input
    st.session_state.prompt_input=""

st.text_input("Enter your prompt here ...", key="prompt_input", on_change=submit)

if st.session_state.entered_prompt != "":
    user_query = st.session_state.entered_prompt
    st.session_state.past.append(user_query)
    output = generate_response()
    st.session_state.generated.append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
