from flask import Flask, request, jsonify
import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Load your chatbot-related data and model here
lemmatizer = WordNetLemmatizer()

# Check if training data and model files exist
if os.path.exists('intents.json'):
    # Load training data
    with open('intents.json', 'r') as f:
        intents = json.load(f)

    with open('words.pkl', 'rb') as f:
        words = pickle.load(f)

    with open('classes.pkl', 'rb') as f:
        classes = pickle.load(f)

    # Load pre-trained model
    model = load_model('chatbot_model.h5')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data['message']
    
    # Use your existing chatbot code to process the message and get a response
    ints = predict_class(message)
    
    if ints:
        # Check if ints is not empty
        res = get_response(ints, intents)
    else:
        # Handle the case where no intents were recognized
        res = "I'm sorry, I didn't understand your message."
    
    return jsonify({'response': res})

if __name__ == '__main__':
    app.run(debug=True)
