import nltk
from nltk.stem import WordNetLemmatizer

# TODO: Add download stuff from nltk (punkt & wordnet)
# TODO: Encapsulate (defs breakdown)

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout

import json
import string
import random
import numpy as np

# CHECK: Shift inside function (no global use)
lemmatizer = WordNetLemmatizer()


def clean_text(text):
    tokenized_text = nltk.word_tokenize(text)
    lemmatized_text = [lemmatizer.lemmatize(word.lower()) for word in tokenized_text if word not in string.punctuation]

    return lemmatized_text


def bag_of_words(text, vocab):
    bow = []
    clean_user_input = clean_text(text)

    for word in vocab:
        bow.append(1) if word in clean_user_input else bow.append(0)

    return np.array(bow)


def train_model(train_X, train_Y):
    model = Sequential()

    learning_rate_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
        initial_learning_rate=0.01,
        decay_steps=10000,
        decay_rate=0.9
    )

    # CHECK: Model methods
    # CHECK: Using legacy keras for more optimized result (optimizers.legacy.Adam)
    # CHECK: Change of 'learning_rate' and add of 'decay_rate' (in legacy)
    adam = tf.keras.optimizers.Adam(learning_rate=learning_rate_schedule)

    model.add(Dense(128, input_shape=(len(train_X[0]),), activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(len(train_Y[0]), activation="softmax"))

    model.compile(
        loss='categorical_crossentropy',
        optimizer=adam,
        metrics=["accuracy"]
    )

    # CHECK: Epochs value
    model.fit(x=train_X, y=train_Y, epochs=150, verbose=1)

    return model


def compute(user_input):
    with open('./data/intents.json', 'r') as file:
        data = json.load(file)

    # Vocal with core tags (output layer)
    words = []
    classes = []

    # All patterns with respective tags
    data_patterns = []
    data_tags = []

    # Building raw data 
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            tokenized_pattern = nltk.word_tokenize(pattern)
            words.extend(tokenized_pattern)

            data_patterns.append(pattern)
            data_tags.append(intent["tag"])

        if intent["tag"] not in classes:
            classes.append(intent["tag"])

    # CHECK: Test on 'pos' value for lemmatization
    words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in string.punctuation]

    words = sorted(set(words))
    classes = sorted(set(classes))

    # Training data (In 0 & 1)
    # [[Match with vocab and pattern], [respective pattern tag]] 
    training = []
    output_row_template = [0] * len(classes)

    for index, pattern in enumerate(data_patterns):
        training_bow = bag_of_words(pattern, words)

        # Mathching tag from 'data_tags'
        # data_tags (obtain tag) -> classes (obtain index) -> output_row
        output_row = list(output_row_template)
        output_row[classes.index(data_tags[index])] = 1
    
        training.append([training_bow, output_row])

    random.shuffle(training)
    training = np.array(training, dtype=object)

    # Features (X) and Target (Y) splitting
    training_X = np.array(list(training[:, 0]))
    training_Y = np.array(list(training[:, 1]))

    # Model training
    model = train_model(training_X, training_Y)

    # Preprocessing user input
    user_input_bow = bag_of_words(user_input, words)

    # CHECK: Redundent use of array as input
    result = model.predict(np.array([user_input_bow]))[0]
    tag = classes[np.argmax(result)]

    for intent in data["intents"]:
        if intent["tag"] == tag:
            res = f"{random.choice(intent['responses'])} - {intent['tag']}"
            print(res)

    return f'''Chatbot is under development.
Sorry for inconvenience! :(
Received input: \'{user_input}\''''

def get_response(user_input):
    if user_input == '':
        res = "Sorry, I don't understand"
    else:
        res = compute(user_input)

    return { 'msg': res }
