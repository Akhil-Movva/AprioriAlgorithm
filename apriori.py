from itertools import combinations

def read_transactions_from_file():
    file=open('basket_data.txt','r')
    data_set=file.readlines()
    file.close()
    
    transactions=[]
    for transaction in data_set:
        transactions.append(transaction.strip().split(" "))
    del transactions[0]
    
    #for transaction in transactions[0:5]:
        #print(transaction)

    return transactions

#Function to generate C1 itemsets
def generate_C1_itemsets():
    C1_itemsets=set()
    transactions=read_transactions_from_file()

    for transaction in transactions:
        for item in transaction:
            C1_itemsets.add(frozenset([item]))#storing each unique item as a frozenset as a set cannot have nested sets.

    return C1_itemsets

#function to generate (k-1) subsets for all itemsets belonging to C(k)
def generate_subsets(itemset):
    s=[]
    subsets=[]

    for i in range(1,len(itemset)):
        s.extend(combinations(itemset,i))
    for i in s:
        subsets.append(frozenset(i))

    return subsets   


#function to generate potentially large itemsets(candidate k-itemsets)
def apriori_gen(L_itemsets,k):
    candidate_itemsets=set()
     
     #This piece of code comprises the join step, where we join L(K-1) WITH L(k-1)
    for itemset1 in L_itemsets:
        for itemset2 in L_itemsets:
            if(len(itemset1.union(itemset2))==k):
                candidate_itemsets.add(itemset1.union(itemset2))

    #This piece of code comoprises the prune step, where we delete all itemsets c belonging to C(K) such that some (k-1)
    #subset of c is not in L(k-1)
    for itemset in candidate_itemsets:
        subsets=generate_subsets(itemset)
         
        flag=False
        for i in subsets:
            
            if(i not in L_itemsets):
                flag=True
                break
        if(flag):
            candidate_itemsets.remove(i)
              
    return candidate_itemsets

 



