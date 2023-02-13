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
    for w in words:
        if word_length == 1 and len(w) == word_length and w in alphabet:
            feature_WL[w] = 1
        elif (has_domain(word_length, 2, 4) and len(w) == word_length) or \
             (has_domain(word_length, 5, 7) and has_domain(len(w), 5, 7)) or \
             (has_domain(word_length, 8, 10) and has_domain(len(w), 8, 10)) or \
             (word_length > 10 and len(w) >= word_length):
            for l in list(w):
                if l in alphabet:
                    feature_WL[l] += 1/letters_times.get(l)
    round_dict(feature_WL, accuracy)
    return feature_WL

def extract_feature_LP(alphabet, case, words, letters_times, accuracy):
    feature_LP = dict.fromkeys(alphabet, 0)
    for w in words:
        first = list(w)[0]
        last = list(w)[len(w)-1]
        if "first" in case and first in alphabet:
            feature_LP[first] += 1/letters_times.get(first)
        elif "last" in case and last in alphabet:
            feature_LP[last] += 1/letters_times.get(last)    
        elif first == last and first in alphabet:
            feature_LP[first] += 1/letters_times.get(first)
    round_dict(feature_LP, accuracy)
    return feature_LP

def extract_feature_DL(alphabet, words, letters_times, accuracy):
    feature_DL = dict.fromkeys(alphabet, 0)
    for w in words:
        prev_letter = "#"
        for l in list(w):
            if len(w) != 1 and prev_letter == l and l in alphabet:
                feature_DL[l] += 1 / letters_times.get(l)
            prev_letter = l
    round_dict(feature_DL, accuracy)
    return feature_DL

def has_domain(var, point1, point2):
    return True if point1 <= var <= point2 else False

def round_dict(dict, accuracy):
    return {key: round(val, accuracy) for key, val in dict.items()}

def get_letters(words):
    return [letter for word in [list(w) for w in words] for letter in word]

def divide_chunks(list, n):
    for i in range(0, len(list), n):
        yield list[i:i + n]

def is_shaffled_alphabet(key):
    return len(key) == len(set(key))

def update_y(fy, y):
    count = 0
    for i in range(len(fy)):
        if fy[i] == "NN":
            if y[count] not in fy:
                fy[i] = y[count]
            count += 1       
    return fy

def update_alphabet(alphabet, fy):
    return [val for val in alphabet if val not in fy]

def load_local_data():

    training_text = "TRAINING-tolstoy-anna-karenina.txt"
    testing_text = "TESTING-tolstoy-anna-karenina-1.txt"
    decryption_alphabet = "rgbhdtkclvnqjxfspamioyzweu"  # encryption_alphabet = "rcheyobdtmgiskuqlapfzjxnvw"

    return training_text, testing_text, decryption_alphabet

def decrypt(text, fy, alphabet):
    decr_dict = {alphabet[i]: fy[i] for i in range(len(alphabet))}
    with open(text, 'r') as f:
        encr_text = f.read()
        decr_text = "".join([decr_dict[encr_char] if encr_char in decr_dict else encr_char 
                            for encr_char in get_letters(encr_text)])
    with open("output.txt", 'w') as output:
        output.write(decr_text)
    print("Decrypted Ciphertext:\n" + decr_text)

def process(super_words, alphabet, chunks):
    
    accuracy = 10
    features, labels = [], []
    sub_words = list(divide_chunks(super_words, chunks))

    for words in sub_words:
        letters = get_letters(words)
        NL = len(letters)
        letters_times = dict(sorted({key: value for key, value in dict(col.Counter(letters)).items()}.items()))

        f0 = extract_feature_FR(alphabet, letters, NL, accuracy)
        f1, f2, f3, f4, f5, f6, f7 = [extract_feature_WL(alphabet, words, i, letters_times, accuracy) for i in (1, 2, 3, 4, rand.randint(5,7), rand.randint(8,10), 11)]
        f8, f9, f10 = (extract_feature_LP(alphabet, pos, words, letters_times, accuracy) for pos in ("first", "last", "both"))
        f11 = extract_feature_DL(alphabet, words, letters_times, accuracy)

        temp_features = dd(list)  # defines an empty dictionary
        for d in (f0, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11):
            for key, value in d.items():
                temp_features[key].append(value)
        temp_features = dict(temp_features)  # gets only the dictionary-part
        temp_features = list(temp_features.values())  # converts dictionary of lists into a list of lists

        features.extend(temp_features)
        labels.extend(alphabet)

    X, y = np.array(features), np.array(labels)
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

        X_test = process(TE_words, alphabet, len(list(TE_words)))[0]
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
    print("\nAccuracy Classification Score: {:.2f}\n{}".format(accuracy, "-"*127))

    complete_alphabet = list(string.ascii_lowercase)
    decrypt(testing_text, final_y, complete_alphabet)

if __name__ == "__main__":
    main()
