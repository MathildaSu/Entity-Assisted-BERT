import pickle
import nltk
from nltk.tokenize import word_tokenize
import json
import argparse
from os import listdir
from os.path import isfile, join

def preproc(fname,fpath):
    result = []
    with open(join(fpath,fname),'r')as fin, open(join('CLEF_coref/',fname.rsplit('.',1)[0]+'_coref.jsonl'),'w') as fout:
        data = fin.read()
        setences = data.split('\n')
        for i,line in enumerate(setences[:-2]):
            triplet1 = line.split('\t')
            triplet2 = setences[i+1].split('\t')
            s1 = word_tokenize(triplet1[-1])
            s2 = word_tokenize(triplet2[-1])
            speaker1 = ["spk1"] * len(s1)
            if triplet2[1] == triplet1[1]:
                speaker2 = ["spk1"] * len(s2)
            else:
                speaker2 = ["spk2"] * len(s2)
            j_file = {
                        "clusters": [],
                        "doc_key": "nw",
                        "sentences": [s1, s2],
                        "speakers": [speaker1, speaker2]
                    }
            fout.write(json.dumps(j_file))
            fout.write('\n')

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
        for fname in files:
            print(fname)
            preproc(fname,args.folder)
