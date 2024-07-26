from PIL import Image
import matplotlib.pyplot as plt
import numpy
import requests
from fashion_clip.fashion_clip import FashionCLIP
from transformers import CLIPProcessor, CLIPModel
import rembg

def getImage(url):
    response=requests.get(url)
    if response.status_code==200:
        with open('image.jpg','wb') as file:
            file.write(response.content)
            return file

def removeBG(imagePath):
    image=Image.open(imagePath)
    removed=rembg.remove(image)
    removed.save('imageNoBG.png')

#getImage('https://auctions.c.yimg.jp/images.auctions.yahoo.co.jp/image/dr000/auc0507/users/0e1fbd426bd1c5639d3d8ab4f3e6da8ad821e53f/i-img1200x1200-1721323147vthdnu6974.jpg')
#removeBG('image.jpg')

clip=CLIPModel.from_pretrained('patrickjohncyh/fashion-clip')
processor=CLIPProcessor.from_pretrained('patrickjohncyh/fashion-clip')

image=Image.open('imageNoBG.png')

inputs = processor(text=["a photo of a black bag with gold hardware", "a photo of a black jacket", 
                         "a photo of a pink tee shirt"],
                   images=image, return_tensors="pt", padding=True)

outputs = clip(**inputs)
logits_per_image = outputs.logits_per_image  # this is the image-text similarity score
probs = logits_per_image.softmax(dim=1)  
print(probs)
image.resize((224, 224))