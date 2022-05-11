def read_data_from_file():
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

    
    
 
