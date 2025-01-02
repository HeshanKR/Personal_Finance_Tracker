# Import neccessary python libraries for the use of the delete_transaction function.
import tkinter.messagebox as mbox

#Define delete_transaction function.
def delete_transaction(delete_val,del_by_category,transactions):

    # Check if transactions are available.
    if transactions:

        # Ask the user if they want to delete an entire category or individual transactions.
        delete_choice = del_by_category
        
        # If the user wants to delete an entire category.
        if delete_choice:
            # Get the category to delete from the user.
            category_to_delete = delete_val
            
            # Check if the category exists.
            if category_to_delete in transactions:
                # Remove the entire category.
                del transactions[category_to_delete]
                #Display the category deleted message.
                print(f"\nThe category '{category_to_delete}' has been deleted.")
                mbox.showinfo("Delete transaction",f"The category '{category_to_delete}' has been deleted ") # GUI message to be displayed to user.
                delete_message= (f"The category '{category_to_delete}' has been deleted.")
            else:
                # Display error message if category doesn't exist.
                print("\nCategory provided was not Found!")
                mbox.showerror("Delete transaction","Category provided was not Found!") # GUI message to be displayed to user.
                delete_message = ("Category provided was not Found!")

        else:

            # Get the serial number of the transaction to be deleted from the user.
            serial_v = delete_val

            # Initialize Transaction_found variable to false as the initial value.
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
                        mbox.showinfo("Delete transaction","Transaction successfully deleted") # GUI message to be displayed to user.
                        delete_message= (f"Transaction deleted ('{category}') =  Serial_no: {deleted_transaction['serial_no']:^5}--Amount: ${deleted_transaction['amount']:^10,.1f} -- Type: {deleted_transaction['t_type']:^10} -- Date: {deleted_transaction['date']:^12}")
                        
                        break  # Exit the loop once the transaction is found.

            # If the transaction is not found, display an error message.
            if not transaction_found:
                print("Transaction with the given serial number not found.")
                mbox.showerror("Delete transaction","Transaction with the given serial number not found.") # GUI message to be displayed to user.
                delete_message= ("Transaction with the given serial number not found.")
        return delete_message
    else:
        # Give the appropriate error message if transactions are not available
        mbox.showerror("Delete transaction","Since no transactions available, no deletions can be done.") # GUI message to be displayed to user.
        print("Since no transactions available, no deletions can be done.")