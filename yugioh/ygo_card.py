from PIL import Image, ImageFont, ImageDraw
import requests
from io import BytesIO
import textwrap

class card_yugioh:
    def __init__(self, card=None, save=True):
        self.card_template = Image.open('./yugioh/assets/img/monster_effect.jpg').convert("RGBA")
        self.card_data = card
        self._proc_image(save=save)
        
    def _proc_image(self, save=True, savefile='./yugioh/assets/img/ygocard.jpg'):
        img = self._download_image()
        self._add_img_to_card(img)
        self._add_title(self.card_data['Title'])
        self._add_description(self.card_data['Effect'])
        if "Stars" in self.card_data and "Attack" in self.card_data and "Defense" in self.card_data:
            star_size = (35, 35)
            self.monster_star = Image.open('./yugioh/assets/img/monster_star.png').resize(star_size).convert("RGBA")
            self._add_monster_attribs(self.card_data['Stars'], self.card_data["Attack"], self.card_data["Defense"])
        if save:
            self._save_image()
        return
        
    def _download_image(self, savefile='./yugioh/assets/img/ygocard.jpg'):
        url = self.card_data['image_url']
        resp = requests.get(url)
        self.card_img = Image.open(BytesIO(resp.content))

    def _add_img_to_card(self, savefile='./yugioh/assets/img/ygocard.jpg'):
        img_box = (381, 384)
        card_img = self.card_img.resize(img_box).convert("RGBA")
        self.card_template.paste(card_img, (73, 166), card_img)
    
    def _add_title(self, title):
        draw = ImageDraw.Draw(self.card_template)
        for font_size in range(80, 0, -1):
            font = ImageFont.truetype('./yugioh/assets/fonts/ygo_title.ttf', font_size)
            if font.getsize(title)[0] <= 381:
                draw.text((48,41), title, (255,255,255), font=font)
                return
        
    
    def _add_description(self, description):
        wrapper = textwrap.TextWrapper(width=62)
        word_list = wrapper.wrap(text=description)
        caption_new = ''
        for ii in word_list[:-1]:
            caption_new = caption_new + ii + '\n'
        caption_new += word_list[-1]
        
        draw = ImageDraw.Draw(self.card_template)
        font = ImageFont.truetype('./yugioh/assets/fonts/ygo_description.ttf', 15)
        draw.text((47,593), caption_new, (0,0,0), font=font)
        return
    
    def _add_monster_attribs(self, stars=None, attack=0, defense=0):
        star_position = (420, 115)
        for _ in range(int(stars)):
            self.card_template.paste(self.monster_star, star_position, self.monster_star)
            star_x = star_position[0]-self.monster_star.size[0]-1
            star_position = (star_x, 115)
        
        draw = ImageDraw.Draw(self.card_template)
        font = ImageFont.truetype('./yugioh/assets/fonts/ygo_description.ttf', 21)
        draw.text((320,695), str(attack), (0,0,0), font=font)
        draw.text((430,695), str(defense), (0,0,0), font=font)
        return
    
    def _save_image(self, savefile='./yugioh/assets/img/ygocard.jpg'):
        self.card_template.convert("RGB").save(savefile)
        print(f'card image saved to {savefile}')
        

    