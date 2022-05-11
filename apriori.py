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
    

print(len(generate_C1_itemsets()))   
 
