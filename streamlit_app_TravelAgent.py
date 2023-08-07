# travel guide powered by openai by Belghini - version July 2023


import os
import openai
import streamlit as st


# Connect to OpenAI GPT-3, fetch API key from Streamlit secrets
openai.api_key = os.getenv("OPENAI_API_KEY")

#or enter the api key here
openai.api_key = "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"

Model= "text-davinci-003"


# DESIGN implement changes to the standard streamlit UI/UX
st.set_page_config(page_title="travel plans", page_icon="ai_travel.png",)
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

def gen_post(source_destination, nb_days, budget, destination):

    response = openai.Completion.create(
        engine=Model,

##        prompt=f"As a travel agent,propose 10 best of travel plans of {nb_days} days from {source_destination} city to other cities on the world with a budget of {budget} $ ",


        prompt=f"you are a travel agent, design 5 top travel plans (with etailed travel program) of {nb_days} days from {source_destination} to other destination over the world for a budget of {budget} $"
              "\ complete the travel plan with flight cost with aerien compagny, accommodation cost per day  , meals cost per day, 5 traditionnal meals proposition,"
                "\ detailed itinerary program."
        "\reply with organized table",
        
        temperature=0.8,
        max_tokens=3000,
        top_p=0.8,
        best_of=2,
        frequency_penalty=0.0,
        presence_penalty=0.0)

    return response.get("choices")[0]['text']


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
