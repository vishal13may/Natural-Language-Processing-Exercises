import os
import glob
import sys
from collections import defaultdict
from random import shuffle

total_documents = 0
total_ham_documents = 0
total_spam_documents = 0

vocabulary = defaultdict(int)
document_dictionary = {}
list_all_files = []

ham_directories = []
spam_directories = []

document_label_dictionary = {}

bias = 0

CONSTANT_SPAM_LABEL = 1
CONSTANT_HAM_LABEL = -1

CONSTANT_HAM = "HAM"
CONSTANT_SPAM = "SPAM"
CONSTANT_FILE_WRITE_SEPARATOR = " ";
CONSTANT_FILE_EXTENSION = ".txt"
CONSTANT_NB_MODEL = "per_model.txt"

NUMBER_OF_ITERATION = 20


def find_spam_ham_directories():
    # Function to find Spam and Ham directories in training data.
    for directory_name, directory_names, file_names in os.walk(training_data_path):
        if os.path.basename(directory_name).strip().upper() == CONSTANT_HAM:
            ham_directories.append(directory_name)
            global total_ham_documents
            total_ham_documents += len(glob.glob(os.path.join(directory_name, '*'+CONSTANT_FILE_EXTENSION)))
        elif os.path.basename(directory_name).strip().upper() == CONSTANT_SPAM:
            spam_directories.append(directory_name)
            global total_spam_documents
            total_spam_documents += len(glob.glob(os.path.join(directory_name, '*'+CONSTANT_FILE_EXTENSION)))
    return

def read_all_files(class_directories,label):
    # Function to generate Vocabulary
    for directory in class_directories:
        for filename in glob.glob(os.path.join(directory, '*'+CONSTANT_FILE_EXTENSION)):
            try:
                list_all_files.append(filename)
                document_label_dictionary[filename] = label
                features = defaultdict(int)
                lines = [line for line in open(filename,"r", encoding="latin1")]
                for line in lines:
                    tokens = line.split()
                    for token in tokens:
                        vocabulary[token] = 0
                        features[token] += 1
                document_dictionary[filename] = features
            except IOError:
                continue
            except:
                continue
    return

def generate_model():
    # Function to generate Model
    global bias
    for itr in range(NUMBER_OF_ITERATION):
        shuffle(list_all_files)
        for filename in list_all_files:
            y = document_label_dictionary[filename]
            features = document_dictionary[filename]
            frequency = 0
            for key in features:
                frequency += vocabulary[key]*features[key]

            alpha = frequency + bias
            if alpha*y <= 0:
                bias += y
                for key in features:
                    vocabulary[key] += (y*features[key])

    return

def write_training_model():
    #Write training model.
    try:
        with open(CONSTANT_NB_MODEL, 'w', encoding="latin1") as file_handler:
            file_handler.write(str(bias)+'\n')
            for token in vocabulary:
                file_handler.write(token+CONSTANT_FILE_WRITE_SEPARATOR+str(vocabulary[token])+'\n')
        file_handler.close()
    except IOError:
        pass
    return


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Please enter the training data directory.")
        sys.exit(0)

    training_data_path = sys.argv[1]
    training_data_path = os.path.abspath(training_data_path)

    find_spam_ham_directories()

    if len(spam_directories) == 0:
        print("Given path does not contain spam directories.")
        sys.exit(0)

    if len(ham_directories) == 0:
        print("Given path does not contain ham directories.")
        sys.exit(0)

    read_all_files(spam_directories, CONSTANT_SPAM_LABEL)
    read_all_files(ham_directories, CONSTANT_HAM_LABEL)

    generate_model()
    write_training_model()



