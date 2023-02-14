# Machine-Learning Ciphertext Decryption Algorithm

This project aims to build a decryption tool that uses a multi-class SVM classification model to decrypt ciphertexts, encrypted with some randomly generated mixed-ciphertext alphabet.

* **Implement manual feature extraction:** Identifies and describes the most common features that define the internal structure of the text-datasets (training & testing). These features include: Single Letter Frequencies, Letter Occurencies in k-letter words, Letter Position Frequencies and Double Letters Frequencies.
* **Perform manual feature selection:** Creates feature-set (X) and label-set (y), by selecting the features that describe best each class.
* **Implement the classification model iteratively:** Trains an SVM classifier on the training plaintext. It then uses this classification model iteratively, to assign class-labels to the testing ciphertext (decryption alphabet prediction).
* **Decrypt the testing ciphertext:** Applies the predicted decryption alphabet to the testing ciphertext to decrypt it.

## Prerequisites
The following python packages are required for the code to run:
* Python 3: https://www.python.org/downloads/
* NumPy: ```pip install numpy```
* Scikit-learn: ```pip install -U scikit-learn```

**Alternatively:** you can download [requirements.txt](https://github.com/nataliakoliou/ML-Ciphertext-Decryption/blob/main/requirements.txt) and run ```pip install -r requirements.txt```, to automatically install all the packages needed to reproduce my project on your own machine.

> The code uses the [TRAINING-tolstoy-anna-karenina.txt](https://github.com/nataliakoliou/ML-Ciphertext-Decryption/blob/main/datasets/TRAINING-tolstoy-anna-karenina.txt) and [TESTING-tolstoy-anna-karenina.txt](https://github.com/nataliakoliou/ML-Ciphertext-Decryption/blob/main/datasets/TESTING-tolstoy-anna-karenina.txt) files as the training and testing text. These files should be in the same directory as the code.

## Acknowledgments
I would like to express my gratitude to [Interactive Maths](https://crypto.interactive-maths.com/mixed-alphabet-cipher.html) for providing valuable information and resources, that contributed to the development of my project.

## Conclusion
This code provides a basic implementation of an ML Ciphertext Decryption Algorithm. Users are encouraged to modify the training/testing datasets or the feature-tuple, to observe the impact on the total performance and accuracy.

Here are some suggestions:
```python
# Remove some good features from the feature tuple:
120  for d in (f3, f4, f5, f6, f7, f8, f9, f10):
```

```python
# Use a different testing dataset:
87   training_text = "TRAINING-tolstoy-anna-karenina.txt"
88   testing_text = "TESTING-tolstoy-anna-karenina.txt"
89   decryption_alphabet = "rgbhdtkclvnqjxfspamioyzweu"  # encryption_alphabet = "rcheyobdtmgiskuqlapfzjxnvw"
```
<sub> In [this](https://github.com/nataliakoliou/ML-Ciphertext-Decryption/tree/main/datasets) folder, you will find a variety of texts to use for the testing process. You can also create another training dataset from scratch, however it requires a lot of effort and is not recommended.

## Author
Natalia Koliou: find me on [LinkedIn](https://www.linkedin.com/in/natalia-k-b37b01197/).
