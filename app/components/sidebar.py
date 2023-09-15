import streamlit as st

# Define the available model options in the side navbar
model_options = {
    "GPT-3 Turbo-16k": "gpt-3.5-turbo-16k",
    "GPT-4": "gpt-4",
    "GPT-3 Turbo": "gpt-3.5-turbo",
    "GPT-3": "text-davinci-003"
}

def convert_decimal(value):
    converted_value = "{:.1f}".format(value).rstrip("0").rstrip(".")
    return converted_value

def set_openai_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key

def set_selected_model_option(selected_model_option: str):
    st.session_state["selected_model_option"] = model_options[selected_model_option]

def sidebar(isModel=True):
    with st.sidebar:
        st.markdown("## **Instructions** 🔧")
        st.markdown(
            "Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below 🔑\n"
        )
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="Paste your OpenAI API key here (sk-...)",
            help="You can get your API key from https://platform.openai.com/account/api-keys.",
            value=st.session_state.get("OPENAI_API_KEY", ""),
        )

        if api_key_input:
            set_openai_api_key(api_key_input)
        
        if isModel:
            selected_model_option = st.sidebar.selectbox("Select a model", list(model_options.keys()))
            
            if selected_model_option:
                set_selected_model_option(selected_model_option)

        with st.expander("More settings", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.checkbox('Memory', value=False, key='memory')
            with col2:
                st.checkbox("Guardrail", value=False, key="is_guardrail")
                
            temperature = st.slider('Temperature', min_value=0.0, max_value=1.0, step=0.1, value=0.0)
            if isModel:
                max_tokens = st.slider('Max Tokens', min_value=0, max_value=8000, value=1000)
            else:
                max_tokens = st.slider('Max Tokens', min_value=0, max_value=8000, value=350)
            st.session_state["temperature"] = float(convert_decimal(temperature))
            st.session_state["max_tokens"] = int(convert_decimal(max_tokens))
