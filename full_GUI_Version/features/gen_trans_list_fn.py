#import tkinter.messagebox to be used inside gen_transaction_list function.
import tkinter.messagebox as mbox

#Define the gen_transaction_list function.
def gen_transaction_list(transactions):
    #initialize an empty list to store all the transaction converted from dictionary to list.
    transactions_list=[]
    #check if transactions available.
    if transactions:
        #Loop through each category and transaction data in transactions.
        for category, category_transactions in transactions.items():
            #Goes through  each transaction in a category one by one.
            for transaction in category_transactions:
                #create a list to store every transaction stored in the dictionary "transactions".
                trans_list=[category,transaction['serial_no'],transaction['amount'],transaction['t_type'],transaction['date']]
                #Append the transaction list to the transactions_list.
                transactions_list.append(trans_list)
    else:
        # Display an error message indicating no transactions available.
        mbox.showerror("View transactions in Table","No transactions stored yet, Therefore, the transaction table would be empty.")
        print("No transactions stored yet, try again after inserting transactions.")
    return transactions_list #Return the transactions_list.