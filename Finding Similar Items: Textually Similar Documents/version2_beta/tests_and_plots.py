#pip install ordered-set
import sympy
import random
import numpy as np
import binascii
import json
from ordered_set import OrderedSet
import matplotlib.pyplot as plt
import time
from sklearn.metrics import accuracy_score
from similarItems import *

def MinHashing_test(Snumb = 2):
    characteristic_mat = np.array([[1. ,0., 0., 1.],[0., 0., 1., 0.],[0., 1., 0., 1.],[1., 0., 1. ,1.],[0. ,0., 1., 0.]])
    M, nDocs = np.shape(characteristic_mat)
    hashes = [[1, 2, 3, 4, 0], [1, 4, 2, 0, 3]]
    signature = np.ones((Snumb, nDocs)) * np.inf
    
    for row_r in range(M) :
        for col_c in range(nDocs) :
            if characteristic_mat[row_r,col_c] == 1 :
                for i, h_i in enumerate(hashes) :
                     signature[i,col_c]  = min(h_i[row_r],  signature[i,col_c])

    return signature 
    
def test_time_hashing(k = 5, untilInd = 20) :
    data = read_data()
    documents = data[0:untilInd]
    s = 0.6
    signature = MinHashing(documents, k)
    
def similar_docs_accaracy(k = 5, untilInd = 50) :
    data = read_data()
    documents = data[0:untilInd]
    s = 0.8
    signature = MinHashing(documents,k, )
    indices = []
    indices_true = []
    total = len(documents)
    for i in range(total) :
        for j in range(i, total) :
            sim = jaccard_sim_minhashing(signature, i,j)
            if sim > s and (i != j) :
                indices.append([i,j])
            sim = compareByJaccard(documents,k,index1 = i, index2 = j )
            if sim > s and (i != j) :
                indices_true.append([i,j])
    print("indices : ",indices)
    print("indices_true : ",indices_true)   
    a = [sum(x) for x in indices ]   
    b = [sum(x) for x in indices_true ]   
    
    count = 0
    for element in b :
        if element in a :
            count += 1

    return (count / max(len(a),len(b) ) ) 
    
    
def similar_docs_accaracy_hashes(nHash = 20, k = 5, untilInd = 50) :
    data = read_data()
    documents = data[0:untilInd]
    s = 0.8
    signature = MinHashing(documents,k, nHash)
    indices = []
    indices_true = []
    total = len(documents)
    for i in range(total) :
        for j in range(i, total) :
            sim = jaccard_sim_minhashing(signature, i,j)
            if sim > s and (i != j) :
                indices.append([i,j])
            sim = compareByJaccard(documents,k,index1 = i, index2 = j )
            if sim > s and (i != j) :
                indices_true.append([i,j])
    print("indices : ",indices)
    print("indices_true : ",indices_true)   
    a = [sum(x) for x in indices ]   
    b = [sum(x) for x in indices_true ]   
    
    count = 0
    for element in b :
        if element in a :
            count += 1

    return (count / max(len(a),len(b) ) ) 
      
def tests() :
    
    s1 = 'ad'
    s2 = 'c'
    s3 = 'bde'
    s4 = 'acd'
    
    
        
    documents = [s1,s2,s3,s4]
    print(hash(s4))
    print()
    
    k = 1
    s1_shingles = k_shingles(s1, k)
    s2_shingles = k_shingles(s2, k)
    s3_shingles = k_shingles(s3, k)
    s4_shingles = k_shingles(s4, k)
    print()
    print("s1_shingles = ", s1_shingles)
    print("s2_shingles = ", s2_shingles)
    print("s3_shingles = ", s3_shingles)
    print("s4_shingles = ", s4_shingles)
    print()
    print(universal_set(documents,k))
    print()
    print(matrix_set(documents,k))
    print("Fictive permutation")
    print(generateMinHashFunctions(M=10, Snumb = 4))
    print()
    print("---------------------------------------")
    
    print(MinHashing_test())
    print("---------------------------------------")
    signature = MinHashing_test() 
    print("similarity : ", jaccard_sim_minhashing(signature, 0,3))
    print("*****************---------------******************")
    signature = MinHashing(documents,k)
    print("signature = ")
    print(signature)
    print("similarity Alldocs: ", jaccard_sim_minhashing(signature, 0,3))

def testsDocs() :
    data = read_data()
    documents = data[0:40]
    k = 5
    s = 0.6
    signature = MinHashing(documents,k)
    indices = []
    indices_true = []
    total = len(documents)
    for i in range(total) :
        for j in range(i, total) :
            sim = jaccard_sim_minhashing(signature, i,j)
            if sim > s and (i != j) :
                indices.append([i,j])
            sim = compareByJaccard(documents,k,index1 = i, index2 = j )
            if sim > 0.5 and (i != j) :
                indices_true.append([i,j])
    print("dataset")
    print(documents)
    print("signature = ")
    print(signature)
    docA = 16
    docB = 17
    print("docA : ", documents[docA])
    print("docB : ", documents[docB])
    print("similarity docA and docB : ", jaccard_sim_minhashing(signature, docA,docB))
    print()
    print(compareByJaccard(documents,k,index1 = docA, index2 = docB ) )
    print("similar docs : ",indices )
    print("similar docs true : ", indices_true )

def test1() :
    
    documents = ["la vie est belle mon amie", "la vida es muy bonita mi amiga", "la vie est bella mon amir",  "hfjfds fjjfds dkf", "vida vie amigo amiga to ", "why to do this hehe hehe", "vida es muy bonita min amigo"]
    k = 5
    s = 0.8
    signature = MinHashing(documents,k)
    indices = []
    indices_true = []
    total = len(documents)
    for i in range(total) :
        for j in range(i, total) :
            sim = jaccard_sim_minhashing(signature, i,j)
            if sim > s and (i != j) :
                indices.append([i,j])
            sim = compareByJaccard(documents,k,index1 = i, index2 = j )
            if sim > 0.5 and (i != j) :
                indices_true.append([i,j])
    print("dataset")
    print(documents)
    print("signature = ")
    print(signature)
    docA = 1
    docB = 6
    print("docA : ", documents[docA])
    print("docB : ", documents[docB])
    print("similarity docA and docB : ", jaccard_sim_minhashing(signature, docA,docB))
    print()
    print(compareByJaccard(documents,k,index1 = docA, index2 = docB ) )
    print("similar docs : ",indices )
    print("similar docs true : ", indices_true )
 
 
def plot_execution_time(temps = 10) :
    
    index = []
    s = 1
    timers = []
    for i in range(temps):
        start = time.time()
        test_time_hashing(k = 5, untilInd = s)
        elapsed =  time.time() - start
        s = 2*s
        timers.append(elapsed)
        index.append(s)
    
    plt.xlabel('Problem size')
    plt.ylabel('Execution time')
    plt.plot(index, timers, 'r-o')
    plt.show()
  
def test_shingle_size_accuracy() :
    
    size = np.arange(1,9)
    accuracies = []
    for k in size :
        acc = similar_docs_accaracy(k, untilInd = 50) * 100
        accuracies.append(acc)
    
    plt.xlabel('Shingle size')
    plt.ylabel('Accuracy')
    plt.plot(size, accuracies, 'r-o')
    plt.show()
  
#TODO test for scalability execution vs size of dataset 
#TODO  test and graph the effect of k (shingles) && [[s (threeshold)]] && #hashes for the accruacy, 
def test_NumberOfHashesFunc_accuracy() :
    
    size = np.linspace(10,100 , 10).tolist()
    size = [ int(x) for x in size ]

    accuracies = []
    for numbHash in size :
        acc =  similar_docs_accaracy_hashes(nHash = numbHash, k = 5, untilInd = 50) * 100
        accuracies.append(acc)
    
    plt.xlabel('Number of hash functions')
    plt.ylabel('Accuracy')
    plt.plot(size, accuracies, 'r-o')
    plt.show()
   
plot_execution_time(temps = 2)

