#Define the view transactions function.
def view_transactions(transactions):
    #check if transactions available or not
    if transactions:
        #intialize count to keep track of transaction number.
        count=0

        #Loop through each category and transaction data in transactions.
        for category, category_transactions in transactions.items():
            #Display the category type before showing the transactions stored in it.
            print()
            print(f"Category: {category} ->")
            count = 0 # Resets count for when each category start.

            #Displays each transaction one by one.
            for transaction in category_transactions:
                count += 1
                # using f-string formating with designators to bring a refined visual output to the user.
                print(f"Transaction{count}=  Serial_no: {transaction['serial_no']:^5}--Amount: ${transaction['amount']:^10,.1f} -- Type: {transaction['t_type']:^10} -- Date: {transaction['date']:^12}")
    else:
        # Display error message indicating no transactions available.
        print("\nNo transactions stored yet, try again after inserting transactions.")

