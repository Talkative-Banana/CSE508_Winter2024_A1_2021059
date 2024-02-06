import os
import string
import pickle
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import nltk
nltk.download('stopwords')
nltk.download('punkt')

def Preprocessing(file, k):
    # Lowering the letters
    a = file.lower()
    if(k == 1):
        print("\n------------------After Lowering Process-----------------\n")
        print(a)
        print()
    
    # Breaking in Tokens
    tokens = word_tokenize(a)
    if(k == 1):
        print("\n------------------After Tokenization-----------------\n")
        print(tokens)
        print ()

    stop_words = set(stopwords.words('english'))

    # Removing stop_words
    tokens = [token for token in tokens if token not in stop_words]
    if(k == 1):
        print("\n------------------After Removing stop_words-----------------\n")
        print(tokens)
        print()

    # Removing punctuations
    tokens = [token for token in tokens if token not in string.punctuation]
    if(k == 1):
        print("\n------------------After Removing punctuations-----------------\n")
        print(tokens)
        print()
    
    # Removing blank space tokens
    tokens = [token for token in tokens if token.strip()]
    if(k == 1):
        print("\n------------------After Removing Blank Space Tokens-----------------\n")
        print(tokens)
        print()

    return tokens

# Preprocessing and Storing the results
def PreProcess():
    for i in range(1, 1000):
        a = f"file{i}.txt"
        f = open(f"./text_files/{a}", "r").read()
        res = Preprocessing(f, (i <= 5))
        if i <= 5:
            print(f"\n[Test Case {i}]")
            print("------------------Before Preprocessing-----------------\n")
            print(f)
            print("\n------------------After Preprocessing------------------\n")
            print(res)
        
        filehandler = open(f"./Processed_result/file{i}.obj","wb")
        pickle.dump(res, filehandler)
        filehandler.close()

def InvertedIndex():
    table = {}
    # Reading Preprocessed results
    for doc in range(1, 1000):
        file = open(f"./Processed_result/file{doc}.obj", 'rb')
        object_file = pickle.load(file)
        for word in object_file:
            if word in table:
                if (table[word][-1] == doc):
                    continue
                else:
                    table[word].append(doc)
            else:
                table[word] = [doc]
        
        file.close()
    
    # Dumping inverted index
    filehandler = open(f"inverted_index.obj","wb")
    pickle.dump(table, filehandler)
    filehandler.close()

def PositionalIndex():
    table = {}
    # Reading Preprocessed results
    for doc in range(1, 1000):
        file = open(f"./Processed_result/file{doc}.obj", 'rb')
        object_file = pickle.load(file)
        for idx in range(len(object_file)):
            word = object_file[idx]
            if word in table:
                if(table[word][-1][0] == doc):
                    table[word][-1][1].append(idx)
                else:
                    table[word].append([doc, [idx]])
            else:
                temp = [doc, [idx]]
                table[word] = [temp]
        file.close()
    
    # Dumping positional index
    filehandler = open(f"positional_index.obj","wb")
    pickle.dump(table, filehandler)
    filehandler.close()

def helper(token, table):
    if token not in table:
        return []
    return table[token]

def NOT(docs1):
    res = []
    i = 1
    idx = 0
    while ((idx < len(docs1)) and (i < 1000)):
        if(i == docs1[idx]):      
            i += 1
        elif(i < docs1[idx]):
            res.append(i)
            i += 1
        elif(i > docs1[idx]):
            idx += 1
    
    while(i < 1000):
        res.append(i)
        i += 1
    
    return res

def AND(docs1, docs2):
    res = []
    i, j = 0, 0
    while(i < len(docs1) and j < len(docs2)):
        if(docs1[i] == docs2[j]):
            res.append(docs1[i])
            i += 1
            j += 1
        elif(docs1[i] < docs2[j]):
            i += 1
        else:
            j += 1  
    
    return res

def OR(docs1, docs2):
    res = []
    i, j = 0, 0
    while(i < len(docs1) and j < len(docs2)):
        if(docs1[i] == docs2[j]):
            res.append(docs1[i])
            i += 1
            j += 1
        elif(docs1[i] < docs2[j]):
            res.append(docs1[i])
            i += 1
        else:
            res.append(docs2[j])
            j += 1  

    while(i < len(docs1)):
        res.append(docs1[i])
        i += 1

    while(j < len(docs2)):
        res.append(docs2[j])
        j += 1

    return res

def ANDNOT(docs1, docs2):
    return AND(docs1, NOT(docs2))

def ORNOT(docs1, docs2):
    return OR(docs1, NOT(docs2))

def Query(InputSeq, ops, table):
    tokens = Preprocessing(InputSeq, 0)
    X = ""
    for i in range(len(ops)):
        X += tokens[i] + " " + ops[i] + " "
    X += tokens[-1]
    last = helper(tokens[0], table)
    itr = 1
    for op in ops:
        if (op == "AND"):
            op1 = last
            op2 = helper(tokens[itr], table)
            last = AND(op1, op2)
        elif (op == "OR"):
            op1 = last
            op2 = helper(tokens[itr], table)
            last = OR(op1, op2)
        elif (op == "AND NOT"):
            op1 = last
            op2 = helper(tokens[itr], table)
            last = ANDNOT(op1, op2)
        elif (op == "OR NOT"):
            op1 = last
            op2 = helper(tokens[itr], table)
            last = ORNOT(op1, op2)
        
        itr += 1

    return X, last

def Common(tkn1, tkn2):
    i, j = 0, 0
    res = []
    while((i < len(tkn1)) and (j < len(tkn2))):
        if(tkn1[i][0] == tkn2[j][0]):
            p, q = 0, 0
            while (p < len(tkn1[i][1]) and q < len(tkn2[j][1])):
                if(1 + tkn1[i][1][p] == tkn2[j][1][q]):
                    res.append(tkn1[i][0])
                    p += 1
                    q += 1
                elif (tkn1[i][1][p] < 1 + tkn2[j][1][q]):
                    p += 1
                else:
                    q += 1
            i += 1
            j += 1
        elif (tkn1[i][0] < tkn2[j][0]):
            i += 1
        else:
            j += 1
    
    return res

def Query(PhraseQue, table):
    tokens = Preprocessing(PhraseQue, 0)
    # All the Docs containing all the tokens of the PhraseQue
    res = [i for i in range(1, 1000)]
    # tokens empty
    if(len(tokens) == 0): return []
    # Docs containing tokens[0]
    if(len(tokens) == 1):
        return [key[0] for key in helper(tokens[0], table)]
    
    tkn1 = helper(tokens[0], table)
    for idx in range(1, len(tokens)):
        tkn2 = helper(tokens[idx], table)
        res = AND(res, Common(tkn1, tkn2))
        tkn1 = tkn2

    return res

def Output(lst):
    out = ""
    for doc in lst:
        out += "file" + str(doc) + ".txt, "
    return out[:-2]

def Boolean(table):
    N = int(input("\nEnter N: "))
    for query in range(N):
        InputSeq = input("Enter Input Seq: ")
        ops = input("Enter Operations: ").split(',')
        for op in range(len(ops)):
            ops[op] = ops[op].lstrip().rstrip()
        X, docs = Query(InputSeq, ops, table)
        print(f"Query {query + 1}: " + X)
        print(f"Number of documents retrieved for query {query}: {len(docs)}")
        print(f"Names of the documents retrieved for query {query}: {Output(docs)}")

def Phrase(table):
    N = int(input("\nEnter N: "))
    for query in range(N):
        InputSeq = input("Enter Phrase Query: ")
        docs = Query(InputSeq, table)
        print(f"Number of documents retrieved for query {query + 1} using positional index: {len(docs)}")
        print(f"Names of documents retrieved for query {query + 1} using positional index: {Output(docs)}")

def setup():
    # Preprocessing
    PreProcess()
    # Constructing and Saving Inverted Index
    InvertedIndex()
    #Constructing and Saving Positional Index
    PositionalIndex()
    # Loading Inverted Index table
    filehandler = open(f"inverted_index.obj","rb")
    table1 = pickle.load(filehandler)
    filehandler.close()
    # Loading Positional Index table
    filehandler = open(f"positional_index.obj","rb")
    table2 = pickle.load(filehandler)
    filehandler.close()
    return table1, table2

def main():
    table1, table2 = setup()
    while(1):
        print('''
Select Option:
1) Unigram Inverted Index and Boolean Queries
2) Positional Index and Phrase Queries
3) Exit''')
        opt = int(input())
        if(opt == 1):
            Boolean(table1)
        elif(opt == 2):
            Phrase(table2)
        elif(opt == 3):
            print("[x] Exiting")
            break
        else:
            print("Invalid Input\n")
        
if __name__ == "__main__": main()