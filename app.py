# IMPORTS
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename
import numpy as np
import cv2
import os

# INITIALIZATION
app = Flask(__name__)

# LOADING MODEL
model = load_model('plantDiseaseDetection.h5')

# TUNING PARAMATERS
imageSize = (256, 256)
labelList = ['Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy', 'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 'Tomato_Bacterial_spot', 'Tomato_Early_blight', 'Tomato_Late_blight',
             'Tomato_Leaf_Mold', 'Tomato_Septoria_leaf_spot', 'Tomato_Spider_mites_Two_spotted_spider_mite', 'Tomato__Target_Spot', 'Tomato__Tomato_YellowLeaf__Curl_Virus', 'Tomato__Tomato_mosaic_virus', 'Tomato_healthy']
urlList = [
    'https://extension.wvu.edu/lawn-gardening-pests/plant-disease/fruit-vegetable-diseases/bacterial-leaf-spot-of-pepper',
    'https://gardenerspath.com/plants/vegetables/growing-using-bell-peppers/',
    'https://www.gardeningknowhow.com/edible/vegetables/potato/potato-early-blight-treatment.htm',
    'https://www.intechopen.com/chapters/58251',
    'https://wikifarmer.com/potato-plant-information/',
    'https://hort.extension.wisc.edu/articles/bacterial-spot-of-tomato/',
    'https://gardenerspath.com/how-to/disease-and-pests/early-blight-tomato/',
    'https://plantix.net/en/library/plant-diseases/100046/tomato-late-blight',
    'https://plantix.net/en/library/plant-diseases/100257/leaf-mold-of-tomato',
    'https://www.missouribotanicalgarden.org/gardens-gardening/your-garden/help-for-the-home-gardener/advice-tips-resources/pests-and-problems/diseases/fungal-spots/septoria-leaf-spot-of-tomato.aspx',
    'https://pnwhandbooks.org/insect/vegetable/vegetable-pests/hosts-pests/tomato-spider-mite',
    'https://apps.lucidcentral.org/pppw_v10/text/web_full/entities/tomato_target_spot_163.htm',
    'https://www.farmprogress.com/controlling-tomato-yellow-leaf-curl-virus',
    'https://www.gardeningknowhow.com/edible/vegetables/tomato/managing-tomato-mosaic-virus.htm',
    'https://wikifarmer.com/tomato-plant-information/'
]

# PLANT DISEASE DETECTION USING IMAGE


def usingImage(img_path):
    image = cv2.imread(img_path)
    image = cv2.resize(image, imageSize)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    inputImage = image*(1./255)
    inputImage = np.expand_dims(inputImage, axis=0)
    predictions = model.predict(inputImage)
    predictedIndex = np.argmax(predictions[0])
    label = labelList[predictedIndex]
    accuracy = str(round(predictions[0][predictedIndex]*100, 3))
    url = urlList[predictedIndex]
    title = f'{label},{accuracy},{url}'
    return title


# ENDPOINTS
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'upload', secure_filename(f.filename))
        f.save(file_path)
        predictions = usingImage(file_path)
        return predictions
    return None


# MAIN
if __name__ == "__main__":
    app.run(debug=True)
