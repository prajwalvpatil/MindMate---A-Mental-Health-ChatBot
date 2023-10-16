import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import os
import tensorflow as tf 

# Load existing intents from your intents.json file
with open('data/intents.json', 'r') as json_file:
    intents = json.load(json_file)

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Define words and classes based on loaded intents
words = []
classes = []
documents = []

for intent in intents['intents']:
    for pattern in intent['patterns']:
        # Tokenize words in the pattern
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        # Add to documents in the format (pattern, intent tag)
        documents.append((w, intent['tag']))
        # Add intent tag to classes
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Lemmatize words and remove duplicates
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ['?', '!', '.', ',']]
words = sorted(list(set(words)))

# Sort classes
classes = sorted(list(set(classes)))

# Create a bag of words representation for training data
def create_training_data():
    training_data = []
    for doc in documents:
        pattern_words = doc[0]
        intent = doc[1]
        bag = bag_of_words(pattern_words, words)
        output_row = [0] * len(classes)
        output_row[classes.index(intent)] = 1
        training_data.append([bag, output_row])
    return training_data

def bag_of_words(sentence, words):
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence]
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return bag  # Return bag as a list, not a NumPy array

training_data = create_training_data()

# Shuffle the training data
random.shuffle(training_data)

# Separate bag and output_row before converting to NumPy arrays
X = [item[0] for item in training_data]
Y = [item[1] for item in training_data]

# Convert to NumPy arrays
X = np.array(X)
Y = np.array(Y)

model = Sequential()
model.add(Dense(128, input_shape=(len(X[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(Y[0]), activation='softmax'))

# Use the legacy SGD optimizer with the decay parameter
sgd = tf.keras.optimizers.legacy.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Train the model
model.fit(np.array(X), np.array(Y), epochs=100, batch_size=5, verbose=1)

# Save the trained model
model.save('chatbot_model.h5')

# Save intents, words, and classes as JSON and pickle files
with open('intents.json', 'w') as json_file:
    json.dump(intents, json_file)

with open('words.pkl', 'wb') as words_file:
    pickle.dump(words, words_file)

with open('classes.pkl', 'wb') as classes_file:
    pickle.dump(classes, classes_file)

print("Chatbot model trained and files saved.")