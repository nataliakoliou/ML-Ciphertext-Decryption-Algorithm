import re
import string
import numpy as np
import random as rand
import collections as col
from sklearn.svm import SVC
from collections import defaultdict as dd
from sklearn.metrics import accuracy_score

def extract_feature_FR(alphabet, letters, NL, accuracy):
    feature_FR = dict.fromkeys(alphabet, 0)
    for l in letters:
        if l in alphabet:
            feature_FR[l] += 1/NL
    round_dict(feature_FR, accuracy)
    return feature_FR

def extract_feature_WL(alphabet, words, word_length, letters_times, accuracy):
    feature_WL = dict.fromkeys(alphabet, 0)
    if word_length == 1:
        for w in words:
            if w not in alphabet:
                continue
            elif len(w) == word_length and feature_WL[w] == 0:
                feature_WL[w] = 1
    elif has_domain(word_length, 2, 4):
        for w in words:
            if len(w) == word_length:
                for l in list(w):
                    if l not in alphabet:
                        continue
                    else:
                        feature_WL[l] += 1/letters_times.get(l)
    elif has_domain(word_length, 5, 7):
        for w in words:
            if has_domain(len(w), 5, 7):
                for l in list(w):
                    if l not in alphabet:
                        continue
                    else:
                        feature_WL[l] += 1/letters_times.get(l)
    elif has_domain(word_length, 8, 10):
        for w in words:
            if has_domain(len(w), 8, 10):
                for l in list(w):
                    if l not in alphabet:
                        continue
                    else:                    
                        feature_WL[l] += 1/letters_times.get(l)
    else:
        for w in words:
            if len(w) >= word_length:
                for l in list(w):
                    if l not in alphabet:
                        continue
                    else:                    
                        feature_WL[l] += 1/letters_times.get(l)
                    
    round_dict(feature_WL, accuracy)
    return feature_WL

def extract_feature_SW(alphabet, case, words, letters_times, accuracy):
    feature_SW = dict.fromkeys(alphabet, 0)
    if "first" in case:
        for w in words:
            first = list(w)[0]
            if first not in alphabet:
                continue
            else:
                feature_SW[first] += 1/letters_times.get(first)
    elif "last" in case:
        for w in words:
            last = list(w)[len(w)-1]
            if last not in alphabet:
                continue
            else:            
                feature_SW[last] += 1/letters_times.get(last)    
    else:
        for w in words:
            first = list(w)[0]
            last = list(w)[len(w)-1]
            if first == last and first in alphabet:
                feature_SW[first] += 1/letters_times.get(first)
    round_dict(feature_SW, accuracy)
    return feature_SW

def extract_feature_DL(alphabet, words, letters_times, accuracy):
    feature_DL = dict.fromkeys(alphabet, 0)
    for w in words:
        if len(w) != 1:
            prev_letter = "#"
            for l in list(w):
                if prev_letter == l and l in alphabet:
                    feature_DL[l] += 1/letters_times.get(l)
                prev_letter = l
    round_dict(feature_DL, accuracy)
    return feature_DL

def has_domain(var, point1, point2):
    if var >= point1 and var <= point2:
        return True
    else:
        return False

def round_dict(dict, accuracy):
    for key in dict: dict[key] = round(dict.get(key),accuracy)
    return dict

def get_letters(words):
    temp = []
    for w in words:
        temp.append(list(w))
    letters = [letter for word in temp for letter in word]
    return letters

def divide_chunks(list, n):
    for i in range(0, len(list), n):
        yield list[i:i + n]

def is_shaffled_alphabet(key):
    if len(key) == len(set(key)):
        return True
    else:
        return False

def update_y(fy, y):
    count = 0
    for i in range(len(fy)):
        if fy[i] == "NN":
            if y[count] not in fy:
                fy[i] = y[count]
            count += 1
        else:
            continue        
    return fy

def update_alphabet(alphabet, fy):
    new_AB = []
    for val in alphabet:
        if val not in fy:
            new_AB.append(val)
    return new_AB

def load_local_data():

    training_text = "TRAINING-tolstoy-anna-karenina.txt"

    testing_text_1 = "TESTING-tolstoy-anna-karenina-1.txt"
    decryption_alphabet_1 = "rgbhdtkclvnqjxfspamioyzweu"  # encryption_alphabet_1 = "rcheyobdtmgiskuqlapfzjxnvw"

    return training_text, testing_text_1, decryption_alphabet_1

def decrypt(text, fy, alphabet):

    decr_dict = {}
    for i in range(len(alphabet)):
        decr_dict[alphabet[i]] = fy[i]

    with open(text, 'r') as f:
        encr_text = f.read()
        re.split(r'(\s+)', encr_text)
        decr_text = ""
        for count, encr_char in enumerate(get_letters(encr_text)):
            if encr_char.isspace():
                decr_text = decr_text + encr_char
            elif encr_char not in decr_dict:
                decr_text = decr_text + encr_char
            else:
                decr_text = decr_text + decr_dict[encr_char]

    with open("output.txt", 'w') as output:
        output.write(decr_text)
    with open("output.txt", 'r') as file:
        contents = file.read()
        print("Decrypted Ciphertext: \n")
        print(contents)

def process(super_words, alphabet, chunks):
    
    accuracy = 10
    features = []
    labels = []

    sub_words = list(divide_chunks(super_words, chunks))

    for words in sub_words:
        letters = get_letters(words)
        NL = len(letters)
        letters_times = dict(sorted({key: value for key, value in dict(col.Counter(letters)).items()}.items()))

        feature_0 = extract_feature_FR(alphabet, letters, NL, accuracy)
        feature_1 = extract_feature_WL(alphabet, words, 1, letters_times, accuracy)
        feature_2 = extract_feature_WL(alphabet, words, 2, letters_times, accuracy)
        feature_3 = extract_feature_WL(alphabet, words, 3, letters_times, accuracy)
        feature_4 = extract_feature_WL(alphabet, words, 4, letters_times, accuracy)
        feature_5 = extract_feature_WL(alphabet, words, rand.randint(5,7), letters_times, accuracy)
        feature_6 = extract_feature_WL(alphabet, words, rand.randint(8,10), letters_times, accuracy)
        feature_7 = extract_feature_WL(alphabet, words, 11, letters_times, accuracy)
        feature_8 = extract_feature_SW(alphabet, "first", words, letters_times, accuracy)
        feature_9 = extract_feature_SW(alphabet, "last", words, letters_times, accuracy)
        feature_10 = extract_feature_SW(alphabet, "both", words, letters_times, accuracy)
        feature_11 = extract_feature_DL(alphabet, words, letters_times, accuracy)
        
        temp_features = dd(list) # defining an empty dictionary

        # feature_0, feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_7, feature_8, feature_9, feature_10, feature_11
    
        for d in (feature_0, feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_7, feature_8, feature_9, feature_10, feature_11):
            for key, value in d.items():
                temp_features[key].append(value)
        temp_features = dict(temp_features)      # get only the dictionary-part
        temp_features = [val for key, val in temp_features.items()]     # convert dictionary of lists into a list of lists

        features.extend(temp_features)
        labels.extend(alphabet)

    X = np.array(features)
    y = np.array(labels)

    return X, y
        
def main():
    
    training_text, testing_text, decryption_alphabet = load_local_data()

    done = False
    alphabet = list(string.ascii_lowercase)
    final_y = ["NN" for a in range(len(alphabet))]
    np.set_printoptions(suppress=True)  # to avoid scientific notation when printing
    
    with open(training_text, 'r') as TR_f:
        TR_words = TR_f.read().split()
    with open(testing_text, 'r') as TE_f:
        TE_words = TE_f.read().split()

    while not done:
        X_train, y_train = process(TR_words, alphabet, 400)
        svc = SVC()
        svc.fit(X_train, y_train)

        X_test, unused = process(TE_words, alphabet, len(list(TE_words)))
        y_pred = svc.predict(X_test)
        final_y = update_y(final_y, y_pred)
        y_test = list(decryption_alphabet)

        if is_shaffled_alphabet(y_pred):
            done = True
        else:
            alphabet = update_alphabet(alphabet, final_y)
            if len(alphabet) == 1:
                final_y = update_y(final_y, alphabet)  # no prediction needed!
                done = True
  
    accuracy = accuracy_score(y_test, final_y)
    print("Accuracy Classification Score: {:.2f}".format(accuracy))
    print("-"*127)

    complete_alphabet = list(string.ascii_lowercase)
    decrypt(testing_text, final_y, complete_alphabet)

if __name__ == "__main__":
    main()