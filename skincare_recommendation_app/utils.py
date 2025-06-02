import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from django.templatetags.static import static
import graphviz

class utils:
    def upload_file(file):
        with open("skincare_recommendation_app/static/user/upload/" + file.name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return file.name

    def get_user_skin_condition(path):
        # Preprocessing User Input 
        SIZE = 200
        img = tf.keras.utils.load_img(path, target_size=(SIZE, SIZE, 3))
        
        img = tf.keras.utils.img_to_array(img)
        img = img / 255.
        
        # load model 
        model = tf.keras.models.load_model('skincare_recommendation_app' + static('assets/ai_model/test1_model.h5'))

        print(model.summary())

        # get the prediction
        img = np.expand_dims(img, axis=0)
        classes = ['Acne', 'Wrinkles', 'Blackhead']  
        proba = model.predict(img)  
        sorted_categories = np.argsort(proba[0])[:-7:-1]  

        # FOR DEVELOPMENT 
        print(classes[sorted_categories[0]])
        for i in range(len(sorted_categories)):
            print("{}".format(classes[sorted_categories[i]]) + " ({:.3})".format(proba[0][sorted_categories[i]]))
        
        # return [classes[sorted_categories[0]], proba[0][sorted_categories[i]]]
        return classes[sorted_categories[0]]

    def classDiagramVisualize():
        g = graphviz.Graph(format='png') 

