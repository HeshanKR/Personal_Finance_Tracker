# Import the view_transactions function to be used inside the delete_transaction function
from features.view_fn import view_transactions

#Define delete transaction function.
def delete_transaction(transactions):
    # Display the transactions to the user by calling view_transactions function.
    view_transactions(transactions)
    
    # Check if transactions are available.
    if transactions:

        # Ask the user if they want to delete an entire category or individual transactions.
        delete_choice = input("Do you want to delete an entire category? (y/n): ").lower()
        
        # If the user wants to delete an entire category.
        if delete_choice.startswith('y'):
            # Get the category to delete from the user.
            category_to_delete = input("Enter the category to delete: ")
            
            # Check if the category exists.
            if category_to_delete in transactions:
                # Remove the entire category.
                del transactions[category_to_delete]
                print(f"\nThe category '{category_to_delete}' has been deleted.")
            else:
                # Display error message if category doesn't exist.
                print("\nCategory provided was not Found!")

        elif delete_choice.startswith('n'):

            # Get the serial number of the transaction to be deleted from the user.
            serial_v = input("Enter the serial No. of the transaction to delete: ")

            # Set the Transaction_found variable to false as the initial value.
            transaction_found = False

            # Iterate over each category and its transactions.
            for category, entries in transactions.items():
                # Iterate through each transaction entry.
                for entry_index, entry in enumerate(entries):
                    # Check if the serial number matches.
                    if entry["serial_no"] == serial_v:
                        # Remove the transaction.
                        deleted_transaction = transactions[category].pop(entry_index)
                        # Set the the transaction_found variable to True to indicate the transaction is found.
                        transaction_found = True
                        # Display the details of the deleted transaction.
                        print(f"\nTransaction deleted ('{category}') =  Serial_no: {deleted_transaction['serial_no']:^5}--Amount: ${deleted_transaction['amount']:^10,.1f} -- Type: {deleted_transaction['t_type']:^10} -- Date: {deleted_transaction['date']:^12}")
                        break  # Exit the loop once the transaction is found.


            # If the transaction is not found, display an error message.
            if not transaction_found:
                print("\nTransaction with the given serial number not found.")
        else:
            #Display an error message if the user provides an invalid choice as delete_choice.
            print("\nplease provide your choice as yes(y) or no(n) next time.")
    else:
        # Give the appropriate error message if transactions are not available
        print("\nSince no transactions available, no deletions can be done.")
        
    return transactions # return the changes made to the transactions dictionary.