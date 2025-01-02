# Import random library for generating random numbers.
import random

# define the gen_rand_serial function.
def gen_rand_serial(transactions):
    
    #generate a random serial number between 0-9999.
    rand_no= random.randint(0,9999)
    # assigns the random number generated as a 4 digit value to the serial_no variable as a string.
    serial_no = f"{rand_no:04d}"

    #Initialize an empty list to store all existing serial numbers of previous transactions.
    serial_numbers = []

    # Iterate through each category and its transactions to gather all serial numbers.
    for entries in transactions.values():
        # Iterate through each transaction entry.
        for entry in entries:
            # Extract the serial number and append it to the list "serial_numbers".
            serial_numbers.append(entry["serial_no"])

    #starting an endless loop to make sure that the serial number is unique.     
    while True:
        if serial_no in serial_numbers:
            #generate a random serial number.
            rand_no= random.randint(0,9999)
            # assigns the random number generated as a 4 digit value to the serial_no variable as a string.
            serial_no = f"{rand_no:04d}"
        else:
            #break out of loop after the new serial number is unqiue amoung the other serial numbers given to previous transactions.
            break

    return serial_no # returns the unique serial number generated.