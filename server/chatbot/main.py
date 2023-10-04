import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer

# TODO: Add download stuff from nltk (punkt & wordnet)
# TODO: Encapsulate (defs breakdown)

import json
import string
import random

# CHECK: Shift inside function (no global use)
lemmatizer = WordNetLemmatizer()

def chatbot(user_input):
    with open('./data/intents.json', 'r') as file:
        data = json.load(file)

    # Vocal with core tags (output layer)
    words = []
    classes = []

    # All patterns with respective tags
    data_patterns = []
    data_tags = []

    # Raw preprocessing data
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

    # Training data  (In 0 & 1)
    # [[Match with vocab and pattern], [respective pattern tag]] 
    training = []
    output_template = [0] * len(classes)

    for index, pattern in enumerate(data_patterns):
        bag_of_words = []

        # Preprocessing single pattern
        tokenized_pattern = nltk.word_tokenize(pattern)
        lemmatized_words = [lemmatizer.lemmatize(word.lower()) for word in tokenized_pattern if word not in string.punctuation] 

        for word in words:
            bag_of_words.append(1) if word in lemmatized_words else bag_of_words.append(0)

        # Mathching tag from 'data_tags'
        # data_tags (obtain tag) -> classes (obtain index) -> output_row
        output_row = list(output_template)
        output_row[classes.index(data_tags[index])] = 1
    
        training.append([bag_of_words, output_row])

    random.shuffle(training)
    training = np.array(training, dtype=object)

    # Features and Target splitting
    training_features = np.array(list(training[:, 0]))
    training_targets = np.array(list(training[:, 1]))

    return f'''Chatbot is under development.
Sorry for inconvenience! :(
Received input: \'{user_input}\''''

def get_response(user_input):
    res = chatbot(user_input)
    return { 'msg': res }
