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



def get_dict():#把已经存在的近义词反义词词典读入到三个list中
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


    
def divide_three_dataset(lis,test,label,unlabel):
    for i in range(0,len(lis)):
        if len(test)<200 and len(label)<100 and len(unlabel)<700:
            
            a=random.randint(1, 11)
            if a==1:
                label.append(lis[i])
            elif a==2 or a==3:
                test.append(lis[i])
            else:
                unlabel.append(lis[i])
                
        elif len(test)<200 and len(label)<100:
            a=random.randint(1, 4)
            if a==1:
                label.append(lis[i])
            elif a==2 or a==3:
                test.append(lis[i])
        elif len(test)<200 and len(unlabel)<700:
            a=random.randint(1, 10)
            if a==1 or a==2:
                test.append(lis[i])
            else:
                unlabel.append(lis[i])
            
        elif len(label)<100 and len(unlabel)<700:
            a=random.randint(1, 9)
            if a==1:
                label.append(lis[i])
            else:
                unlabel.append(lis[i])
            
        elif len(label)<100:
            label.append(lis[i])
            
        elif len(unlabel)<700:
            unlabel.append(lis[i])
            
        elif len(test)<200:
            test.append(lis[i])
   




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

    word=[]
    antonym=[]
    synonym=[]
    
    get_dict(word,antonym,synonym)

    neg_test=[]  #20%
    pos_test=[]
    neg_label=[]  #10%
    pos_label=[]
    neg_unlabel=[]  #70%
    pos_unlabel=[]
    divide_three_dataset(lis_neg,neg_test,neg_label,neg_unlabel)
    divide_three_dataset(lis_pos,pos_test,pos_label,pos_unlabel)
    
    
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
