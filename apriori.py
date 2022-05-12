from itertools import combinations
from collections import defaultdict

def read_transactions_from_file():
    file=open('groceries.txt','r')
    data_set=file.readlines()
    file.close()
    
    transactions=[]
    for transaction in data_set:
        transactions.append(frozenset(transaction.strip().split(",")))
    del transactions[0]
    
    #for transaction in transactions[0:5]:
        #print(transaction)

    return transactions

#Function to generate C1 itemsets
def generate_C1_itemsets(transactions):
    C1_itemsets=set()

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
            if len(itemset1.union(itemset2))==k:
                candidate_itemsets.add(itemset1.union(itemset2))

    #This piece of code comoprises the prune step, where we delete all itemsets c belonging to C(K) such that some (k-1)
    #subset of c is not in L(k-1)
    
    for itemset in candidate_itemsets.copy():
        subsets=generate_subsets(itemset)
         
        flag=False
        for i in subsets:
            if i not in L_itemsets:
                flag=True
                break
        if flag:
            candidate_itemsets.remove(itemset)
              
    return candidate_itemsets

#function to generate large itemsets
def generate_large_itemsets(C_itemsets,transactions,minsup,itemset_number):
    large_itemsets=set()
    itemset_count=defaultdict(int)

    #incrementing the count of the itemset if it is found to be part of the current transaction
    for itemset in C_itemsets:
        for transaction in transactions:
           if itemset.issubset(transaction):
                itemset_count[itemset]=itemset_count[itemset]+1
                itemset_number[itemset]=itemset_number[itemset]+1

    #adding the itemset to the set of large itemsets if its count is greater than or equal to minimum support
    for itemset in itemset_count:
        support=float(itemset_count[itemset])/len(transactions) 
        if support>= minsup:
            large_itemsets.add(itemset)
                   
    #print(large_itemsets)
    return large_itemsets

def generate_non_empty_subsets(itemset):
    subsets=[]

    for i,a in enumerate(itemset):
        subsets.extend(combinations(itemset,i+1))
    return subsets    

def apriori(minsup,minconf):
    transactions=read_transactions_from_file()
    #print(transactions[1:5])

    large_itemsets_set={}
    itemset_number=defaultdict(int)
    
    C_itemsets=generate_C1_itemsets(transactions)
    L_itemsets=generate_large_itemsets(C_itemsets,transactions,minsup,itemset_number)
    #print(L_itemsets)

    k=2
    while L_itemsets!=set([]):
        large_itemsets_set[k-1]=L_itemsets
        C_itemsets=apriori_gen(L_itemsets,k)
        L_itemsets=generate_large_itemsets(C_itemsets,transactions,minsup,itemset_number)
        k+=1
    #print(large_itemsets_set)
    
    large_itemsets_support={}
    for itemsets in large_itemsets_set:
        for itemset in large_itemsets_set[itemsets]:
           large_itemsets_support[itemset]=float(itemset_number[itemset])/len(transactions)


    association_rules_confidence={}
    for k,itemsets in list(large_itemsets_set.items())[1:]:
        for itemset in itemsets:
            subsets=map(frozenset, [x for x in generate_non_empty_subsets(itemset)])
            for a in subsets:
                set_without_a=itemset.difference(a)
                if len(set_without_a)>0:
                    support_l=float(itemset_number[itemset])/len(transactions)
                    support_a=float(itemset_number[a])/len(transactions)
                    confidence=support_l/support_a
                    if confidence>=minconf:
                        association_rules_confidence[(a,set_without_a)]=confidence

    print("The large itemsets are")
    for itemset in large_itemsets_support:
        print("itemset: %s support: %.4f\n" % (itemset,large_itemsets_support[itemset]))


apriori(0.05,0.6)
 
      



    
     





