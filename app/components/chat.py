import streamlit as st
from langchain.callbacks.tracers.run_collector import RunCollectorCallbackHandler
from langchain.schema.runnable import RunnableConfig
from langchain.callbacks.tracers.langchain import wait_for_all_tracers
from langsmith import Client
from app.components.feedback import user_feedback, reset_feedback
from app.langchain.chains import qa_chain

client = Client()
run_collector = RunCollectorCallbackHandler()
runnable_config = RunnableConfig(
    callbacks=[run_collector],
    tags=["GitDoc-AI"],
)

def initialise():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "trace_link" not in st.session_state:
        st.session_state.trace_link = None
    if "run_id" not in st.session_state:
        st.session_state.run_id = None

def display_source(document):
    metadata_list = [{**doc[0].metadata, "score":doc[1]} for doc in document]
    
    with st.expander("Source Documents"):
        col1, col2, col3, col4 = st.columns(4)
        col1.markdown("**Page: " + str(metadata_list[0]["page"]) + "** *" + metadata_list[0]["file"] + "*" + " Score: " + str(metadata_list[0]["score"]))
        col2.markdown("**Page: " + str(metadata_list[1]["page"]) + "** *" + metadata_list[1]["file"] + "*" + " Score: " + str(metadata_list[1]["score"]))
        col3.markdown("**Page: " + str(metadata_list[2]["page"]) + "** *" + metadata_list[2]["file"] + "*" + " Score: " + str(metadata_list[2]["score"]))
        col4.markdown("**Page: " + str(metadata_list[3]["page"]) + "** *" + metadata_list[3]["file"] + "*" + " Score: " + str(metadata_list[3]["score"]))

def display_chat(chain=qa_chain, input_format=None, output_format=None):
    initialise()
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if message["role"] == "assistant":
                    if message["source"] is not None:
                        display_source(message["source"])

    if prompt := st.chat_input("Enter you question..."):
        user_content = "```"+input_format+"\n" + prompt + "\n```" if input_format is not None else prompt
        st.session_state.messages.append({"role": "user", "content": user_content})
        with st.chat_message("user"):
            st.markdown(user_content)
        
        reset_feedback()
        response, source = chain(prompt, runnable_config)

        with st.chat_message("assistant"):
            assistant_content = "```"+output_format+"\n" + response + "\n```" if output_format is not None else response
            st.markdown(assistant_content)
            if source is not None:
                display_source(source)
        st.session_state.messages.append({"role": "assistant", "content": assistant_content, "source": source})

        if st.session_state.is_guardrail is False:
            run = run_collector.traced_runs[0]
            run_collector.traced_runs = []
            st.session_state.run_id = run.id
            wait_for_all_tracers()
            url = client.share_run(run.id)
            st.session_state.trace_link = url

    if st.session_state.is_guardrail is False:
        user_feedback(client)