# Define the display summary of transactions function.
def display_summary(transactions):
    # Check if there are transactions available.
    if transactions:
        # Initialize variables to store total income, total expense, total number of transactions, and total balance.
        total_income = 0
        total_expense = 0
        tot_trans_count=0

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
            
            # Calculating the total transaction count for all transactions.
            tot_trans_count += tot_no_transactions

        # Calculate the total balance.
        total_balance = total_income - total_expense
        
        # Display the total summary.
        print("\nOverall Summary:")
        print(f"Total number of transactions:{tot_trans_count}")
        print(f"Total Income: ${total_income:.2f}")
        print(f"Total Expense: ${total_expense:.2f}")
        print(f"Total Balance: ${total_balance:.2f}")
    else:
        # Display error message if no transactions available.
        print("\nNo transactions stored yet. Try again after inserting transactions.")
