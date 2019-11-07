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


def hash(text, M = 2**32 - 1) :
    
    xlength = len(text)
    sum = 0
    
    for i in range(xlength) :
        sum += ord(text[i])
        
    return ( sum % M)
    
def hash_with_binascii(text) :
    hash = binascii.crc32(text.encode())
    return hash 

def k_shingles(document, k):
    
    shingles = OrderedSet()
    shings = OrderedSet()
    
    for i in range(len(document) - k + 1 ):
        temp_shingle = document[ i:(i + k ) ]
        shingles.add(hash(temp_shingle))
        shings.add(temp_shingle)
        
    return shingles, shings

def universal_set(documents, k) :
    
    universal = OrderedSet()
    universal1 = OrderedSet()
    for doc in documents :
        #print("doc = ", doc)
        shingles, shings = k_shingles(doc, k)
        universal = universal.union(shingles)
        universal1 = universal1.union(shings)
    
    universal = list(universal)
    universal1 = list(universal1)
    universal.sort()
    universal1.sort()
    universal = OrderedSet(universal)
    universal1 = OrderedSet(universal1)
    
    return universal, universal1
    
def matrix_set(documents, k) :
    universal, universal1 = universal_set(documents, k)
    matrices = []
    
    for doc in documents :
        matrixSet = np.zeros(len(universal))
        shingles, shings = k_shingles(doc, k)
        for s in shingles :
            indx = universal.index(s)
            matrixSet[indx] = 1
            
        matrices.append(matrixSet.tolist())
    
    return np.array(np.transpose(matrices))

def CompareSets(setA, setB) :
    A = setA.intersection(setB)
    B = setA.union(setB)
    
    return (len(A)/len(B))
  
  
def compareByJaccard(documents,k,index1 = 10, index2 = 11 ) :
    
    allDocs = [] 
    for doc in documents :
        shingles, shings = k_shingles(doc, k)
        allDocs.append(shingles)

    
    return CompareSets(allDocs[index1] , allDocs[index2])
 
def generate_coefficient_list(number_of_coefficients):
    max = 2**32 - 1
    next_prime = 4294967311
    coeffs = []
    
    def random_int():
        return random.randint(1, max)
    
    for _ in range(number_of_coefficients):
        temp = random_int()
        while temp in coeffs:
            temp = random_int()
        coeffs.append(temp)
    
    return coeffs
    

def generateMinHashFunctions(M, Snumb):
    #np.random.seed()
    #np.random.permutation(10)
    """
    h(row_i)=(a*row_i + b) mod c
    """
    hashes = [] 
    k = np.arange(1,M)
    # coeff_a = np.random.permutation(k)
    # coeff_b = np.random.permutation(k)
    # print("M = ", M)
    # print("Snumb = ",Snumb )
    coeffs_a = generate_coefficient_list(Snumb)
    coeffs_b = generate_coefficient_list(Snumb)

    row = np.arange(M)
    c = sympy.nextprime(M+1)
    
    for i in range(Snumb):
        hash_i = ( (coeffs_a[i]*row + coeffs_b[i]) % c ) % M
        #hash_i = ( (coeff_a[i]*row + coeff_b[i]) % c )
        #hash_i = ((a * row + b) % c) % M
        hashes.append(hash_i.tolist())
    
    #print("hashes = ", hashes)
    return hashes

def MinHashing(documents,k,Snumb = 100):
    characteristic_mat = matrix_set(documents, k)
    M, nDocs = np.shape(characteristic_mat)
    hashes = generateMinHashFunctions(M, Snumb)
    signature = np.ones((Snumb, nDocs)) * np.inf
    
    for row_r in range(M) :
        for col_c in range(nDocs) :
            if characteristic_mat[row_r,col_c] == 1 :
                for i, h_i in enumerate(hashes) :
                     signature[i,col_c]  = min(h_i[row_r],  signature[i,col_c])

    
    return signature
    
 
def jaccard_sim_minhashing(signature, index1, index2) :
    signature = np.array(signature)
    A = signature[:,index1].tolist()
    B = signature[:,index2].tolist()
    
    total = len(A)
    commun = 0 
    for i in range(len(A)) :
        if A[i] == B[i] :
            commun += 1
    
    return (commun/total)
    
    
def read_data():
    f = open('dataDuplicates.json')
    filen = json.load(f)
    dataset = filen['texts']
    return dataset
 
    
def similar_docs(k = 5, untilInd = 50) :
    
    data = read_data()
    documents = data[0:untilInd]
    s = 0.6
    signature = MinHashing(documents, k)
    indices = []
    total = len(documents)
    for i in range(total) :
        for j in range(i, total) :
            sim = jaccard_sim_minhashing(signature, i,j)
            if sim > s and (i != j) :
                indices.append([i,j])

    print("similar docs : ",indices )
