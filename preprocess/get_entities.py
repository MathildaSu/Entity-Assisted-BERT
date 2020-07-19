import sys
import json
from os import listdir
from os.path import isfile, join
import argparse

from six.moves import input
import pickle
import pandas as pd
import random
from os import listdir
from os.path import isfile, join



import xml.etree.ElementTree as ET
import shlex,subprocess
import re

random.seed(0)

resturl = "http://localhost:2222/rest/annotate"


import nltk
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize



def get_entities(train):
    train_en= []
    test_en = []
    train_pos = []
    test_pos = []
    for i in range(len(train)):
        tokens = nltk.word_tokenize(train[i])
        pos = nltk.pos_tag(tokens)
        sentence = train[i].replace("'", "\\'")
        sentence = sentence.replace('"', "")
        print(sentence)
        entities = []
        try:
            input = 'curl --silent {} -H "Accept: text/xml"   --data-urlencode "text={}" \
                    --data "confidence=0.3"   --data "support=0"'.format(resturl,sentence)
            args = shlex.split(input)
            out = subprocess.Popen(args, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT)
            stdout,stderr = out.communicate()
            stdout = re.sub(r'.+<\?xml','<?xml',str(stdout))
            #stdout = re.sub('</Annotation>.*','</Annotation>',stdout)
            formatted_output = str(stdout).replace('\\n', '\n')
            #formatted_output = re.sub('</Annotation>.*','</Annotation>',formatted_output)
            for c in reversed(formatted_output):
                if c == '>':
                    break
                formatted_output = formatted_output[:-1]
            print(formatted_output)
            root = ET.fromstring(formatted_output)
            for child in root:
                for c in child:
                    entities.append(c.attrib)
            print(entities)
        except: 
            pass
        train_en.append(entities)
        train_pos.append(pos)
    return train_en, train_pos

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Input file/fphath, at least one must be provided.')
    # parser.add_argument('--folder',
    #                help='given folder or not')
    # parser.add_argument('file', type=str, default=None,
    #                     help='path to the file that needs to be processed')    
    parser.add_argument('folder', type=str,default=None,
                        help='path to the folder that all the files need to be processed')
    
    args = parser.parse_args()
    
    # if args.file != None:
    #     run_process(args.file)

    if args.folder != None:
        files = [f for f in listdir(args.folder) if isfile(join(args.folder, f))]
        for fname in files[3:]:
            print(fname)
            with open(args.folder+fname,'rb') as f:
                train = pickle.load(f)
            f_en,f_pos = get_entities(train)
            fenout = join('CLEF_coref/', fname.rsplit('.',1)[0] + '_f_en.pkl')
            fposout = join('CLEF_coref/', fname.rsplit('.',1)[0] + '_f_pos.pkl')
            with open(fenout, 'wb') as fp:
                pickle.dump(f_en, fp)
            with open(fposout, 'wb') as fp:
                pickle.dump(f_pos,fp)


