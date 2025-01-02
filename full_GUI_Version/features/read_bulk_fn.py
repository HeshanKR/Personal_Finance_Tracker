# import the necessary python modules and functions(from subfiles). 
from datetime import datetime
from features.serial_gen import gen_rand_serial
import tkinter.messagebox as mbox

# define read_bulk_transactions_from_file function.
def read_bulk_transactions_from_file(filename,transactions):
    # finding the absolute file path 
    file_path = filename

    # Initialize variables to keep track of invalid transactions and valid transactions
    invalid_trans=0
    valid_trans=0
    
    # Attempt to open the "read_bulk.txt" file for reading
    with open(file_path, "r") as file:

        # Check if the file is empty or not. If file empty, display file data not available message.
        content = file.read()
        if content.strip() == "":
            # Display a message if the file is empty.
            mbox.showwarning("Read transactions in bulks","File data not available!") # GUI message to be displayed to user.
            print("File data not available!")
            return transactions # Return the transactions variable without adding any transactions if the read file is empty.

        # Move the file pointer back to the beginning of the file.
        file.seek(0)

        # Reading the file line by line.
        for line in file:
            # Split the line into category, amount, transaction type, and date.
            try:
                category, amount_str, t_type, date_str = line.strip().split(', ')
            except ValueError:
                #incrementing the total of invalid transactions.
                invalid_trans+=1
                #Display error message if a transaction data in the read file is not according to the correct format.
                print(f"Invalid transaction format(missing values): {line}")
                continue # move to the next iteration.
            else:
                # Convert amount to float and handle invalid amounts.
                try:
                    amount = float(amount_str)
                    # checking if the amount value is equal to zero.
                    if amount <= 0:
                        #incrementing the total of invalid transactions.
                        invalid_trans+=1
                        #if the amount value is equal to zero, display error message.
                        print(f"Invalid transaction format, the amount of transaction is invalid in line : {line}")
                        continue #move to the next iteration.
                except ValueError:
                    #incrementing the total of invalid transactions.
                    invalid_trans+=1

                    # If amount value is a invalid data type, display error message.
                    print(f"Invalid transaction format, the amount of transaction is invalid in line : {line}")
                    continue #move to the next iteration.

                # check if the date provided for the transaction in the file is in correct format.  
                try:
                    datetime.strptime(date_str, '%Y-%m-%d')
                    date = date_str
                except ValueError:
                    #Display error message for invalid date format.
                    print(f"Invalid transaction format, the date of transaction is invalid in line : {line}")

                    # Get the current date and time.
                    current_datetime = datetime.now()
                    # Extract the date part only.
                    current_date = current_datetime.date()
                    # Format the date as a string in the specified format.
                    formatted_date = current_date.strftime("%Y-%m-%d")
                    #assigning the formated date as the date of the transaction.
                    date = formatted_date

                # Make the Transaction_type value lowercase to check with the conditions below.
                t_type = t_type.lower()

                # Check if the Transaction type value are valid or not
                if (t_type.startswith("inc") or t_type.startswith("exp")) and t_type != "":
                    # Assign the transaction type as Income or Expense based on the input.
                    if t_type.startswith("inc"):
                        t_type = "Income"
                    else:
                        t_type = "Expense"

                    # generate a random serial number for the transaction using a function.
                    serial_no = gen_rand_serial(transactions)
                    
                    # Create a new transaction dictionary
                    new_transaction = {"serial_no": serial_no, "amount": amount, "t_type": t_type, "date": date}
                    
                    # Add the transaction to the transactions dictionary under the appropriate category.
                    if category in transactions:
                        transactions[category].append(new_transaction)
                    else:
                        transactions[category] = [new_transaction]

                    #increment the total of valid transactions.
                    valid_trans+=1
                    #Display transaction recorded successfully for the transactions in correct format.
                    print("Transactions added successfully, Make sure save changes!")
                else:
                    #increment the total of invalid transactions.
                    invalid_trans+=1
                    #Display Error message for the transactions in invalid format.
                    print(f"Invalid transaction format, the transaction type is invalid in line : {line}")


    return invalid_trans,valid_trans # Return the counts of invalid and valid transactions.