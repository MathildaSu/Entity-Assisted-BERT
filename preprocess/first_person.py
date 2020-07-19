import sys
import json
from os import listdir
from os.path import isfile, join
import re
import argparse
import pickle 
def run_process(fname,fpath):
    sentences = []
    with open(join(fpath,fname),'r') as fin:
        doc = fin.read()
    for line in doc.split('\n')[:-1]:
        # print(line)
        segs = line.split('\t')
        # print(segs)
        sentence = re.sub(r'(.|,|!) *((I )|(me )|(Me )|(We)|(we))',segs[1],segs[2])
        sentences.append(sentence)
    fout = join('CLEF/test/',f.rsplit('.',1)[0] + '_fp.pkl')
    with open(fout,'wb') as fout:
        pickle.dump(sentences,fout)


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
        for f in files:
            run_process(f,args.folder)
