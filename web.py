from werkzeug.utils import secure_filename
from flask import Flask, request, render_template
import cv2
import numpy as np
import tensorflow as tf
from gtts import gTTS
from playsound import  playsound
from googletrans import Translator


# Define a flask app
app = Flask(__name__)

def process_eval(imk):
    output1 = cv2.resize(imk, (32,32))
    output1 = output1.astype('float')
    output1 /= 255.0
    print(type(output1))
    output1 = np.array(output1).reshape(-1, 32, 32, 3)
    classifer = tf.keras.models.load_model('/Users/sowmyakota/Desktop/Python Project/trafficsignSprint1/model.h5')
    pred_arr = classifer.predict(output1[[0], :]) 
    x=np.argmax(pred_arr,axis=1)
    #x = classifer.predict_classes(output1[[0], :])
    res_dictionary = {"0" : "Speed limit (20km/h)","1": "Speed limit (30km/h)","2": "Speed limit (50km/h)",
    "3": "Speed limit (60km/h)","4": "Speed limit (70km/h)","5": "Speed limit (80km/h)","6" : "End of speed limit (80km/h)","7" :"Speed limit (100km/h)",
    "8": "Speed limit (120km/h)","9": "No passing","10" : "No passing veh over 3.5 tons","10" : "No passing veh over 3.5 tons","11" : "Right-of-way at intersection",
    "11": "Right-of-way at intersection","12":"Priority road","13":"Yield",
    "14":"Stop","15":"No vehicles","16":"Veh > 3.5 tons prohibited","17":"No entry",
    "18":"General caution","19": "Dangerous curve left","20": "Dangerous curve right","21":"Double curve","22":"Bumpy road","23":"Slippery road",
    "24":"Road narrows on the right","25":"Road work","26":"Traffic signals",
    "27":"Pedestrians","28":"Children crossing","29": "Bicycles crossing","30":"Beware of ice/snow","31":"Wild animals crossing","32": "End speed + passing limits",
    "33":"Turn right ahead","34":"Turn left ahead","35":"Ahead only","36":"Go straight or right","37":"Go straight or left","38":"Keep right",
    "39":"Keep left","40":"Roundabout mandatory","41":"End of no passing",
    "42": "End no passing veh > 3.5 tons"
    }
    result = ""
    for i in res_dictionary.keys():
        if int(i) == x:
            result = res_dictionary[i]
            return result    

@app.route('/', methods=['GET'])
def index():
   return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def handle_form():
    translation = ""
    selected =""
    if request.method == 'POST':
        if request.form.get("classify"):
            file = request.files['file']
            file.save(secure_filename("bird.jpg"))
            im=cv2.imread("bird.jpg")
            result=process_eval(im)
            return render_template('index.html',result=result)
        elif request.form.get("play"):
            im=cv2.imread("bird.jpg")
            result=process_eval(im)
            language='en'
            myobj=gTTS(text=result,lang=language,slow=True)
            print("Hello from play")
            myobj.save("welcome1.mp3")
            playsound("welcome1.mp3")
            result = ""
        elif request.form.get("translate"):
            from translate import Translator
            selected=request.form.get('language')
            translator= Translator(to_lang=selected)
            file = request.files['file']
            file.save(secure_filename("bird.jpg"))
            im=cv2.imread("bird.jpg")
            result=process_eval(im)
            translation = translator.translate(result)
            print(selected)
            print(translation)
            # result = ""
            return render_template('index.html',result=result,translation=translation)
        # result = ""
        return render_template('index.html',result=result)

if __name__ == "__main__":
    app.debug = True
    app.run()