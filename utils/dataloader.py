import os
import re
import unicodedata

#Word tokens
PAD_token = 0  # Padding short sentences
SOS_token = 1  # Start-of-sentence
EOS_token = 2  # End-of-sentence
MAX_LENGTH = 15 #Self Explanitory

class Dialog:
    def __init__(self, name):
        self.name = name




def get_file_header(file, ln=10):
    with open(file, 'rb') as df:
        lines = file.readlines()
    for line in lines[:n]:
        print(line)

def loadLines(fileName, fields):
    lines = {}
    with open(fileName, 'r', encoding='iso-8859-1') as f:
        for line in f:
            values = line.split(" +++$+++ ")
            # Extract fields
            lineObj = {}
            for i, field in enumerate(fields):
                lineObj[field] = values[i]
            lines[lineObj['lineID']] = lineObj
    return lines


def loadLines(fileName, fields):
    lines = {}
    with open(fileName, 'r', encoding='iso-8859-1') as f:
        for line in f:
            values = line.split(" +++$+++ ")
            # Extract fields
            lineObj = {}
            for i, field in enumerate(fields):
                lineObj[field] = values[i]
            lines[lineObj['lineID']] = lineObj
    return lines

def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )

def normalizeString(s):
    s = unicodeToAscii(s.lower().strip())
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
    s = re.sub(r"\s+", r" ", s).strip()
    return s

def readDialog(dialogs, normalized=True):
    
    with open(dialogs) as f:
        content = f.readlines()


    lines = [dialog.strip() for dialog in content]
    iterd = iter(lines)
    print(type(next(iterd)))

    if(normalized):
        dialog_pairs = [[x, next(iterd)] for x in iterd]
    else:
        dialog_pairs = [[normalizeString(x), normalizeString(next(iterd))] for x in iterd]
    
    return dialog_pairs

def pair_contained(p):
    return not (len(p[0].split(' ')) < MAX_LENGTH and \
        len(p[1].split(' ')) < MAX_LENGTH)

def filteredPairs(pairs):
    return [pair for pair in pairs if pair_contained(pair)]

def dataParse(dialogs, dialog_name):
    pairs = readDialog(dialogs)
    print("Total sentence pairs: {!s}".format(len(pairs)))
    pairs = filteredPairs(pairs)
    print("After Filter: {!s} total dialog pairs".format(len(pairs)))



    
