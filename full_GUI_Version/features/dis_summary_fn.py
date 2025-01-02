#import tkinter.messagebox to be used inside display_summary function.
import tkinter.messagebox as mbox 

# Define the display summary of transactions function.
def display_summary(transactions):
    # Check if there are transactions available.
    if transactions:
        # Initialize variables to store total income, total expense, total balance, total transaction count, and total individual category transaction count.
        total_income = 0
        total_expense = 0
        tot_transaction_count=0
        all_category_tran_count=[]

        # Display the summary.
        print("\nSummary of Transactions:")
        

        # Iterate through each transaction category.
        for category, entries in transactions.items():
            # Calculate the total number of transactions in the category.
            tot_no_transactions = len(entries)
            
            # Initialize variables to store total income and total expense for the category.
            #Using for loop to iterate over each transaction checking the transaction type and add to the relevant transaction type total.
            category_income = sum(entry["amount"] for entry in entries if entry["t_type"] == "Income")
            category_expense = sum(entry["amount"] for entry in entries if entry["t_type"] == "Expense")
            
            # Update total income and total expense with category totals.
            total_income += category_income
            total_expense += category_expense


            # Display each category summary.
            print(f"\nCategory: {category}")
            print(f"Total Number of Transactions: {tot_no_transactions}")

            #Appending all the total individual category transaction count to a list variable called "all_category_tran_count".
            all_category_tran_count.append(f"Category: {category}\nTotal Number of Transactions: {tot_no_transactions}\n")
            # Calculating the total transaction count for all transactions.
            tot_transaction_count += tot_no_transactions

        # Calculate the total balance.
        total_balance = total_income - total_expense

        #Creating a string/ text that combines all the information about the individual transaction count of each category.
        summary_all_category="\n".join(all_category_tran_count)
        
        # Display the total summary.
        print("\nOverall Summary:")
        print(f"Total number of transactions:{tot_transaction_count}")
        print(f"Total Income: ${total_income:.2f}")
        print(f"Total Expense: ${total_expense:.2f}")
        print(f"Total Balance: ${total_balance:.2f}")
        #creating a text to be passed to text widget of tkinter to display the overall summary of transactions.
        summary =(f"{summary_all_category}\nOverall Summary:\nTotal number of transactions:{tot_transaction_count}\nTotal Income: ${total_income:.2f}\nTotal Expense: ${total_expense:.2f}\nTotal Balance: ${total_balance:.2f}") 

    else:
        # Display error message if no transactions available.
        mbox.showerror("Display summary","No transactions stored yet. Try again after inserting transactions.") # GUI message to be displayed to user.
        print("\nNo transactions stored yet. Try again after inserting transactions.")
        summary = "No transactions stored yet. Try again after inserting transactions."
    return summary # returning the text variable to the main program.
