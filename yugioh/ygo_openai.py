import os
import openai

class openai_yugioh:
    def __init__(self, openai_session):
        self.openai_session = openai_session
        self.openai_session.api_key = os.getenv("API_KEY")
        
    def prompt_text(self, text):
        
        text_length = len(text.split(' '))+50

        response = self.openai_session.Completion.create(
          model="text-davinci-003",
          prompt=f"""\nHuman: make a new card that didn't exist before in yugioh, 
          {text}, 
          if the card is a monster, generate an attack and defense power according to its star level,
          otherwise if it is spell or trap card the Stars, Attack, and Defense are null,
          also generate a description of the image for this card,
          formate your response like below with no linebreaks,
          Title: title of card
          Effect: card effect
          Image: description of the image
          Stars: star rating
          Attack: attack power
          Defense: defense power
          """,
          temperature=0.9,
          max_tokens=4000-text_length,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0.6,
          stop=[" Human:", " AI:"]
        )
    
        res = response.choices[0].text
        print(res)
        res_proc = [x.split(':') for x in res.split('\n') if len(x)>0]
        res_proc = [[s.strip() for s in tup] for tup in res_proc]
        res_clean = []
        for tup in res_proc:
            if len(tup) == 2:
                res_clean.append(tup)
            elif len(tup) > 2:
                proc_tup = [tup[0], ' '.join(tup[1:])]
                res_clean.append(proc_tup)
        
        print(res_clean)
        return dict(res_clean)
    
    
    def prompt_image(self, text):

        response = self.openai_session.Image.create(
          prompt=f"Fit image to entire canvas with background matching the theme of image, no blank or black or white parts, this is a single Yugioh style image, {text}",
          n=1,
          size="1024x1024"
        )
        image_url = response['data'][0]['url']
        
        return image_url
    
    def generate_card_data(self, text):
        card_text = self.prompt_text(text)
        card_img_url = self.prompt_image(card_text['Image'])
        card_text['image_url'] = card_img_url
        return card_text
