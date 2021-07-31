import os
import re
import torch
import unicodedata
from .configs import MAX_LENGTH, data_path

#Word tokens
PAD_token = 0  # Padding short sentences
SOS_token = 1  # Start-of-sentence
EOS_token = 2  # End-of-sentence

class Corpus:
    def __init__(self, nm):
        self.name = nm
        self.word_index = {}
        self.word_count = {}
        self.index_word = {0:"SOS", 1:"EOS", 2:"PAD"}
        self.n_words = 3 #counts all
    
    def addSentence(self,sentence):
        for word in sentence.split(' '):
            self.addWord(word)
    
    def addWord(self,word):
        if word not in self.word_index:
            self.word_index[word] = self.n_words
            self.word_count[word] = 1
            self.index_word[self.n_words] = word
            self.n_words +=1
        else:
            self.word_count[word]+=1


def file_header(file, ln=10):
    with open(file, 'rb') as df:
        lines = df.readlines()
    for line in lines[:ln]:
        print(line)

def unicode_to_ascii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )

def normalize_string(s):
    s = unicode_to_ascii(s.lower().strip())
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)

    s = re.sub(r"\s+", r" ", s).strip()
    return s

#'''
#iter issue
def read_corpus(file, normalized=True):
    
    with open(file) as f:
        content = f.readlines()


    lines = [line.strip() for line in content]
    if(len(lines)%2 != 0):
        lines.pop()

    iterd = iter(lines)

    if(normalized):
        pairs = [[x, next(iterd)] for x in iterd]
    else:
        pairs = [[normalize_string(x), normalize_string(next(iterd))] for x in iterd]
    
    return pairs
'''

def extract_pairs(conversations, normalized=True):
    qa_pairs = []
    for conversation in conversations:
        # Iterate over all the lines of the conversation
        for i in range(len(conversation["lines"]) - 1):  # We ignore the last line (no answer for it)
            inputLine = conversation["lines"][i]["text"].strip()
            targetLine = conversation["lines"][i+1]["text"].strip()
            # Filter wrong samples (if one of the lists is empty)
            if inputLine and targetLine:
                qa_pairs.append([inputLine, targetLine])
    return qa_pairs

'''

def pair_contained(p):
    return not (len(p[0].split(' ')) < MAX_LENGTH and \
        len(p[1].split(' ')) < MAX_LENGTH)

def filtered_pairs(pairs):
    return [pair for pair in pairs if pair_contained(pair)]

def prep_data(file, corpus_name):
    pairs = read_corpus(file)
    corpus = Corpus(corpus_name)
    
    print("Total sentence pairs: {!s}".format(len(pairs)))
    pairs = filtered_pairs(pairs)
    print("After Filter: {!s} total dialog pairs".format(len(pairs)))
    for pair in pairs:
        corpus.addSentence(pair[0])
        corpus.addSentence(pair[1])
    
    print("Words Counted: ", corpus.n_words)
    dir = os.path.join(data_dir, 'training_data', corpus_name)
    print("DIR:", dir)
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    torch.save(corpus, os.path.join(dir, '{!s}.tar'.format('corpus')))
    torch.save(pairs, os.path.join(dir, '{!s}.tar'.format('pairs')))

    return corpus, pairs

def loadPreparedData(file):
    corpus_name = file.split('/')[-1].split('.')[0]

    try:
        print("Loading train data ...")
        corpus = torch.load(os.path.join(data_path, 'training_data', corpus_name ,'corpus.tar'))
        pairs = torch.load(os.path.join(data_path, 'training_data', corpus_name ,'pairs.tar'))
    except FileNotFoundError:
        print("Saved data not found, start preparing training data ...")
        corpus, pairs = prep_data(file, corpus_name)

    return corpus, pairs


        


#prep_data('movie_lines.txt', 'Cornell Movie Corpus')
#loadPreparedData(os.path.join(data_path,'training_data', 'Cornell Movie Corpus'))
#read_corpus('movie_lines.txt')