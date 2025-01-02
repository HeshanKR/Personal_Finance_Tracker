# import the necessary python libraries, and import the necessary functions from files located in the subfolder called "features".
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mbox
from features.gen_trans_list_fn import gen_transaction_list
from features.load_fn import load_transactions
from features.save_fn import save_transactions
from features.add_fn import add_transaction
from features.view_fn import view_transactions
from features.delete_fn import delete_transaction
from features.update_fn import update_transaction
from features.dis_summary_fn import display_summary
from features.read_bulk_fn import read_bulk_transactions_from_file

# define the class with it's properties and methods.
class FinanceTrackerGUI:
    def __init__(self):
        '''
        Initialize the properties of the class FinanceTrackerGUI.
        '''
        self.transactions = load_transactions() # Load transactions from a JSON file and assign them to self.transactions.
        # converts the transactions dictionary to a list called transactions_list using generate transaction list function, so that the data can be inserted to the tree view widget.
        self.transactions_list = gen_transaction_list(self.transactions) # Convert the transactions dictionary to a list.


    # Define the create_widget() method.
    def create_widgets(self, transactions_list):
        self.root = tk.Tk() # Create a Tkinter root window.
        self.root.geometry("1150x400") # Set the geometry of the root window.
        self.root.title("Personal Finance Tracker - w2082289(UOW)/20222094(IIT)") # SET the Title of the window. 

        # Frame to show the title/name of the app and intro about the table.
        frame = tk.Frame(self.root, height=100, width=500, border=4, relief=tk.FLAT, bg="black") # Create frame1 for the app name.
        frame.pack(fill=tk.BOTH, padx=10, pady=5) # Add it to be displayed in the window.

        #Create label to display the app name.
        label = tk.Label(frame, text="Personal Finance Tracker", fg="blue", font=("Arial", 12, "bold"))
        label.pack()# packing it.

        # Create label to display intro about the table.
        label_2 = tk.Label(frame, text="Down below table records all your transactions:", fg="red",font=("Arial", 11, "bold"), bg="black")
        label_2.pack(side="bottom", anchor="w")# packing it.

        # Frame for table and scrollbar and packing it.
        frame2 = tk.Frame(self.root, height=300, width=500, border=4, relief=tk.GROOVE, bg="yellow")
        frame2.pack(fill=tk.BOTH, padx=10, pady=5)

        # Create a Treeview widget for displaying the table
        columns = ("Category", "Serial No.", "Amount", "Type", "Date") # initialize the columns tuple with value/column names.
        self.tree = ttk.Treeview(frame2, columns=columns, show="headings")# creating the treeview widget.

        # Create a custom style for the heading text of the treeview.
        style = ttk.Style()
        style.configure("Treeview.Heading", foreground="red", font=("Arial", 11, "bold"))

        # Add headers for the columns
        for col in columns:
            # make the column items alignment as center and keeps a minimum width of 200 so that the columns cannot be shrunk beyond that.
            self.tree.column(col, anchor="center", minwidth=200)
            """
            sets up the heading for the column specified by variable "col",
            and it's text is also set to "col" value.Then creates an anonymous function using lambda that takes argument "c" and it's value is set to "col",
            this ensures that correct column is passed to sort_column function. Then sort_column method is called that takes the "c" and "False" paramters to the function(This is to sort in ascending order).
            """
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(c, False))

        # Add scrollbars and packs them.
        scrollbar_y = ttk.Scrollbar(frame2, orient="vertical", command=self.tree.yview)# the "self.tree.yview" make the scroll bar to work as the vertical scroll of the treewidget.
        scrollbar_y.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar_y.set) #scroll bar vertical

        scrollbar_x = ttk.Scrollbar(frame2, orient="horizontal", command=self.tree.xview) # the "self.tree.yview" make the scroll bar to work as the horizontal scroll of the treewidget.
        scrollbar_x.pack(side="bottom", fill="x")
        self.tree.configure(xscrollcommand=scrollbar_x.set) #scroll bar horizontal

        # Insert data into from transaction list to the Treeview.
        for transaction in transactions_list:
            self.tree.insert("", "end", values=transaction)# "" mean there no parent, "end" mean the items are packed at end. And the value entered will be the transaction(list).

        self.tree.pack(expand=True, fill=tk.BOTH) # finally pack the tree in a way that it takes the whole area inside the "frame2".

        
        # create a frame 3 to hold all the buttons needed to be added for the search feature and pack it.
        frame3 = tk.Frame(self.root, height=100, width=200, border=4, relief=tk.FLAT, bg="black")
        frame3.pack(fill=tk.BOTH, padx=10, pady=5)
        # Label for search bar and pack it. 
        label_3 = tk.Label(frame3, text="Search Transactions:", fg="white", font=("Arial", 11, "bold"), bg="black")
        label_3.pack(side="left")
        # search bar entry and pack it.
        self.search_entry = tk.Entry(frame3, width=50)
        self.search_entry.pack(side="left")

        # To get the selected column (default is Category).
        self.selected_column = tk.StringVar()
        self.selected_column.set("Category")

         # The radio button frame to select which column data the user wants to search.
        radio_buttons_frame = tk.Frame(frame3)
        radio_buttons_frame.pack(side="left")

        #creating the radio button options.
        for col in columns:
            # here the variable associated with the radio button will be "selected_column" and the value assigned to that variable will be "col".
            rb = tk.Radiobutton(radio_buttons_frame, text=col, variable=self.selected_column, value=col, bg="black",fg="white", selectcolor="black")
            rb.pack(side="left")

        # The search execution button that calls search() function.
        search_button = tk.Button(frame3, text="Search", relief=tk.RAISED, command=self.search)
        search_button.pack(side="left")

        # The search reset button that calls reset() function.
        reset_button = tk.Button(frame3, text="Reset", command=self.reset)
        reset_button.pack(side="left")

        # quit button that call quit_window() function.
        quit_button = tk.Button(frame3, text="Quit window", command=self.quit_window, bg="silver", fg="red",font=("Arial", 8, "bold"))
        quit_button.pack(side="right")

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    # define the sort_column() method.
    def sort_column(self, col, reverse):
        """
        The line below is a list comprehension that iterates over each child item(row) of the tree widget.
        For each child item,"self.tree.set(child, col)",this method returns the value stored in the specified column for the given child item.
        "child", This part of the tuple simply represents the child item itself.In tkinter each row has an item ID,
        so that is the value extracted here.
        (self.tree.set(child, col), child), this simply creates a tuple including the values and IDs extracted.
        """
        if col == "Amount": # Check if sorting the amount column.
            data = [(float(self.tree.set(child, col)), child) for child in self.tree.get_children("")]
        else:
            data = [(self.tree.set(child, col), child) for child in self.tree.get_children("")]
        """
        The line belowchecks if the the value passed as the value of the reverse is True or False,
        if True nothing happens just sorts in ascending order, else it sorts in descending order.
        """
        data.sort(reverse=reverse)
        """
        The code below is a loop iterates over the sorted data list of tuples.
        For each tuple (item), it extracts the child item (row) and its index in the sorted list (index).
        It rearranges the rows in the Treeview widget based on the sorted data by moving each row to its new position.
        """
        for index, item in enumerate(data):
            self.tree.move(item[1], "", index)
        # Switch the sorting order for next click to sort in descending order.
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))


    # define the search() method.
    def search(self):
        search_text = self.search_entry.get() # Get the search text value entered.
        selected_column = self.selected_column.get() # Get the selected column for the search (from the radio button group for column selection).

        self.tree.delete(*self.tree.get_children()) # delete's all the items displayed in the tree-view.

        search_index = None # initialize the searching index for a transaction list.
        found = False # Initialize the "found" variable as False.

        # determine the index to be searched in a transaction list depending on the column searched
        if selected_column == "Category":
            search_index = 0
        elif selected_column == "Serial No.":
            search_index = 1
        elif selected_column == "Amount":
            #checking if the value entered as a amount to be searched is convertible.
            try:
                search_text = float(search_text)# converting the search value to meet the data type of amount category.
            except ValueError:
                mbox.showerror("Search", "Invalid search value for amount.")
                return
            search_index = 2
        elif selected_column == "Type":
            search_index = 3
        else:
            search_index = 4

        # handling the instance where the user, accidently presses the search button.
        if search_text != "":
            #checking each transaction.
            for transaction in self.transactions_list:
                if search_text == transaction[search_index]:
                    found = True # setting the found variable as True to indicate that transaction was found.
                    # Insert the matching transaction into the treeview.
                    self.tree.insert("", "end", values=transaction)
                else:
                    continue # continue the search.
        else:
            found= False # setting the found variable as False to indicate that transaction was not found.

        if not found:
            # display error message if search is not found.
            mbox.showerror("Search", "No matching results found.")


    # define the reset() method.
    def reset(self):
        '''
        The line below is used to delete the content of the search entry, here delete() method removes characters from the widget.
        "0" here is the starting index and "end" means the ending index (which is the absolute end).
        ''' 
        self.search_entry.delete(0, 'end')
        self.tree.delete(*self.tree.get_children()) # Clear the existing items in the treeview.
        # Insert data into from transaction list to the Treeview.
        for transaction in self.transactions_list:
            self.tree.insert("", "end", values=transaction)
        self.tree.pack(expand=True, fill=tk.BOTH)

    # define the quit_window() method.
    def quit_window(self):
        self.root.destroy()
#-------------------------------------------------------------------------------------------------------------------------

# define the main_menu() method.
def main_menu():
    # loading the data in "transactions.json" file and assign the data in it to the variable "transactions".
    transactions = load_transactions()

    # Display an Overview of the Personal Finance Tracker.
    print("\n--- Personal Finance Tracker ---")
    print("\nThis program is created to assist you to keep track of your day-to-day transactions.")
    print("This program calculates your transactions considering only transactions\nthat can be categorized as either Income or Expense. ")
    print("\nThis program is capable of finding your total profit (profit=income-expense) by analyzing your transactions")

    #Starting an endless loop.
    while True:

        # convert transaction dictionary to a list.
        transaction_list = gen_transaction_list(transactions)
        
        #Display the options provided by the application to the user.
        print("\nPlease select either of the options down below and provide the relevant option number to proceed!")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Display Summary")
        print("6. Save and Quit")
        print("7. Read transactions in bulk")
        print("8. Show transactions in GUI view\n")

        #Prompt the user to enter their choice out of the options(1-8).
        choice = input("Enter your choice (1-8): ")

        # Validate user's choice, if the choice is not within the range 1-8 give an error message.
        if choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
            # opening a try except block to avoid index errors if the user does not input a confirmation of the command.
            try:
                # To confirm that the user has made his/her choice correctly(willingly).    
                confirm_c = input("Confirm your choice ['Y'/'N']: ").lower()[0]
            except IndexError:
                # Display error message if the user does not enter the confirmation.
                print("Confirmation rejected!, do you wish to make a different choice?")
            else:

                # Execute the rest of the code only if the confirmation is "y(yes)".   
                if confirm_c == "y":

                    #Checking what option matches with the users choice.
                    if choice == "1":
                        transactions = add_transaction(transactions)
                    elif choice == "2":
                        view_transactions(transactions)
                    elif choice == "3":
                        transactions = update_transaction(transactions)
                    elif choice == "4":
                        transactions = delete_transaction(transactions)
                    elif choice == "5":
                        display_summary(transactions)
                    elif choice == "7":
                        transactions = read_bulk_transactions_from_file(transactions)
                    elif choice == "8":
                        # checking if transaction are available in the transaction_list.
                        if transaction_list:
                            save_transactions(transactions) # save the transactions to the json file, before the tkinter GUI is opened.
                            return True # This boolean value decides whether the GUI is launched or not.
                        else:
                            print("\nThere are no transactions to be viewed in the GUI!\nPlease try again later after entering transactions. ")
                    else:
                        save_transactions(transactions)
                        break # exiting loop if option given is '6'.
                else:
                    #Display confirmation rejected message to user.
                    print("\nConfirmation rejected!, do you wish to make a different choice?")
        else:
            #Display error message if the users choice is invalid.
            print("\nInvalid choice. Please try again.")
    return False # This boolean value decides whether the GUI is launched or not.

# Define main() function.
def main():
    while True:
        if main_menu(): # run the main_menu function in a loop, until the option 8 is selected to view the GUI interface.
            app = FinanceTrackerGUI() # creates an class instance "app"
            app.create_widgets(app.transactions_list) # call the create_widget method.
            app.root.mainloop() # runs the root window in a loop.
        else:
            # if the user enters "6" as the option then the program should stop. if the main_menu returns False the the program should stop.
            break

# Checks if the code currently being executed is the main program, if so calls the function main().
if __name__ == "__main__":
    main()


# IF you are paid to do this assignment  please delete this line of comment.