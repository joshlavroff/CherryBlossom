from PIL import Image
import requests
import rembg
import os

def getImage(url):
    response=requests.get(url)
    if response.status_code==200:
        with open(url.split('/')[-1],'wb') as file:
            file.write(response.content)
            return file

def makeTrainingImage(imagePath,savePath='',overwrite=True):
    if savePath=='' and not overwrite:
        raise Exception('savePath must not be blank when overwrite is disabled')
    image=Image.open(imagePath)
    removed=rembg.remove(image).resize((255, 255))
    if not overwrite:
        expPath=savePath+'\\'+os.path.splitext(os.path.basename(imagePath))[0]+'.png'  
    else:
        expPath=os.path.splitext(imagePath)[0]+'.png'
    removed.save(expPath)
    return expPath
