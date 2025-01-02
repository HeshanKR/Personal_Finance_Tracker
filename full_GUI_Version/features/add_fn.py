# Import Necessary python libraries and import necessary functions from subfiles.
from datetime import datetime 
from features.serial_gen import gen_rand_serial
import tkinter.messagebox as mbox

# Define the add_transaction function.
def add_transaction(category_,amount_,transaction_type_,date_ ,transactions):
        #Making sure that the user enter a value as the amount, that is valid for the transaction.
        try:
            amount = float(amount_)
            # Handling the instance where the user gives the amount that is equal to Zero.
            if amount<=0:
                # Display error message if the value entered as the amount is less than or equal to Zero.
                mbox.showerror("Add Transaction Error","Transaction cannot have negative values or equal to Zero. Therefore, your attempt to record the transactions was discarded!")# GUI message to be displayed to user.
                print("Transaction cannot have negative values or equal to Zero. Therefore, your attempt to record the transactions was discarded!")
                return
                
        except ValueError:
            #Displays the error message that the value entered as the amount is invalid.
            mbox.showerror("Add Transaction Error","You entered a non-numerical value as the amount. Therefore, your attempt to record the transactions was discarded!")# GUI message to be displayed to user.
            print("You entered a non-numerical value as the amount. Therefore, your attempt to record the transactions was discarded!")
            return
        
        else:
            # Generate a random serial number for the transaction using the gen_rand_serial function.
            serial_no = gen_rand_serial(transactions)

            # Gathering other inputs requirements to be filled for recording of the transaction.
            category = str(category_).capitalize()
            transaction_type = str(transaction_type_).capitalize()
            date=str(date_)

            # Making sure that the category type is not empty if so, then a default value is assigned.
            if category =="":
                category = "Miscellanous"

            # Check if the date is in the valid format (YYYY-MM-DD).
            try:
                datetime.strptime(date, '%Y-%m-%d')

            except ValueError:
                #Display error message for invalid date format.
                mbox.showinfo("Add Transaction","Invalid date format. Please use YYYY-MM-DD next time.\nThe current date has been set as the transaction date.")# GUI message to be displayed to user.
                print("Invalid date format. Please use YYYY-MM-DD next time. The current date has been set as the transaction date.")

                # Get the current date and time.
                current_datetime = datetime.now()
                # Extract the date part only.
                current_date = current_datetime.date()
                # Format the date as a string in the specified format.
                formatted_date = current_date.strftime("%Y-%m-%d")
                #Assign the formated date as the date of the transaction.
                date = formatted_date

            # Appending the transaction only if the transaction type fall into the category of either Income or Expense.
            if ((transaction_type.startswith("Inc") or transaction_type.startswith("Exp")) and transaction_type !=""):

                # Set type transaction_type string value to either Income or Expense, if the user gives an incomplete input.
                if transaction_type.startswith("I"):
                    transaction_type="Income"
                else:
                    transaction_type="Expense"

            
                # Check if the category already exists in transactions, if not, creating it.
                if category not in transactions:
                    transactions[category] = []

                # Create a new transaction entry.
                new_transaction = {
                    "serial_no": serial_no,
                    "amount": amount,
                    "t_type": transaction_type,
                    "date": date
                }

                # Append the new transaction to the appropriate category list.
                transactions[category].append(new_transaction)

                # Inform user about successful transaction addition of the transaction.
                mbox.showinfo("Add Transaction", "Transaction added successfully.Make sure to save and quit to save the transaction!")# GUI message to be displayed to user.

                #Display success message when the transaction is added.
                print("Transaction added successfully added to queue!\nMake sure to save and quit to save the transaction!")


            else:
                # Display a message that the transaction was discarded as it was not specified as either Income or expense.
                mbox.showerror("Add Transaction Error", "Transaction was not specified as either Income or expense.Therefore, it was discarded")# GUI message to be displayed to user.
                print("Transaction was not specified as either Income or expense.Therefore, it was discarded.")