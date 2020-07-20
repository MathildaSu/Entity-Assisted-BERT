import json
import pickle
from os import listdir
from os.path import isfile, join
import argparse

def check_sentence(sentence1,sentence2,ind1,ind2):
    if ind1 < len(sentence1):
        return sentence1, 1, ind1, ind2
    else: 
        return sentence2, 2, ind1 - len(sentence1), ind2 - len(sentence1)


def replace(sentence1,sentence2,cs,ce,rs,re):
    sentence_for_replace, ind1, cs, ce = check_sentence(sentence1,sentence2,cs,ce)
    sentence_to_be_replaced, ind2, rs, re = check_sentence(sentence1,sentence2,rs,re)
    # print(sentence_for_replace, cs, ce)
    # print(sentence_to_be_replaced,rs, re)
    if ind2 == 2:
        for_replace = [' '] * (re-rs+1)
        # print(for_replace)
        for_replace[0] = ' '.join(sentence_for_replace[cs:ce+1])
        sentence_to_be_replaced[rs:re+1]=for_replace
        return sentence_to_be_replaced    
    return sentence2

def run_post_proc(fname, fpath):
    sentences = []
    with open(join(fpath,fname),'r') as fin:
        filedata = fin.read()
    filedata = ''.join(filedata)
    filedata = filedata.split('\n')
    data = json.loads(filedata[0])
    sentence1 = data['sentences'][0]
    sentences.append(sentence1)
    for line in filedata[:-1]:
        # print(line)
        data = json.loads(line)
        sentence1 = sentences[-1]
        sentence2 = data['sentences'][1]
        cluster_lists = data['predicted_clusters']
        for cluster in cluster_lists:
            cs = cluster[0][0]
            ce = cluster[0][1]
            for rs,re in cluster[1:]:
                sentence2 = replace(sentence1,sentence2,cs,ce,rs,re)
        # print(sentence2)
        sentences.append(sentence2)
    fout = join('/nfs/CLEF_coref_post/',fname.rsplit('.')[0]+'.pkl')
    with open(fout,'wb') as fout:
        pickle.dump(sentences,fout)
    print(sentences)



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
            run_post_proc(f,args.folder)



# python post_proc.py /nfs/CLEF_coref
# /nfs/CLEF_coref_post/20160303_GOP_michigan_coref.pkl

# import pickle
# with open('/nfs/CLEF_coref_post/20160303_GOP_michigan_coref.pkl','rb') as f:
#     data = pickle.load(f)

# tree = git log --graph --decsorate --pretty=format:'%C(bold yellow)%h%Creset -%C(auto)%d %s %C(bold cyan)(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
