# Machine-Learning Ciphertext Decryption Algorithm

This project aims to build a decryption tool that uses a multi-class SVM classification model to decrypt ciphertexts, encrypted with some randomly generated mixed-ciphertext alphabet.

* **Implements manual feature extraction:** Identifies and describes the most common features that define the internal structure of the text-datasets. These features include: Single Letter Frequencies, Letter Occurencies in k-letter words, Letter Position Frequencies and Double Letters Frequencies.
* **Perform manual feature selection:** Creates feature-set (X) and label-set (y), by selecting the features that describe best each class.
* **Implement the classification model iteratively:** Trains the classification model on a plaintext and assigns class-labels to the encrypted testing ciphertext.
* **Decrypts the testing ciphertext:** Applies the predicted decryption alphabet to the testing ciphertext to decrypt it.

### Prerequisites
