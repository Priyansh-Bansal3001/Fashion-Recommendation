import streamlit as st
import os
from PIL import Image
import tensorflow
import numpy as np
from numpy.linalg import norm
from tensorflow.keras.applications.resnet50 import ResNet50,preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import GlobalMaxPooling2D
from tensorflow.keras.preprocessing.image import load_img
import pickle
from tensorboard.notebook import display
from sklearn.neighbors import NearestNeighbors

st.title('Fashion Recommender System')

feature_list = np.array(pickle.load(open('embeddings.pkl','rb')))
filenames = pickle.load(open('filenames.pkl','rb'))

model = ResNet50(weights='imagenet',include_top = False, input_shape = (224,224,3))
model.trainable = False

model = tensorflow.keras.Sequential([
    model,
    GlobalMaxPooling2D()
])

def extract_features(img_path,model):
    img = image.load_img(img_path,target_size=(224,224))
    img_array = image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array,axis=0)
    preprocess_img = preprocess_input(expanded_img_array)
    result = model.predict(preprocess_img).flatten()
    normalized_result = result/ norm(result)
    return normalized_result

def recommend(feature,feature_list):
    neighbors = NearestNeighbors(n_neighbors=5, algorithm='brute', metric='euclidean')
    neighbors.fit(feature_list)

    distances, indices = neighbors.kneighbors([features])
    return indices


def save_uploaded_file(uploaded_file):
    try:
        with open(os.path.join('uploads',uploaded_file.name),'wb') as f:
            f.write(uploaded_file.getbuffer())
        return 1
    except:
        return 0

uploaded_file = st.file_uploader("Choose an Image")
if uploaded_file is not None:
    if save_uploaded_file(uploaded_file):
        display_image = Image.open(uploaded_file)
        st.image(display_image)
        features = extract_features(os.path.join('uploads',uploaded_file.name),model)
        indices = recommend(features,feature_list)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.image(filenames[indices[0][0]])
        with col2:
            st.image(filenames[indices[0][1]])
        with col3:
            st.image(filenames[indices[0][2]])
        with col4:
            st.image(filenames[indices[0][3]])
        with col5:
            st.image(filenames[indices[0][4]])
    else:
        print('Some error occurred in file upload')