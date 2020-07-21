import json
import pickle
from os import listdir
from os.path import isfile, join
import argparse
import pandas as pd
import nltk
import xml.etree.ElementTree as ET
import shlex,subprocess
import re

resturl = "http://localhost:2222/rest/annotate"


def run_fp(speaker,sentence):
    first_person = ['I','me','Me','We','we']
    for i, word in enumerate(sentence):
        if word in first_person:
            sentence[i] = speaker
    return sentence


def get_entities(tokens):
    pos = nltk.pos_tag(tokens)
    sentence = ' '.join(tokens)
    sentence = sentence.replace("'", "\\'")
    sentence = sentence.replace('"', "")
    # print(sentence)
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
    return entities, pos, sentence


def get_ready(fname, fpath):
    fname_proc = join(fpath, fname)
    origin_path = 'CLEF2020/clef2020-factchecking-task5/test-input/test-input'
    fname_orig = join(origin_path, fname.split('_coref')[0]+'.tsv')
    with open(fname_proc,'rb') as f:
        sentences = pickle.load(f)
    df = pd.read_csv(fname_orig, sep='\t', names=['index','speaker','sentence'],delimiter=None, dtype=None)
    file_pos = []
    file_entities = []
    file_sentence = []
    for (index, row),proc_sent in zip(df.iterrows(),sentences):
        print('pre-fp',proc_sent)
        s = run_fp(row['speaker'],proc_sent)
        print('post-fp',s)
        ents, pos, sentence = get_entities(s)
        print('pre-en',sentence)
        print('ent',ents)
        print('pos',pos)
        file_pos.append(pos)
        file_entities.append(ents)
        file_sentence.append(sentence)

    fenout = join('CLEF_final/', fname.rsplit('.',1)[0] + '_en.pkl')
    fposout = join('CLEF_final/', fname.rsplit('.',1)[0] + '_pos.pkl')
    fsentout = join('CLEF_final/', fname.rsplit('.',1)[0] + '_sent.pkl')
    with open(fenout, 'wb') as fp:
        pickle.dump(file_entities, fp)
    with open(fposout, 'wb') as fp:
        pickle.dump(file_pos,fp)
    with open(fsentout, 'wb') as fp:
        pickle.dump(file_sentence,fp)




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
        print('---------------------------------------')
        for f in files:
            get_ready(f,args.folder)

# /nfs/CLEF_coref_post


# curl --silent http://localhost:2222/rest/annotate -H "Accept: text/xml"   --data-urlencode "text=TRUMP \'re going to strengthen TRUMP borders ." \
# --data "confidence=0.3"   --data "support=0"