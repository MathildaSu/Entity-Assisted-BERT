# -*- coding: utf-8 -*-
import pickle 
from os import listdir
import argparse
from os.path import isfile, join
from wikipedia2vec import Wikipedia2Vec
import numpy as np
# import pandas as pd

MODEL_FILE = './models/enwiki_20180420_win10_300d.pkl'

def get_processed_test(ent_path, sent_path, f_ent, f_sent):
    with open(join(ent_path,f_ent),'rb') as fen:
        enl = pickle.load(fen)
    with open(join(sent_path,f_sent),'rb') as fsent:
        sentence = pickle.load(fsent)
    data = []
    wiki2vec = Wikipedia2Vec.load(MODEL_FILE)
    nu = np.full((1,300),-1.0).flatten()
    URL = []
    for URI in enl:
        num = len(URI)
        U = []
        if num == 0:
            URL.append([])
            continue
        if num == 1:
            URL.append([URI[0]['URI']])
            continue
        else:
            for i in range(num):
                U.append(URI[i]['URI'])
            U = set(U)
            URL.append(U)

    print(len(URL),len(sentence))
    for URI,s,n in zip(URL,sentence,range(0,500000)):
        # print(df['line_number'][i])
        num = len(URI)
        URI = list(URI)
        if num == 0:
            data.append(['NA','NA',nu,nu,-1,s,n])
            print(data[-1][-1])
            continue
        if num == 1: 
            en1_name = URI[0].split('/')[-1].replace('_',' ')
            try: 
                en1 = wiki2vec.get_entity_vector(en1_name)
            except:
                en1 = nu
            data.append([en1_name,'NA',en1,nu,-1,s,n])
            print(data[-1][-1])
            continue
        for i in range(num):
            en1_name = URI[i].split('/')[-1].replace('_',' ')
            try:
                en1 = wiki2vec.get_entity_vector(en1_name)
            except:
                en1 = nu
            for j in range(i+1,num):
                en2_name = URI[j].split('/')[-1].replace('_',' ')
                try:
                    en2 = wiki2vec.get_entity_vector(en2_name)
                except:
                    en2 = nu
                data.append([en1_name, en2_name,en1,en2,-1,s,n])
                print(data[-1][-1])
    # print(len(data))
    return data 

def get_processed_train(enl,sentence,df):
    data = []
    wiki2vec = Wikipedia2Vec.load(MODEL_FILE)
    nu = np.full((1,300),-1.0).flatten()
    URL = []
    for URI in enl:
        num = len(URI)
        U = []
        if num == 0:
            URL.append([])
            continue
        if num == 1:
            URL.append([URI[0]['URI']])
            continue
        else:
            for i in range(num):
                U.append(URI[i]['URI'])
            U = set(U)
            URL.append(U)

    print(len(URL),len(sentence))
    for URI,s,l,n in zip(URL,sentence,label[:,2],range(1,3000) ):
        # print(df['line_number'][i])
        num = len(URI)
        URI = list(URI)
        if num == 0:
            data.append(['NA','NA',nu,nu,l,s,n])
            print(data[-1][-1])
            continue
        if num == 1: 
            en1_name = URI[0].split('/')[-1].replace('_',' ')
            try: 
                en1 = wiki2vec.get_entity_vector(en1_name)
            except:
                en1 = nu
            data.append([en1_name,'NA',en1,nu,l,s,n])
            print(data[-1][-1])
            continue
        for i in range(num):
            en1_name = URI[i].split('/')[-1].replace('_',' ')
            try:
                en1 = wiki2vec.get_entity_vector(en1_name)
            except:
                en1 = nu
            for j in range(i+1,num):
                en2_name = URI[j].split('/')[-1].replace('_',' ')
                try:
                    en2 = wiki2vec.get_entity_vector(en2_name)
                except:
                    en2 = nu
                data.append([en1_name, en2_name,en1,en2,l,s,n])
                print(data[-1][-1])
    # print(len(data))
    return data 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode",help = "Processing test or train data",
                        type = str, required = True)
    parser.add_argument("--ent_path",help = "The path that the ent file is in",
                        type = str, required = True)
    parser.add_argument("--sentence_path",help = "The path that the sentence is in",
                        type = str, required = True)
    parser.add_argument("--label_path",help = "The path that the labeled file is in",
                        type = str, required = False)
    # parser.add_argument("--file_name",help = "The file you want to parse",
                        # type = str, required = True)
    

    args = parser.parse_args()
    if args.ent_path != None:
        fs_ent = [f for f in listdir(args.ent_path) if isfile(join(args.ent_path, f)) and f.endswith('_en.pkl')]

    if args.sentence_path != None:
        fs_sent = [f.split('_en.pkl')[0]+'_sent.pkl' for f in fs_ent]

    if args.mode == 'test':
        for f_ent, f_sent in zip(fs_ent, fs_sent):
            processed = get_processed_test(args.ent_path, args.sentence_path, f_ent, f_sent)
            with open(join('./data/test/',f_ent.split('_en.pkl')[0]+'.pkl'),'wb') as fd:
                pickle.dump(processed, fd)

    # else:
    #     fs_label = [f.split('_en.pkl')[0]+'.tsv' for f in f_ent]
    #     for f_ent, f_sent, f_label in zip(fs_ent, fs_sent,fs_label):
    #         processed = get_processed_train(args.ent_path, args.sentence_path, args.label_path, f_ent, f_sent,f_label)
    #         with open(join('/nfs/CLEF/data/train/',args.ent_name),'wb') as fd:
    #             pickle.dump(processed, fd)
    
    


# /nfs/CLEF_final
# python preprocess/get_entity_emb.py --mode='test' --ent_path=/nfs/CLEF_final --sentence_path=/nfs/CLEF_final