# travel guide powered by openai by Belghini - version July 2023


import os
import openai
import streamlit as st
import requests
import base64


# Connect to OpenAI GPT-3, fetch API key from Streamlit secrets
#openai.api_key = os.getenv("OPENAI_API_KEY")

#or enter the api key here
#openai.api_key = OPENAI_API_KEY

Model= "text-davinci-003"

github_token = st.secrets.github_token
repo_owner = st.secrets.repo_owner
repo_name = st.secrets.repo_name
file_path = st.secrets.file_path


# DESIGN implement changes to the standard streamlit UI/UX
st.set_page_config(page_title="travel plans", page_icon="My_logo.png",)
# Design hide top header line
hide_decoration_bar_style = '''<style>header {visibility: hidden;}</style>'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
# Design hide "made with streamlit" footer menu area
hide_streamlit_footer = """<style>#MainMenu {visibility: hidden;}
                        footer {visibility: hidden;}</style>"""
st.markdown(hide_streamlit_footer, unsafe_allow_html=True)
welcome_title = '<center style="font-family:Courier; color:Orange; font-size: 35px;">Generate travel plans - powered by OpenAI</>'
st.markdown(welcome_title, unsafe_allow_html=True)
st.write('\n')  # add spacing

# Set the width of the sidebar
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        width: 300px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
openai.api_key = st.sidebar.text_input('OpenAI API Key', type='password')
if openai.api_key=="":
    st.sidebar.write("You do not provide an API key. Please enter your openai key")
st.sidebar.write('\n')
st.sidebar.write("<a href='https://platform.openai.com/account/api-keys' id='api_link'>Generate you own API key by clicking here</a>", unsafe_allow_html=True)
st.sidebar.write('\n')


bmc_button_html = """
<div style="display: flex; justify-content: center; align-items: center; height: 100%;">
    <script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js"
        data-name="bmc-button" data-slug="naouarbelgx" data-color="#FFDD00" data-emoji=""
        data-font="Cookie" data-text="Buy me a coffee" data-outline-color="#000000"
        data-font-color="#000000" data-coffee-color="#ffffff">
    </script>
</div>
"""

# Display the Buy Me a Coffee button HTML in the sidebar

with st.sidebar:
    st.components.v1.html(bmc_button_html, height=70)

st.sidebar.write("So I can keep it alive. Thank you!")
st.sidebar.image("bmc_qr.png")

def gen_post(source_destination, nb_days, budget, destination):

    response = openai.Completion.create(
        engine=Model,

##        prompt=f"As a travel agent,propose 10 best of travel plans of {nb_days} days from {source_destination} city to other cities on the world with a budget of {budget} $ ",


        prompt=f"you are a travel agent, design 5 top travel plans (with etailed travel program) of {nb_days} days from {source_destination} to other destination over the world for a budget of {budget} $"
        "\ complete the travel plan with flight cost with aerien compagny, accommodation cost per day  , meals cost per day, 5 traditionnal meals proposition,"
        "\ detailed itinerary program."
        "\reply with organized markdown table"
        "\add new table that proposes flight company and hotel recommendations based on best rated",
        
        temperature=0.8,
        max_tokens=3000,
        top_p=0.8,
        best_of=2,
        frequency_penalty=0.0,
        presence_penalty=0.0)

    return response.get("choices")[0]['text']

def update_github_file(data):

    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    headers = {
        "Authorization": f"token {github_token}"
    }

    response = requests.get(url, headers=headers)
    file_data = response.json()

    if "content" in file_data:
        decoded_content = base64.b64decode(file_data["content"]).decode("utf-8")
    else:
        decoded_content = ""

    form_data = f"{decoded_content}\n\n{data}"
    encoded_form_data = base64.b64encode(form_data.encode("utf-8")).decode("utf-8")

    payload = {
        "message": "Update contact form data",
        "content": encoded_form_data,
        "sha": file_data["sha"]
    }

    update_response = requests.put(url, json=payload, headers=headers)
    return update_response.status_code

def main_send_message():
    st.subheader("Contact me for any personalized request")
    message = st.text_area("Message")
    
    if st.button("Submit"):
        form_data = f"Message: {message}"
        status_code = update_github_file(form_data)

        if status_code == 200:
            st.success("Form submitted successfully!")
        else:
            st.error("An error occurred while updating the file.")

def main_gpt_post_generator():

    st.image('banner_travel.png')  # Ttitle
    
    st.write('\n')  # add spacing

    st.subheader('\n Are you looking for destinations that fits your budget ?\n')

    post_text = ""  # initialize columns variables

    input_destination = st.text_input('Where are you now? (your current city)')
    input_days = st.text_input('Trip duration (in days)')
    input_budget = st.text_input('What is your budget ($) ')

    col1, col2, col3 = st.columns([10, 10, 10])
    with col1:
        pass
    with col3:
        pass
    with col2 :
        if st.button('create travel plan'):
            if openai.api_key=="":
                st.warning("You do not provide an API key. Please enter your openai key")
            else:
                with st.spinner():
                    post_text = gen_post(input_destination, input_days, input_budget, 'any')
    if post_text != "":
        st.write('\n')  # add spacing
        with st.expander("Travel plans", expanded=True):
            st.markdown(post_text)  #output the results

    welcome_title = '<center style="font-family:Courier; color:Gray; font-size: 35px;">Plan your next trip now...</>'
    st.markdown(welcome_title, unsafe_allow_html=True)
    st.image('benefits_ai.png')  # services

if __name__ == '__main__':
    main_gpt_post_generator()
    main_send_message()
