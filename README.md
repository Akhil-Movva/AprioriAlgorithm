# Apriori Algorithm

## Assignment Description
This project implements the apriori algorithm from the paper:
> http://www.vldb.org/conf/1994/P487.PDF

## Motivation for the project
 Everytime after purchasing goods on Amazon, I notice the "frequently bought" section. I had always wondered how Amazon generates this section.
 In the "Introduction to Data science" course I got introduced to the concept of association rule learning and got to know how this helps in 
 producing recommmendations to the users. I became interested with the topic, and since then wanted to build the force that generates the associations
 between products.

 ## Problem
 The goal of the project is to generate association rules that have the desired minimum confidence specified by the user. The generated association
 rules are of the form, X-->Y, where X and Y are itemsets formed from the items stored in the database. We say that a rule X-->Y has confidence 'c' if
 c% of transactions in database that contain X also contain Y.

 ## Solution
 In this project, apriori algorithm is used to mine association rules from the transaction data. There are 2 steps involved in achieving
 this purpose, which are:
   
   1. Finding itemsests whose support is atleast minimum support, known as large itemsets. The support of an itemset is the number of transactions
      that contain it.
   2. Using these large itemsets to generate the rules. For every large itemset 'l', we generate all its non-empty subsets. Then for each subset 's',
      we check if support(l)/support(s) is atleast minimum confidence specified by the user and if it is, we add the rule 's-->(l-s)' to our
      set of association rules.

 ## Implementation
 The code consists of the following functions

  1. **read_transactions_from_file:** It generates a list of transactions from the text containing transaction data.
  2. **generate_C1_itemsets:** It generates C1 itemsets.
  3. **generate_subsets:**  This function is used to generate subsets for the prune step of the
    candidate generation function. It generates (k-1) subsets for all itemsets belonging to C(k).
  4. **apriori_gen:** This is the apriori candiate generation function that generates potentially large itemsets. This function comprises 2 steps, which are join
    and prune step. In the join step, we join L(K-1) with L(k-1). In the prune step, we delete all itemsets c belonging to C(K) such that some (k-1)
    subset of c is not in L(k-1)
  5. **generate_large_itemsets:** It is the function that generates the large itemsets, which are of interest to us.
  6. **generate_non_empty_subsets:** It is used generate non-empty subsets for each large itemset. It will be used in the process of generating association rules.
   
        ### Code flow
        The program takes minimum confidence and minimum support as input. The valid range of both the variables are between 0 and 1, and the program doesn't accept
        any value outside of the range for the variables. Once the valid inputs are given, the program proceeds to generating large itemsets and association rules.

        ### Working of the code
        We call the apriori function which takes the name of the file, minsupport and minconfidence arguments. Inside the function, we firstly genrate a list of 
        transactions by calling the 'read_transactions_from_file' function. Then we call the function, 'generate_C1_itemsets'. Now we use the C1 set to generate
        large  1-itemsets by calling the function, generate_large_itemsets.

        We use a while looop to generate potentially large itemsets and use them to generate large itemsets. This loop terminates when a certain L(K-1) set is empty. 
        As the large itemsets are generated, they are added to a dictionary, 'large_itemsets_set'.

        Once the large itemsets are generated, we calculate their support and print them out. Then, we generate association rules from the large item sets. Finally, we
        print the generated rules and their confidence to the screen.

  ## Dependencies
  For the project, **combinations** and **defaultdict** from itertools and collections module respectively are the dependencies. Itertools and collections can be imported
  directly. There is no need for any installation.

  ## Instructions to run the code
  After changing the directory to the project's directory, enter:

  > `python apriori.py`

  ## Results
  Below is the link to the text file containing output produced when the minimum support and minimum confidence values supplied are 0.01 and 0.2 respectively.

  [View output](output.txt)   

         
  ## References
  1. https://github.com/stedy/Machine-Learning-with-R-datasets/blob/master/groceries.csv(dataset)
  2. http://www.vldb.org/conf/1994/P487.PDF
  3. https://github.com/asaini/Apriori






 
