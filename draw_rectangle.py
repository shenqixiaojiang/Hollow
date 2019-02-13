#coding:utf-8
from PIL import Image,ImageDraw,ImageFont

font = ImageFont.truetype('./simkai.ttf', 20) ##load the chinese font
def draw_rectangle(img_full_path, save_path):
    img = Image.open(img_full_path)
    img = img.resize((299,299))
    drawObject = ImageDraw.Draw(img)
    for ii in range(3):
        left,top,right,bottom = 100 + ii,100 + ii,200 + ii,200 + ii
        drawObject.rectangle([left,top,right,bottom],outline = "red")
        drawObject.text([left, top], '少年加油'.decode('utf-8'), font=font, fill=(0, 255, 0))
    img.save(save_path)
