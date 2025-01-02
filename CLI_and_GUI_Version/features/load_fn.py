#import json and os python library to be used inside load_transactions function.
import os 
import json

# Define the load_transactions function.
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
                # load transactions from the JSON file to transactions variable.
                transactions = json.load(file)
            except json.JSONDecodeError:
                # Handle the case where there's an issue decoding JSON and give a proper error message.
                print("No transactions found within file. Starting with an empty Dictionary.")
            else:
                # Inform the user that transactions were loaded successfully
                print("\nTransactions loaded successfully.")
    #Handle file not found error.            
    except FileNotFoundError as e:

        #Display error message for file not found and start with an empty dictionary.
        print(f"No transactions file found. Starting with an empty dictionary.\n{e}")


    return transactions # Return transactions to the main program


