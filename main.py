from flask import Flask,request, render_template
import cv2
from cv2 import IMREAD_GRAYSCALE, imread,imshow,CascadeClassifier
from cv2 import rectangle
import matplotlib.pyplot as plt
from werkzeug.exceptions import MethodNotAllowed
from PIL import Image

app = Flask(__name__)

def detect_faces(image_path):
    pixels = imread(image_path)

    classifier = CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    bboxes = classifier.detectMultiScale(pixels)
    # print bounding box for each detected face
   
    for box in bboxes:

        x, y, width, height = box
        x2, y2 = x + width, y + height

        rectangle(pixels, (x, y), (x2, y2), (0,0,255), 1)


    image = Image.fromarray(cv2.cvtColor(pixels, cv2.COLOR_BGR2RGB))
    image.save(image_path)
        
    return 1




@app.route("/",methods = ['GET','POST'])
def home():
    return render_template("index.html")

@app.route("/submit", methods = ["GET","POST"])
def detect_face():
    print("detect_faces")
    if request.method == 'POST':
        img = request.files['my_image']
        img_path = "./static/" + img.filename
        
        img.save(img_path)

        detect = detect_faces(img_path)
    return render_template("index.html",detection = detect, img_path = img_path)





if __name__=="__main__":
    app.run(debug=True)




