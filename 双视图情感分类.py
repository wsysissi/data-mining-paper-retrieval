import codecs
import re
import sys
import numpy as np
from numpy import *



def get_text_list(all_review,lis):
    f = open(all_review,"r",encoding='utf-8')
    lines = f.readlines()   
    n=0
    #生成所有字母
    x = [chr(letter).lower() for letter in range (65,91)]
    y = [chr(letter) for letter in range (65,91)]
    az = x + y
    
    for line in lines:
        if n==1:#如果在某一个评论内容中n=1
            words = line.split()
            for word in words:#判断一行中所有的文字词语，并加入中间量a
                if word[0] in az:
                    a.append(word)
        if line[0:13]=="<review_text>": #按照提供的格式，识别开始行，并把中间量a[]初始化，n判断是否在某个评论中=1
            n=1
            a=[]
        if line[0:14]=="</review_text>":#按照提供的格式，识别结束行，并添加中间量到最终输出中，n判断是否在某个评论中=0
            n=0
            lis.append(a)    

    f.close()



def get_dict():
    word=[]
    antonym=[]
    synonym=[]
    f = codecs.open("synonym_antonym_set.txt", mode='r', encoding='utf-8')
    lines = f.readlines()
    for line in lines :
        words = line.split()
        word.append(words[0])
        antonym.append(words[1])
        synonym.append(words[2])
    f.close()
    return word,antonym,synonym


    
def random_chose(lis):
    review_num = len(lis) #计算一共有多少条评论
    unlabelled = random.sample(lis,int(review_num*0.7))#随机取百分之70作为未标记数据
    all_lable_test = lis
    for i in unlabelled:
        all_lable_test.remove(i)#除去为未标记数据
    labelled = random.sample(all_lable_test,int(review_num*0.2))#从剩下的数据中随机取百分之20作为标记数据
    tests = all_lable_test
    for i in labelled:
        tests.remove(i)#除去标记数据
    return tests,labelled,unlabelled

def remove_nagation (original_review):#检测并除去句子列表中的表翻译的单词（not等）
    nagation_lis = ['no','not']
    for word in original_review:
        if ("n't" in word) or (word.lower() in nagation_lis):
            original_review.remove(word)        
    
def reverse_orgreview (org_label,words,antonym,synonym):
    org_review = []
    anti_org_review = []
    for i in org_label:
        for word in i :
            if word in words:#如果该评论中的单词出现在词典原单词列表中，就对那个单词得到反义词
                wordnum = words.index(word)
                anti = antonym[wordnum]
                org_review.append(word)
                anti_org_review.append(anti)
            elif word in synonym:#如果该评论中的单词出现在词典近义词列表中，就对那个单词得到原单词和反义词
                wordnum = synonym.index(word)
                orgword = words[wordnum]
                anti = antonym[wordnum]
                org_review.append(word)
                anti_org_review.append(anti)
            elif word in antonym:#如果该评论中的单词出现在词典反义词列表中，就对那个单词得到原单词和近义词（评论单词的反义词）
                wordnum = antonym.index(word)
                orgword = words[wordnum]
                anti_org = orgword
                anti_syn = synonym[wordnum]
                org_review.append(word)
                anti_org_review.append(anti)
    
def stais(pos_label,word,antonym,synonym,original_dic_pos,antony_dic_pos):
    original=[]
    antony=[]
    for i in range(0,len(pos_label)):
        for j in range(0,len(pos_label[i])):
            if pos_label[i][j] in word:
                original.append(pos_label[i][j])
                l=0
                while l<len(word):
                    if word[l]==pos_label[i][j]:
                        antony.append(antonym[l])
                        break
                    l=l+1
            elif pos_label[i][j] in synonym:
                l=0
                while l<len(word):
                    if synonym[l]==pos_label[i][j]:
                        original.append(word[l])
                        antony.append(antonym[l])
                        break
                    l=l+1
             
            elif pos_label[i][j] in antonym:
                original.append(pos_label[i][j])
                while l<len(word):
                    if antonym[l]==pos_label[i][j]:
                        antony.append(word[l])
                        break
                    l=l+1
           
            else:
                original.append(pos_label[i][j])
                antony.append(pos_label[i][j])
    #delete=["a","an","A","An","the","The","and","I","he","He","this","that",".",",","'","!"]
    selection=["not","isn't","doesn't","don't","wouldn't","didn't","couldn't","can't","won't","No","NO","aren't","haven't"]
    guodu1=[]
    #guodu2=[]
    for i in range(0,len(antony)):
        if antony[i] not in selection :
            guodu1.append(antony[i])

    antony=guodu1
    #original=guodu2
    for i in range(0,len(original)):
        if original_dic_pos.get(original[i])==None:
            original_dic_pos[original[i]]=1
        else:
            original_dic_pos[original[i]]=original_dic_pos[original[i]]+1
    for i in range(0,len(antony)):
        if antony_dic_pos.get(antony[i])==None:
            antony_dic_pos[antony[i]]=1
        else:
            antony_dic_pos[antony[i]]=antony_dic_pos[antony[i]]+1       


def original_classify(original_dic_pos,original_dic_neg,sample):
    neg=1
    pos=1
    len_neg=0
    len_pos=0
    for key in original_dic_pos:
        len_pos=len_pos+original_dic_pos[key]
    for key in original_dic_neg:
        len_neg=len_neg+original_dic_neg[key]
    for i in range(0,len(sample)):
        if sample[i] in list(original_dic_pos.keys()):
            pos=pos*(original_dic_pos[sample[i]]/len_pos)
        if sample[i] in list(original_dic_neg.keys()):
            neg=neg*(original_dic_neg[sample[i]]/len_neg)
    neg=neg*len_neg/(len_neg+len_pos)
    pos=pos*len_pos/(len_neg+len_pos)
    
    if pos>neg:
        return 1
    else:
        return 0
            
def antony_classify(antony_dic_pos,antony_dic_neg,sample):
    neg=1
    pos=1
    len_neg=0
    len_pos=0
    for key in antony_dic_pos:
        len_pos=len_pos+antony_dic_pos[key]
    for key in antony_dic_neg:
        len_neg=len_neg+antony_dic_neg[key]
    for i in range(0,len(sample)):
        if sample[i] in list(antony_dic_pos.keys()):
            pos=pos*(antony_dic_pos[sample[i]]/len_pos)
        if sample[i] in list(antony_dic_neg.keys()):
            neg=neg*(antony_dic_neg[sample[i]]/len_neg)
    neg=neg*len_neg/(len_neg+len_pos)
    pos=pos*len_pos/(len_neg+len_pos)
    
    if pos>neg:
        return 1
    else:
        return 0


def dual_classify(dual_dic_neg,dual_dic_pos,sample):


    neg=1
    pos=1
    len_neg=0
    len_pos=0
    
    for key in dual_dic_pos:
        len_pos=len_pos+dual_dic_pos[key]
    for key in dual_dic_neg:
        len_neg=len_neg+dual_dic_neg[key]
    for i in range(0,len(sample)):
        if sample[i] in list(dual_dic_pos.keys()):
            pos=pos*(dual_dic_pos[sample[i]]/len_pos)
        if sample[i] in list(dual_dic_neg.keys()):
            neg=neg*(dual_dic_neg[sample[i]]/len_neg)
    neg=neg*len_neg/(len_neg+len_pos)
    
    pos=pos*len_pos/(len_neg+len_pos)
    if pos>neg:
        return 1
    else:
        return 0

def assemble_dual(antony_dic_pos,antony_dic_neg,original_dic_pos,original_dic_neg,dual_dic_neg,dual_dic_pos):
    
    for key in original_dic_pos:
        if key not in list(antony_dic_neg.keys()):
            dual_dic_pos[key]=original_dic_pos[key]
        else:
            dual_dic_pos[key]=original_dic_pos[key]+antony_dic_neg[key]
    for key in antony_dic_neg:
        if key not in list(original_dic_pos.keys()):
            dual_dic_pos[key]=antony_dic_neg[key] 

    for key in original_dic_neg:
        if key not in list(antony_dic_pos.keys()):
            dual_dic_neg[key]=original_dic_neg[key]
        else:
            dual_dic_neg[key]=original_dic_neg[key]+antony_dic_pos[key]
    for key in antony_dic_pos:
        if key not in list(original_dic_neg.keys()):
            dual_dic_neg[key]=antony_dic_pos[key]

def assemble_dual2(antony_dic_pos,antony_dic_neg,original_dic_pos,original_dic_neg,dual_dic_neg,dual_dic_pos):
    
    for key in original_dic_pos:
        if key not in list(original_dic_neg.keys()):
            dual_dic_pos[key]=original_dic_pos[key]
        else:
            dual_dic_pos[key]=original_dic_pos[key]+original_dic_neg[key]
    for key in original_dic_neg:
        if key not in list(original_dic_pos.keys()):
            dual_dic_pos[key]=original_dic_neg[key] 

    for key in antony_dic_neg:
        if key not in list(antony_dic_pos.keys()):
            dual_dic_neg[key]=antony_dic_neg[key]
        else:
            dual_dic_neg[key]=antony_dic_neg[key]+antony_dic_pos[key]
    for key in antony_dic_pos:
        if key not in list(antony_dic_neg.keys()):
            dual_dic_neg[key]=antony_dic_pos[key]



def main():
    lis_neg=[]
    lis_pos=[]
    get_text_list("negative.reviewdvd",lis_neg)
    get_text_list("positive.reviewdvd",lis_pos)

    dic = get_dict()
    word=dic[0]
    antonym=dic[1]
    synonym=dic[2]

    negt = random_chose(lis_neg)
    post = random_chose(lis_pos)
    neg_test=negt[0]  
    pos_test=post[0]
    neg_label=negt[1]  
    pos_label=post[1]
    neg_unlabel=negt[2]  
    pos_unlabel=post[2]

    
    unlabel=neg_unlabel+pos_unlabel

    while len(unlabel)>0:
        
        original_dic_pos={}
        antony_dic_pos={}
        original_dic_neg={}
        antony_dic_neg={}

        stais(pos_label,word,antonym,synonym,original_dic_pos,antony_dic_pos)  
        stais(neg_label,word,antonym,synonym,original_dic_neg,antony_dic_neg)  

        dual_dic_neg={}
        dual_dic_pos={}
        assemble_dual2(antony_dic_pos,antony_dic_neg,original_dic_pos,original_dic_neg,dual_dic_neg,dual_dic_pos)#semble_dual2和1的区别，2的效率更好
        
        guodu=[]
    
    #(original_classify(original_dic_pos,original_dic_neg,neg_unlabel[1]))
    #(antony_classify(antony_dic_pos,antony_dic_neg,neg_unlabel[1]))
        x=[]
        n=len(unlabel)
        for i in range(0,len(unlabel)):
        
            if original_classify(original_dic_pos,original_dic_neg,unlabel[i])==dual_classify(dual_dic_neg,dual_dic_pos,unlabel[i]):#antony_classify(antony_dic_pos,antony_dic_neg,unlabel[i]):可以实验不同条件下的概率，如dual配oiginal效果最好
                if original_classify(original_dic_pos,original_dic_neg,unlabel[i])==1:
                    pos_label.append(unlabel[i])
                
                else:
                    neg_label.append(unlabel[i])
                x.append(i)
    
        for i in range(0,len(unlabel)):
            if i not in x:
                guodu.append(unlabel[i])
        unlabel=guodu
        if n==len(unlabel):
            break
    print(len(neg_label))
    print(len(pos_label))
    print(len(unlabel))
    test=0
    for i in range(0,len(neg_test)):
        if dual_classify(dual_dic_neg,dual_dic_pos,neg_test[i])==0:
            test=test+1
    print(test)
    for i in range(0,len(pos_test)):
        if antony_classify(antony_dic_pos,antony_dic_neg,pos_test[i])==1:
            test=test+1
    print(test)
    print(test/(len(neg_test)+len(pos_test)))
                
    
main()
