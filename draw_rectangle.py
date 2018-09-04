from PIL import Image,ImageDraw
def draw_rectangle(img_full_path, save_path):
  img = Image.open(img_full_path)
  img = img.resize((299,299))
  drawObject = ImageDraw.Draw(img)
  left,top,right,bottom = 100,100,200,200
  drawObject.rectangle([left,top,right,bottom],outline = "red")
  img.save(save_path)
