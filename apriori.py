from itertools import combinations
from collections import defaultdict

def read_transactions_from_file(filename):
    file=open(filename,'r')
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

    #This piece of code comprises the prune step, where we delete all itemsets c belonging to C(K) such that some (k-1)
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

#function to generate non-empty subsets for each large itemset. It will be used in the process of generating association rules
def generate_non_empty_subsets(itemset):
    subsets=[]

    for i,a in enumerate(itemset):
        subsets.extend(combinations(itemset,i+1))
    return subsets    

#This is the implementation of the apriori algorithm that generates large itemsets and association rules
def apriori(filename,minsup,minconf):
    transactions=read_transactions_from_file(filename)
    #print(transactions[1:5])

    large_itemsets_set={}#dictionary that is used to store large itemsets as they are generated
    itemset_number=defaultdict(int)#dictionary to store itemsets and their counts
    
    C_itemsets=generate_C1_itemsets(transactions)#generating candidate 1-itemsets
    L_itemsets=generate_large_itemsets(C_itemsets,transactions,minsup,itemset_number)#generating large 1-itemsets
    #print(L_itemsets)

    k=2

    #running the loop until a certain L(K-1) produced has no elements
    while L_itemsets!=set([]):
        large_itemsets_set[k-1]=L_itemsets
        C_itemsets=apriori_gen(L_itemsets,k)#calling apriori_gen to produce potentially large itemsets
        L_itemsets=generate_large_itemsets(C_itemsets,transactions,minsup,itemset_number)#generating large itemsets
        k+=1
    #print(large_itemsets_set)
    
    large_itemsets_support={}#dictionary to store large itemsets and their corresponding support
    #determining support for each large itemset
    for itemsets in large_itemsets_set:
        for itemset in large_itemsets_set[itemsets]:
           large_itemsets_support[itemset]=float(itemset_number[itemset])/len(transactions)

    
    association_rules_confidence={}#dictionary to store association rules and their corresponding confidence
    #generating association rules and determing their corresponding confidence
    #for k,itemsets in list(large_itemsets_set.items())[1:]:
    for k in large_itemsets_set:
        if k!=1:
            for itemset in large_itemsets_set[k]:
            #generating non-empty subsets for each large itemset
                subsets=[]
                s=generate_non_empty_subsets(itemset)
                for subset in s:
                    subsets.append(frozenset(subset))
                for a in subsets:
                    set_without_a=itemset.difference(a) #generating l-a for each subset a
                    if len(set_without_a)>0:
                        support_l=float(itemset_number[itemset])/len(transactions)
                        support_a=float(itemset_number[a])/len(transactions)
                        confidence=support_l/support_a
                        if confidence>=minconf:
                            association_rules_confidence[(a,set_without_a)]=confidence

    #printing each large itemset and its support
    print("The large itemsets are:\n")
    for itemset in large_itemsets_support:
        print("%s support: %.4f\n" % (str(itemset),large_itemsets_support[itemset]))

    #printing each association rule and its confidence
    print("The association rules are:\n")
    for rule in association_rules_confidence:
        (antecedent,consequent)=rule
        print("%s --> %s confidence: %.4f\n"% (str(antecedent),str(consequent),association_rules_confidence[rule]))

while True:
    msup=float(input("Enter the desired minimum support\n"))
    if not (msup > 0 and msup <=1):
        print("please enter valid minimum support\n")
        continue
    else:
        break     

while True:
    mconf=float(input("Enter the desired minimum confidence\n"))
    if not (mconf > 0 and mconf<=1):
        print("please enter valid minimum confidence\n")
        continue
    else:
        break
     
apriori("groceries.txt",msup,mconf)

      



    
     





