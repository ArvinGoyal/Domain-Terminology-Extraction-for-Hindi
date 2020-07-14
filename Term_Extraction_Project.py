
# coding: utf-8

# In[1]:


#from selenium import webdriver
import datetime
import time
import os
import re
from collections import defaultdict, Counter
import numpy as np
import sys


# In[2]:


def get_NNP_Word(domain_tokens):
    filters = ["NNP","NNP JJ", "JJ NNP" "NNP NN","JJ NN","JJ NN NN"]
    
    NNP_Word = []
    
    for f in filters:
        filter_token = f.split()
        if len(filter_token) == 1:
            token_length = len(domain_tokens)
        elif len(filter_token) == 2:
            token_length = len(domain_tokens) - 2
        elif len(filter_token) == 3:
            token_length = len(domain_tokens) - 4
            
        for i in range(token_length):
            if len(filter_token) == 1:
                if domain_tokens[i] == filter_token[0]:
                    NNP_Word.append(domain_tokens[i-1])
                    
            elif len(filter_token) == 2:
                if domain_tokens[i] == filter_token[0] and domain_tokens[i+2] == filter_token[1]:
                    NNP_Word.append(domain_tokens[i-1] + " " + domain_tokens[i+1])
                    
                    
            elif len(filter_token) == 3:
                if domain_tokens[i] == filter_token[0] and domain_tokens[i+2] == filter_token[1] and domain_tokens[i+4] == filter_token[2]:
                    NNP_Word.append(domain_tokens[i-1] + " " + domain_tokens[i+1] + " " + domain_tokens[i+3])
                    
        
    return NNP_Word


# In[3]:


def get_seperated_terms(term_list,sep):
    new_term_list = []
    for term in term_list:
        word_list = term.split(sep)
    
        if len(word_list) == 1:
            new_term_list.append(term)
        elif len(word_list) > 1:
            for word in word_list:
                if len(word) > 0:
                    new_term_list.append(word)
    return new_term_list

def get_Cleaned_Words(string_list):
    #pick only Hindi Words
    Term_list = []
    Hindi_regex = re.compile(r'[\u0900-\u097F]+')
    
    for term in string_list:
        hindi_term = Hindi_regex.findall(term)
        if len(hindi_term) == 1:
            Term_list.extend(hindi_term)
        elif len(hindi_term) > 1:
            Term_list.append(term)
    Term_list_c1 = get_seperated_terms(Term_list, '/')
    Term_list_c2 = get_seperated_terms(Term_list_c1,'|')
    return Term_list_c2


def get_NNP_Counter(Terms_list):
    NNP_Counter = Counter()
    for i in Terms_list:
        NNP_Counter[i] += 1
    return NNP_Counter


# In[4]:


#Arvin - Start
def clean_stopword(sub_trm,stop_word_lst):
    sw_flg = 'N'
    for sw in stop_word_lst:
        if sub_trm == sw:
            sw_flg = 'Y'
    if sw_flg == 'Y':
        sub_trm = ''
    return sub_trm

def generate_stem_word(word):
    suffixes = {
    #1: [u"ो",u"े",u"ू",u"ु",u"ी",u"ि",u"ा"],
    #2: [u"कर",u"ाओ",u"िए",u"ाई",u"ाए",u"ने",u"नी",u"ना",u"ते",u"ीं",u"ती",u"ता",u"ाँ",u"ां",u"ों",u"ें"],        
    #3: [u"ाकर",u"ाइए",u"ाईं",u"ाया",u"ेगी",u"ेगा",u"ोगी",u"ोगे",u"ाने",u"ाना",u"ाते",u"ाती",u"ाता",u"तीं",u"ाओं",u"ाएं",u"ुओं",u"ुएं",u"ुआं"],
    #4: [u"ाएगी",u"ाएगा",u"ाओगी",u"ाओगे",u"एंगी",u"ेंगी",u"एंगे",u"ेंगे",u"ूंगी",u"ूंगा",u"ातीं",u"नाओं",u"नाएं",u"ताओं",u"ताएं",u"ियाँ",u"ियों",u"ियां"],
    #5: [u"ाएंगी",u"ाएंगे",u"ाऊंगी",u"ाऊंगा",u"ाइयाँ",u"ाइयों",u"ाइयां"]} 


    1: [u"ो ", u"ओ"],
    2: [u"ों",u"ओं",u"एं"],
    3: [u"यें",u"याँ",u"यां",u"यों"],
    4: [],
    5: []} 
    
    
    for L in 5, 4, 3, 2, 1:
        if len(word) > L + 1:
            for suf in suffixes[L]:
                if word.endswith(suf):
                    return word[:-L]

    # specail case to change from aane to aana. for example धबराने  to धबराना
    suf = u"ाने"
    if word.endswith(suf) and len(word) > 4:
        word = word[:-3] + u"ाना"
    
    return word    
    
    
def remove_stopword_and_stemword(list,stop_word_lst):
    cln_list = []
    #stop_word_lst = ['एक', 'दो', 'तीन', 'चार', 'पाँच', 'छः', 'सात', 'आठ', 'नौ', 'दस', 'बीस', 'तीस', 'चालीस', 'पचास','अत', 'अपना', 'अपनी', 'अपने', 'अभी', 'अंदर', 'आदि', 'आप', 'इत्यादि', 'इन ', 'इनका', 'इन्हीं', 'इन्हें', 'इन्हों', 'इस', 'इसका', 'इसकी', 'इसके', 'इसमें', 'इसी', 'इसे', 'उन', 'उनका', 'उनकी', 'उनके', 'उनको', 'उन्हीं', 'उन्हें', 'उन्हों', 'उस', 'उसके', 'उसी', 'उसे', 'एक', 'एवं', 'एस', 'ऐसे', 'और', 'कई', 'कर', 'करता', 'करते', 'करना', 'करने', 'करें', 'कहते', 'कहा', 'का', 'काफ़ी', 'कि', 'कितना', 'किन्हें', 'किन्हों', 'किया', 'किर', 'किस', 'किसी', 'किसे', 'की', 'कुछ', 'कुल', 'के', 'को', 'कोई', 'कौन', 'कौनसा', 'गया', 'घर', 'जब', 'जहाँ', 'जा', 'जितना', 'जिन', 'जिन्हें', 'जिन्हों', 'जिस', 'जिसे', 'जीधर', 'जैसा', 'जैसे', 'जो', 'तक', 'तब', 'तरह', 'तिन', 'तिन्हें', 'तिन्हों', 'तिस', 'तिसे', 'तो', 'था', 'थी', 'थे', 'दबारा', 'दिया', 'दुसरा', 'दूसरे', 'दो', 'द्वारा', 'न', 'नके', 'नहीं', 'ना', 'निहायत', 'नीचे', 'ने', 'पर', 'पहले', 'पूरा', 'पे', 'फिर', 'बनी', 'बही', 'बहुत', 'बाद', 'बाला', 'बिलकुल', 'भी', 'भीतर', 'मगर', 'मानो', 'मे', 'में', 'यदि', 'यह', 'यहाँ', 'यही', 'या', 'यिह', 'ये', 'रखें', 'रहा', 'रहे', 'ऱ्वासा', 'लिए', 'लिये', 'लेकिन', 'व', 'वग़ैरह', 'वर्ग', 'वह', 'वहाँ', 'वहीं', 'वाले', 'वुह', 'वे', 'सकता', 'सकते', 'सबसे', 'सभी', 'साथ', 'साबुत', 'साभ', 'सारा', 'से', 'सो', 'संग', 'ही', 'हुआ', 'हुई', 'हुए', 'है', 'हैं', 'हो', 'होता', 'होती', 'होते', 'होना', 'होने']
    #list = ['अत', 'अपना', 'अपना चरणो', 'प्रथम चरण', 'प्रथम','चरण', 'चरणो']
    
    for trm in list:
        trm_sub_list = trm.split()
        trm_temp = ''
        for sub_trm in trm_sub_list:
            sub_trm = clean_stopword (sub_trm,stop_word_lst)
            sub_trm = generate_stem_word (sub_trm)
            if len(sub_trm) > 0:
                trm_temp = trm_temp + sub_trm + ' '
        trm_temp = trm_temp[: len (trm_temp)-1]    
        
        #if trm_temp != trm:
        #    print ("Change the term: ",trm, '  to new term: ',trm_temp,'')
        if len(trm_temp) > 1:
            cln_list.append(trm_temp)
    #print (cln_list)
    return cln_list


# In[5]:


def SplitTextfromTags(pathList,DomainList,stop_word_lst):
    Tags = defaultdict(dict)
    Texts = defaultdict(dict)
    Terms = defaultdict(Counter)
    CorpusLen = defaultdict(Counter)
    TermList =[]
    for i, path in enumerate(pathList):
        tagDict = {}
        textDict ={}
        NNP_WordsDict = {}
        files =[]
        for r, d, f in os.walk(path):
            for file in f:
                if '.txt' in file:
                    files.append(file)
            os.chdir(path)
            #print(os.getcwd())
            
                
        for fileName in files:
            #print(fileName)
            file1= open(fileName,"r",encoding='utf-8')
            taggedtext = file1.readlines()
            taggedList = taggedtext[0].split()
            
            taggedList = [w.replace('\u200d', '') for w in taggedList]
            
            
            temp_text = taggedList[0::2]
            temp_tags =taggedList[1::2]
            tagDict[fileName] = " ".join(temp_tags)
            textDict[fileName] = " ".join(temp_text)
            CorpusLen[DomainList[i]][fileName] = len(temp_text)
            
            NNP_Word = get_NNP_Word(taggedList)
            NNP_Cleaned = get_Cleaned_Words(NNP_Word)

            NNP_Cleaned = remove_stopword_and_stemword (NNP_Cleaned,stop_word_lst)
            
            NNP_Counter = get_NNP_Counter(NNP_Cleaned)
            
            NNP_WordsDict[fileName] = NNP_Counter
            TermList.append(NNP_Cleaned)
            file1.close()
        
            
        Tags[DomainList[i]] = tagDict
        Texts[DomainList[i]] = textDict
        Terms[DomainList[i]] = NNP_WordsDict
        
        
    return Tags,Texts,Terms,TermList,CorpusLen
    
   


# In[6]:


def getDomainLength(CorpusLen):
    DomainLength = {}
    for key in CorpusLen.keys():
        len_temp = 0
        for inner_key in CorpusLen[key].keys():
            len_temp = len_temp + CorpusLen[key][inner_key]
        
        DomainLength[key] = len_temp
        
    return DomainLength
    
    


# In[7]:


#getDomainLength(CorpusLen)


# In[8]:


def getWordCountInDomain(word,Terms):
    
    Domain_count ={}
    for key in Terms.keys():
        total_count = 0
        for inner_key in Terms[key].keys():
            if Terms[key][inner_key][word] >0:
                total_count = total_count +  Terms[key][inner_key][word]
                
        Domain_count[key] = total_count
    return Domain_count
            
def getWordCountInDomain(word,Terms):
    
    Domain_count ={}
    for key in Terms.keys():
        total_count = 0
        for inner_key in Terms[key].keys():
            if Terms[key][inner_key][word] >0:
                total_count = total_count +  Terms[key][inner_key][word]
                
        Domain_count[key] = total_count
    return Domain_count


def CalculateNCI(word,Terms,CorpusLen):
    
    DomainLength = getDomainLength(CorpusLen)
    
    WordCountsInDomain = getWordCountInDomain(word,Terms)
    TotalCountAcrossDomain = sum(WordCountsInDomain.values())
    
    Norm_Prob_D_Given_Word = {}
    
    for cKey in WordCountsInDomain.keys():
        p_temp = 0
        p_temp = WordCountsInDomain[cKey]/(TotalCountAcrossDomain*DomainLength[cKey])
        Norm_Prob_D_Given_Word[cKey] = p_temp
        
    Total_P = sum(Norm_Prob_D_Given_Word.values())
        
    P_Prime_D_Given_Word = {}
    for oKey in Norm_Prob_D_Given_Word.keys():
        p_prime_temp = 0
        p_prime_temp = Norm_Prob_D_Given_Word[oKey]/Total_P
            
        P_Prime_D_Given_Word[oKey] = p_prime_temp
            
    NCI = 0 
    for fKey in P_Prime_D_Given_Word.keys():
        if P_Prime_D_Given_Word[fKey] ==0:
            pass
        else:
            temp_nci = P_Prime_D_Given_Word[fKey]*np.log(P_Prime_D_Given_Word[fKey])
            NCI = NCI + temp_nci
        
    NCI = NCI*(-1)
    return NCI
        
    
                
def CalCulateNDI(word,Terms,CorpusLen):
    Norm_Prob_Doc_Given_Word = defaultdict(dict)
    Prime_Prob_Doc_Given_Word = defaultdict(dict)
    WordCountsInDomain = getWordCountInDomain(word,Terms)
    
    for cKey in Terms.keys():
        for fileName in Terms[cKey].keys():
            if WordCountsInDomain[cKey] ==0:
                temp_norm_p =0
            else:
                try:
                    temp_norm_p = Terms[cKey][fileName][word]/(WordCountsInDomain[cKey]*CorpusLen[cKey][fileName])
                except ZeroDivisionError:
                    temp_norm_p = 0 
                    
            Norm_Prob_Doc_Given_Word[cKey][fileName] = temp_norm_p
            
    for dKey in Norm_Prob_Doc_Given_Word.keys():
        sum_norm_prob = sum(Norm_Prob_Doc_Given_Word[dKey].values())
        for fileName2 in Norm_Prob_Doc_Given_Word[dKey].keys():
            
            if sum_norm_prob ==0:
                Prime_Prob_Doc_Given_Word[dKey][fileName2] =0
            else:
                try:
            
                    Prime_Prob_Doc_Given_Word[dKey][fileName2] = Norm_Prob_Doc_Given_Word[dKey][fileName2]/sum_norm_prob
                except ZeroDivisionError:
                    Prime_Prob_Doc_Given_Word[dKey][fileName2] = 0 
    NDI_dict = {}
    
    for fKey in Prime_Prob_Doc_Given_Word.keys():
        NDI = 0
        for fileName3 in Prime_Prob_Doc_Given_Word[fKey].keys():
            if Prime_Prob_Doc_Given_Word[fKey][fileName3] ==0:
                pass
            else:
                temp_ndi = Prime_Prob_Doc_Given_Word[fKey][fileName3]*np.log(Prime_Prob_Doc_Given_Word[fKey][fileName3])
                NDI = NDI + temp_ndi
            
        NDI_dict[fKey] = NDI*(-1)
        
            
    
            
    return NDI_dict
                


# In[23]:


def main():
    
    cur_wd = os.getcwd()
    print('Program Started')
    arguments = sys.argv[1:]
    try: 
       CorpusPathFile = arguments[0]
       StopWordFile = arguments[1]
       DomainsFile = arguments[2]
    except IndexError:
        print('Not enough parameters to run')
        sys.exit()
    CorpusPathFile = os.path.abspath(CorpusPathFile)
    StopWordFile = os.path.abspath(StopWordFile)
    DomainsFile = os.path.abspath(DomainsFile)
    

    try:
        pathFile =open(CorpusPathFile,"r",encoding='utf-8')

        pathData = pathFile.readlines()
        pathFile.close()
    except:
        print('file containing corpus path not found')
        sys.exit()
    pathList = []
    for path in pathData:
        pathList.append(path.rstrip('\n'))
    
    
    try:
        sw_file = open(StopWordFile,"r",encoding='utf-8')
        stop_word_lst = sw_file.readlines()
        stop_word_lst = stop_word_lst[0].split()
        sw_file.close()
    except:
        print('Stop word file not found')
        sys.exit()

    


    try:
        domainFile =open(DomainsFile,"r",encoding='utf-8')

        domainData = domainFile.readlines()
        domainFile.close()
    except:
        print('Domain List file not found')
        sys.exit()
    DomainList = []
    for domain in domainData:
        DomainList.append(domain.rstrip('\n'))




    Tags,Texts,Terms,TermList,CorpusLen = SplitTextfromTags(pathList,DomainList,stop_word_lst)
    flat_list = [item for sublist in TermList for item in sublist]
    CandidateTerms =list(set(flat_list))
    CandidateTerms.sort()

    CandidateTerms_dict = {}
    for i in CandidateTerms:
        CandidateTerms_dict[i] = CandidateTerms.index(i)


    NoOfCandidates = len(CandidateTerms)
    FinalData = np.zeros((NoOfCandidates,len(DomainList)+2))
    alpha = 0.8
    for term in CandidateTerms:
        ind = CandidateTerms_dict[term]
        NCI = CalculateNCI(term,Terms,CorpusLen)
    
        FinalData[ind][0] = NCI
    
    
        NDI_dict = CalCulateNDI(term,Terms,CorpusLen)
        for i in range(1,FinalData.shape[1] - 1):
            FinalData[ind][i] = NDI_dict[DomainList[i-1]]
        
    
    
        FinalData[ind,4] = (-1)*alpha*FinalData[ind,0] + (1-alpha)*FinalData[ind,1]/3 + (1-alpha)*FinalData[ind,2]/3 + (1-alpha)*FinalData[ind,3]/3
        RSA = FinalData[:,4]
        
    finalOutput = {}
    for domain in DomainList:
        finalOutput[domain] =[]
    
    for i in range(300):
        ind = np.argmax(RSA)
        domainArr = FinalData[ind,1:4]
        domainInd = np.argmax(domainArr)
        domain = DomainList[domainInd]
        finalOutput[domain].append(CandidateTerms[ind])
        
        #print(domain + ' :  ' +CandidateTerms[ind] )
    
        RSA[ind] = 0
    os.chdir(cur_wd)
    output = open('output.txt','w',encoding='utf-8')
    for key in finalOutput:
        #print('\n')
        #print('Key words in domain ', key ,'are : ')
        #print('****************************************')
        #print(finalOutput[key])
        
        
        output.write('\n')
        output.write('Domain terms for  ' + key + ' are : ')
        output.write('\n')
        output.write('****************************************')
        output.write('\n')
        output.write(str(' ,'.join(finalOutput[key])))
    output.close()
    print('Program output is available at ',cur_wd+'output.txt')
        
        
        #output.write(str(finalOutput[key]))
        


# In[24]:


#main('C:\\Users\\rahkhand\\CSE7401\\Project Final\\corpusPath.txt','C:\\Users\\rahkhand\\CSE7401\\Project Final\\hindi_stop_words.txt','C:\\Users\\rahkhand\\CSE7401\\Project Final\\Domains.txt')

if __name__ == "__main__":
   main()
