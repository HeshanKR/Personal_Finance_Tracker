# Import Necessary python libraries.
from datetime import datetime 
from features.serial_gen import gen_rand_serial

# Define the add_transaction function.
def add_transaction(transactions):
    #checking the number of transactions the user is willing to record.
    try:
        transaction_count=int(input("How many transactions do you wish to enter (maximum 7): "))
    except ValueError:
        #Display an error message to user if the input entered as transaction count in invalid.
        print("\nPlease enter a valid value as the number of transactions you wish to enter! ")
    else:
        #checking if the transaction count is in between 0(excluding) and 7(including).
        if 0< transaction_count <=7:
            # recording the transactions one by one.
            for count in range(1,transaction_count+1):
                #Making sure that the user enter a value as the amount, that is valid for the transaction.
                try:
                    amount = float(input("Enter the amount (eg: 45062): "))
                    # Handling the instance where the user gives the amount that is equal to Zero.
                    if amount<=0:
                        print("\nTransaction cannot have negative values or equal to Zero. Therefore, the transaction was discarded")
                        continue #Move to the next iteration of the loop.
                        
                except ValueError:
                    #Displays the error message that the value entered as amount  is invalid.
                    print("\nPlease enter a valid numerical value ")
                    print("your attempt for recording the previous transactions was discarded,\nplease Move onto record your next transaction!")
                    continue #Move to the next iteration of the loop.
                else:
                    # generating a random serial number for the transaction using the gen_rand_serial function.
                    serial_no = gen_rand_serial(transactions)

                    # Gathering other inputs requirements to be filled for recording of the transaction.
                    category = str(input("Enter the category (default :Miscelleanous): ")).capitalize()
                    transaction_type = str(input("Enter the type 'I'(Income)/'E'(Expense): ")).capitalize()
                    date=str(input("Enter the date of transaction(YYYY-MM-DD): "))

                    # Making sure that the category type is not empty if so, then a default value is assigned.
                    if category =="":
                        category = "Miscellanous"

                    # Checking if value inputed as the date is a valid date.
                    try:
                        datetime.strptime(date, '%Y-%m-%d')

                    except ValueError:
                        #Display error message invalid date format.
                        print("\nInvalid date format. Please use YYYY-MM-DD next time.\nThe date for the current transaction been entered is set to the current date!")

                        # Get the current date and time.
                        current_datetime = datetime.now()
                        # Extract the date part only.
                        current_date = current_datetime.date()
                        # Format the date as a string in the specified format.
                        formatted_date = current_date.strftime("%Y-%m-%d")
                        #assigning the formated date as the date of the transaction.
                        date = formatted_date

                    # Appending the transaction only if the transaction type fall into the category of either Income or Expense.
                    if ((transaction_type.startswith("I") or transaction_type.startswith("E")) and transaction_type !=""):

                        # setting type transaction_type string value to either Income or Expense if the user gives a incomplete input.
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

                        #Display success message when the transaction is added.
                        print("\nTransaction added successfully added to queue!\nMake sure to save and quit to save the transaction!")
                    else:
                        #Display unsuccessful message, if transaction was not specified as either Income or expense.
                        print("\nTransaction was not specified as either Income or expense.Therefore, it was discarded.")
                        continue #Move to the next iteration of the loop.
        else:
            # Display rejection message if the transaction count is not within the range 1-7.
            print("\nOnly a maximum of 7 transactions are allowed to be entered at once!\nNegative values are not accepted")

    return transactions # return the changes made to the transactions dictionary.