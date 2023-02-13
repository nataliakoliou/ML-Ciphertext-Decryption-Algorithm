# Machine-Learning Ciphertext Decryption Algorithm

This project aims to build a decryption tool that uses a multi-class SVM classification model to decrypt ciphertexts, encrypted with some randomly generated mixed-ciphertext alphabet.

* **Implement manual feature extraction:** Identifies and describes the most common features that define the internal structure of the text-datasets (training & testing). These features include: Single Letter Frequencies, Letter Occurencies in k-letter words, Letter Position Frequencies and Double Letters Frequencies.
* **Perform manual feature selection:** Creates feature-set (X) and label-set (y), by selecting the features that describe best each class.
* **Implement the classification model iteratively:** Trains an SVM classifier on the training plaintext. It then uses this classification model iteratively, to assign class-labels to the testing ciphertext (decryption alphabet prediction).
* **Decrypt the testing ciphertext:** Applies the predicted decryption alphabet to the testing ciphertext to decrypt it.

### Prerequisites
The following python packages are required for the code to run:

* Python 3: https://www.python.org/downloads/
* NumPy: ```pip install numpy```
* Scikit-learn: ```pip install -U scikit-learn```




## Author
Natalia Koliou: find me on [LinkedIn](https://www.linkedin.com/in/natalia-k-b37b01197/).
