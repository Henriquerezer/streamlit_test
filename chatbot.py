import streamlit as st
import openai
import os

from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]

## SIDEBAR

st.sidebar.title('Configuração')

def model_callback():
    st.session_state['model'] = st.session_state['model_selection']

#Iniciando o modelo
if "model" not in st.session_state:
    st.session_state.model = "gpt-3.5-turbo"

st.session_state.model = st.sidebar.radio(
    "Escolha o Modelo",
    ("gpt-3.5-turbo","gpt-3.5-turbo-16k"),
    index=0 if st.session_state['model'] else 1,
    on_change=model_callback,
    key='model_selection',
)

bot_roles = {
    "Odonto bot":{
        "role": "system",
        "content": "Eu sou seu assistente especializado em conteúdo Bucomaxilofacial. Como posso lhe ajudar?",
        "description": "Você falará apenas em português brasileiro. Você é um assistente de um curso chamado Buco Approve, e sua função é ajudar os alunos com a resolução de questões de editais, referentes a residência odontológica na área de cirurgião bucomaxilofacial. Sempre termine a sua frase, falando que está disponível para mais questionamentos!",
    },
        "Coder bot": {
        "role": "system",
        "content": "You will be a bot that helps with code resolution in python, sql and dax.",
        "description": "You will speak in Brazilian Portuguese, and you will help the user with the creation, explanation, documentation and correction of codes in Python, SQL and DAX.",
    }
}

def bot_role_calback():
    st.session_state['bot_role'] = st.session_state['bot_role_selected']
    st.session_state['messages'] = [bot_roles[st.session_state["bot_role"]]]

if 'bot_role' not in st.session_state:
    st.session_state['bot_role'] = "Odonto bot"

st.session_state.bot_role = st.sidebar.radio(
    "Select bot role",
    tuple(bot_roles.keys()),
    index=list(bot_roles.keys()).index(st.session_state["bot_role"]),
    on_change=bot_role_calback,
    key='bot_role_selected'

)

###APP PRINCIPAl###
st.title("Bem Vindo ao Chatbot do BucoAprove!🤖")

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# initialize model
#if "model" not in st.session_state:
#    st.session_state.model = "gpt-3.5-turbo"

# user input
if user_prompt := st.chat_input("Escreva sua Mensagem"):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # generate responses
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        for response in openai.ChatCompletion.create(
            model=st.session_state.model,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
