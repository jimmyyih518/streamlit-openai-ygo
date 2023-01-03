import openai
from yugioh.ygo_main import ygo_main
import streamlit as st
from PIL import Image
from io import BytesIO
import base64
import sys
sys.path.append('./yugioh/')
sys.path.append('../')

st.set_page_config(layout="wide", page_title="Yugioh Card Generator")

def main():
    if 'ygo' not in st.session_state:
        st.session_state['ygo'] = ygo_main(openai)
    header()
    sidebar(st.session_state.ygo)
    page(st.session_state.ygo)

def header():
    st.write("## Generate Yugioh Cards")

def sidebar(ygo):

    st.sidebar.write("## Create your card :gear:")
    st.sidebar.markdown("\n")
    description = st.sidebar.text_input(label="Description", placeholder="""a 6 star effect monster card,
                we want a frozen theme, the main theme effects are to put opponent cards into frozen state,
                a magic or trap card in frozen state cannot be activated,
                a monster in frozen state cannot attack""")
        
    generate_button = st.sidebar.button(label="Generate")
    
    if generate_button:
        try_counter = 0
        while try_counter <= 2:
            try:
                ygo.generate_card(description)
                break
            except:
                try_counter += 1


def page(ygo):
    
    mainpage = st.container()
    mainpage.write("Generated Yugioh Cards")
    gameplay_button = st.button("Generate Gameplay Strategy")
    if gameplay_button:
        if len(ygo.deck) < 3:
            mainpage.write("Need at least 3 cards")
        else:
            mainpage.write(ygo.generate_gameplay())
    mainpage.image([card.card_template for card in ygo.deck])

# Run App
if __name__ == "__main__":
    main()