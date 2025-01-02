#import the json,tkinter.messagebox, and os python library to be used in save_transactions function.
import os
import json
import tkinter.messagebox as mbox

#Define the save_transactions function.
def save_transactions(transactions):

    # Finding the absolute file path of the transactions.json file. 
    file_path = os.path.abspath("transactions.json")

    #File path if absolute file path doesn't work in python IDLE.
    file_path2="transactions.json"

    #Using try block to handle issues where there's issues where inputs and outputs will not work due to OS related issues.
    try:
        
        # Check if file_path is a valid path.
        if os.path.exists(file_path):
            
            # Open the "transactions.json" file for writing using the absolute file path.
            with open(file_path, "w") as file:
                # Write the transactions data to the file as JSON.
                json.dump(transactions, file, indent=4)
        else:
            
            # Open the backup file path if the absolute file path does not exist.
            with open(file_path2, "w") as file:
                # Write the transactions data to the file as JSON.
                json.dump(transactions, file, indent=4)
        
        # Display a message for the user indicating that the transactions were saved successfully.
        mbox.showinfo("Save & quit", "Transactions saved successfully.") # GUI message to be displayed to user.
        print("Transactions saved successfully.")

    # Handle any other input/output error  that may occur .
    except OSError as e:
        # Handle any other input/output error and provide a proper error message.
        mbox.showwarning("Save & quit Error", f"Error: Could not save transactions. Input/output error: {e}") # GUI message to be displayed to user.
        print(f"Error: Could not save transactions. Input/output error: {e}")