#import json, os, and tkinter.messagebox python library to be used inside load_transactions function.
import os 
import json
import tkinter.messagebox as mbox

# define load transactions function.
def load_transactions():
    #Initialize an empty Dictionary for transactions.
    transactions = {}

    # Get the absolute file path of "transactions.json"
    file_path = os.path.abspath("transactions.json")
    
    #checking if file available or not.
    try:  
        # Attempt to open the "transactions.json" file for reading.
        with open(file_path, "r") as file:
            try:
                # Read transactions from the JSON file and parse it as JSON to transactions variable.
                transactions = json.load(file)
            except json.JSONDecodeError:
                # Handle the case where there's an issue decoding JSON and give a proper error message.
                mbox.showwarning("Load transactions","No transactions found within file. Starting with an empty Dictionary.") #GUI message to be displayed to user.
                print("No transactions found within file. Starting with an empty Dictionary.")
            else:
                # Inform the user that transactions were loaded successfully
                print("Transactions loaded successfully.")
    #Handle file not found error.            
    except FileNotFoundError as e:

        #Display error message for file not found and start with an empty dictionary.
        mbox.showerror("Load transactions","No transactions file found. Starting with an empty dictionary.") #GUI message to be displayed to user.
        print(f"No transactions file found. Starting with an empty dictionary.\n{e}")

    return transactions # Return transactions to the main program


