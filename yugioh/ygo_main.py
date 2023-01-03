'''    
#usage example
yugioh = ygo_main(openai)

description = """a 6 star effect monster card,
            we want a frozen theme, the main theme effects are to put opponent cards into frozen state,
            a magic or trap card in frozen state cannot be activated,
            a monster in frozen state cannot attack, change positions, 
            activate its effects or be used as materials for normal or special summons"""

yugioh.generate_card(description)
yugioh.generate_gameplay()
'''

import sys
sys.path.append('./yugioh/')
sys.path.append('../')

import openai
import yugioh.ygo_card
import yugioh.ygo_openai

class ygo_main:
    def __init__(self, openai, save=True):
        self.ygo = ygo_openai.openai_yugioh(openai)
        self.save_image = save
        self.deck = []
        
    def generate_card(self, description):
        card_data = self.ygo.generate_card_data(description)
        ygocard = ygo_card.card_yugioh(card_data, self.save_image)
        self.deck.append(ygocard)
        return
    
    def generate_gameplay_prompt(self):
        prompt = ['Generate a yugioh gameplay strategy where the player wins in two turns with these cards.']
        for card in self.deck:
            text = [f"{key}: {value}" for key, value in card.card_data.items() if key not in ["Image","image_url"]]
            prompt.append(' \n'.join(text))
        
        print(prompt)            
        return ' '.join(prompt)
    
    def generate_gameplay(self):
        text = self.generate_gameplay_prompt()

        text_length = len(text.split(' '))+50

        response = self.ygo.openai_session.Completion.create(
          model="text-davinci-003",
          prompt=text,
          temperature=0.9,
          max_tokens=4000-text_length,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0.6,
          stop=[" Human:", " AI:"]
        )
        
        res = response.choices[0].text
        print(res)
        return str(res)
