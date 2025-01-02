# Import neccessary python libraries for the use of the update_transaction function.
from datetime import datetime
from features.view_fn import view_transactions

# Define the update_transaction function.
def update_transaction(transactions):
    # Display the transactions by calling view_transactions function.
    view_transactions(transactions)

    # Check if transactions available or not before proceeding.
    if transactions:
        # Get the serial No. of the transaction to be updated from the user.
        serial_v = input("Enter the Serial No. of the transaction to update: ")

        # Initialize that the transaction is not found at the begining of the search.
        transaction_found = False

        # Iterate through each category and its transactions to search for the serial number.
        for entries in transactions.values():
            for entry in entries:
                #Check if the entry serial number matches with the users input.
                if entry["serial_no"] == serial_v:
                    # Change the value of transaction_found variable to true to state that transaction is found,and this will be used to break the loop.
                    transaction_found = True
                    print("Transaction found!")
                    
                    # getting the amount from the user and checking if it is valid.
                    try:
                        amount = float(input("Enter the amount (eg: 45062): "))
                                
                    except ValueError:
                        #Display proper error message to user if the amount value entered in invalid.
                        print("\nPlease enter a valid values that are numerical ")
                        print("your attempt for recording the previous transactions was discarded")

                    else:

                        # Check if the amount is non-negative.
                        if amount<=0:
                            # Display proper error message if amount is negative.
                            print("\nTransaction cannot have negative values, therefore the transaction update was discarded")
                        else:
                            # Get the transaction type from the user.
                            transaction_type = str(input("Enter the type 'I'(Income)/'E'(Expense): ")).capitalize()
                            # Get the transaction date from the user.
                            date=str(input("Enter the date of transaction(YYYY-MM-DD): "))
                            
                            #Validate the date format.
                            try:
                                # Checking if value the inputed is a valid date.
                                datetime.strptime(date, '%Y-%m-%d')

                            except ValueError:
                                #Display proper error message if date entered is invalid and assigning current date as date.
                                print("\nInvalid date format. Please use YYYY-MM-DD next time.\nThe date for the current transaction been entered is set to the current date!")

                                # Get the current date and time.
                                current_datetime = datetime.now()
                                # Extract the date part only.
                                current_date = current_datetime.date()
                                # If you want to format the date as a string in a specific format.
                                formatted_date = current_date.strftime("%Y-%m-%d")
                                #assigning the formated date as the date of the transaction.
                                date = formatted_date

                            # updating the transaction only if the transaction type falls into the category of either Income or Expense.
                            if ((transaction_type.startswith("I") or transaction_type.startswith("E")) and transaction_type !=""):

                                # setting type transaction_type string value to either Income or Expense if the user gives a incomplete input.
                                if transaction_type.startswith("I"):
                                    transaction_type="Income"
                                else:
                                    transaction_type="Expense"

                                # Update the values in the dictionary.
                                entry["amount"] = amount
                                entry["t_type"] = transaction_type
                                entry["date"] = date

                                print("\nTransaction updated successfully!")
                                break  # Exit the loop once the transaction is updated.
                            else:
                                # Display transaction prevented from being updated message to user.
                                print("\nSorry your update cannot be executed unless you specify whether transaction is either a Income or an Expense.!")
            if transaction_found:
                break  # Exit the outer loop once the transaction is found and updated.

        if not transaction_found:
            # Display Error message if transaction for the serial number given is not found.
            print("\nTransaction with the given serial number is not found.")
    else:
        # Give the appropriate message if transactions are not available.
        print("\nSince no transactions available, no updates can be done")
    
    return transactions # return the changes made to the transactions dictionary.