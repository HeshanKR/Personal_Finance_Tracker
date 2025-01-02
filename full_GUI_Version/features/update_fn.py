# Import neccessary python libraries for the use of the update_transaction function.
from datetime import datetime
import tkinter.messagebox as mbox


# Define the update_transaction function.
def update_transaction(serial_no, amount, transaction_type, date, transactions):

    # Check if transactions are available.
    if transactions:
        # Get the serial No. of the transaction to be updated that was entered by the user.
        serial_v = serial_no

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
                    
                    # Get the amount from the user and check if it is valid.
                    try:
                        amount_ = float(amount)
                                
                    except ValueError:
                        #Display proper error message to user if the amount value entered in invalid.
                        mbox.showerror("update changes","Please enter a valid values that are numerical, your attempt to update the transaction was discarded") # GUI Message to be displayed to user.
                        print("Please enter a valid values that are numerical, your attempt to update the transaction was discarded.")
                        return

                    else:

                        # Check if the amount is non-negative.
                        if amount_<=0:
                            # Display proper error message if amount is negative or equal to Zero. 
                            mbox.showerror("Update Transaction Error","Transaction cannot have negative values or equal to Zero. Therefore, the transaction update was discarded!")# GUI Message to be displayed to user.
                            print("Transaction cannot have negative values or equal to Zero. Therefore, the transaction update was discarded")
                        else:
                            # Get the transaction type from the user input.
                            transaction_type_ = str(transaction_type).capitalize()
                            # Get the transaction date from the user input.
                            date_=str(date)

                            #Validate the date format.
                            try:
                                # Checking if value the inputed is a valid date (YYYY-MM-DD).
                                datetime.strptime(date, '%Y-%m-%d')

                            except ValueError:
                                #Display proper error message if date entered is invalid and assigning current date as date.
                                mbox.showinfo("Update Transaction","Invalid date format. Please use YYYY-MM-DD next time.\nThe date for the current transaction has been set to the current date!")# GUI Message to be displayed to user.
                                print("Invalid date format. Please use YYYY-MM-DD next time. The date for the current transaction has been set to the current date!")

                                # Get the current date and time.
                                current_datetime = datetime.now()
                                # Extract the date part only.
                                current_date = current_datetime.date()
                                # If you want to format the date as a string in a specific format.
                                formatted_date = current_date.strftime("%Y-%m-%d")
                                #assigning the formated date as the date of the transaction.
                                date_ = formatted_date

                            # Update the transaction only if the transaction type falls into the transaction type of either Income or Expense.
                            if ((transaction_type_.startswith("Inc") or transaction_type_.startswith("Exp")) and transaction_type_ !=""):

                                # set type transaction_type string value to either Income or Expense if the user gives a incomplete input.
                                if transaction_type_.startswith("I"):
                                    transaction_type_="Income"
                                else:
                                    transaction_type_="Expense"

                                # Update the values in the dictionary.
                                entry["amount"] = amount_
                                entry["t_type"] = transaction_type_
                                entry["date"] = date_

                                # Display that the transaction was successfully updated.
                                mbox.showinfo("Update Transaction","Transaction updated successfully!")# GUI Message to be displayed to user.
                                print("Transaction updated successfully!")
                                break  # Exit the loop once the transaction is updated.
                            else:
                                # Display transaction prevented from being updated message to user.
                                mbox.showerror("Update Transaction Error","Sorry your update cannot be executed unless you specify whether transaction is either a Income or an Expense.!")# GUI Message to be displayed to user.
                                print("Sorry your update cannot be executed unless you specify whether transaction is either a Income or an Expense.!")
            if transaction_found:
                break  # Exit the outer loop once the transaction is found and updated.

        if not transaction_found:
            # Display Error message if transaction for the serial number given is not found.
            mbox.showerror("Update Transaction Error","Transaction with the given serial number is not found.")# GUI Message to be displayed to user.
            print("Transaction with the given serial number is not found.")
    else:
        # Give the appropriate message if transactions are not available.
        mbox.showerror("Update Transaction Error","Since no transactions available, no updates can be done")# GUI Message to be displayed to user.
        print("Since no transactions available, no updates can be done")
