# import the necessary python libraries, and import the necessary functions from files located in the subfolder called "features".
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mbox
from tkinter import filedialog
from features.gen_trans_list_fn import gen_transaction_list
from features.save_fn import save_transactions
from features.add_fn import add_transaction
from features.update_fn import update_transaction
from features.delete_fn import delete_transaction
from features.dis_summary_fn import display_summary
from features.load_fn import load_transactions
from features.read_bulk_fn import read_bulk_transactions_from_file


# define the class with it's properties and methods.
class FinanceTrackerGUI:
    def __init__(self, root):
        '''
        Initialize the properties of the class FinanceTrackerGUI.
        '''
        self.root = root # Assign the root window to the instance variable self.root.
        self.root.geometry("1150x500")  # Set the geometry of the root window.
        self.root.title("Personal Finance Tracker - w2082289(UOW)/20222094(IIT)")  # SET the Title of the window. 
        self.transactions = load_transactions()  # Load transactions from a JSON file and assign them to self.transactions.
        # converts the transactions dictionary to a list called transactions_list using generate transaction list function, so that the data can be inserted to the tree view widget.
        self.transactions_list = gen_transaction_list(self.transactions) # Convert the transactions dictionary to a list.
        self.create_widgets(self.transactions_list) # Calls the create_widget method with the transactions_list as the parameter.
        self.filename = None # Initialize the filename property to None.

    # Define the create_widget() method.
    def create_widgets(self,transaction_list):
        # Frame to show the title/name of the app and intro about the table.
        frame = tk.Frame(self.root,height=100,width=500, border= 4,relief= tk.FLAT,bg= "black") # Create frame1 for the app name.
        frame.pack(fill=tk.BOTH,padx=10, pady=5) # Add it to be displayed in the window.


        #Create label to display the app name.
        label = tk.Label(frame, text="Personal Finace tracker",fg="blue",font=("Arial", 12, "bold")) # The label that stores the app name.
        label.pack() # packing it.

        # Create label to display intro about the table.
        label_2 = tk.Label(frame, text="Down below table records all your trasactions:",fg="red",font=("Arial",11,"bold"), bg="black") # The label that has the intro.
        label_2.pack(side= "bottom",anchor="w") # packing it.




        # Frame for table and scrollbar and packing it.
        frame2 = tk.Frame(self.root,height=300,width=500, border= 4,relief=tk.GROOVE,bg= "yellow")
        frame2.pack(fill=tk.BOTH,padx=10, pady=5)
    
        # Create a Treeview widget for displaying the table
        columns = ("Category","Serial No.","Amount","Type","Date") # initialize the columns tuple with value/column names.
        self.tree = ttk.Treeview(frame2, columns=columns, show="headings") # creating the treeview widget.

        # Create a custom style for the heading text of the treeview.
        style = ttk.Style()
        style.configure("Treeview.Heading", foreground="red",font=("Arial",11, "bold") )

        # Add headers for the columns
        for col in columns:
            # make the column items alignment as center and keeps a minimum width of 200 so that the columns cannot be shrunk beyond that.
            self.tree.column(col,anchor="center",minwidth=200) 
            """
            sets up the heading for the column specified by variable "col",
            and it's text is also set to "col" value.Then creates an anonymous function using lambda that takes argument "c" and it's value is set to "col",
            this ensures that correct column is passed to sort_column function. Then sort_column method is called that takes the "c" and "False" paramters to the function(This is to sort in ascending order).
            """
            self.tree.heading(col, text=col,command=lambda c=col: self.sort_column(c, False)) 

        # Add scrollbars and packs them.
        scrollbar_y = ttk.Scrollbar(frame2, orient="vertical", command=self.tree.yview) # the "self.tree.yview" make the scroll bar to work as the vertical scroll of the treewidget.
        scrollbar_y.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar_y.set) #scroll bar vertical

        scrollbar_x = ttk.Scrollbar(frame2, orient="horizontal", command=self.tree.xview) # the "self.tree.yview" make the scroll bar to work as the horizontal scroll of the treewidget.
        scrollbar_x.pack(side="bottom", fill="x")
        self.tree.configure(xscrollcommand=scrollbar_x.set) #scroll bar horizontal

        # Insert data into from transaction list to the Treeview.
        for transaction in transaction_list:
            self.tree.insert("", "end", values=transaction) # "" mean there no parent, "end" mean the items are packed at end. And the value entered will be the transaction(list).

        self.tree.pack(expand=True, fill=tk.BOTH)# finally pack the tree in a way that it takes the whole area inside the "frame2".





        # create a frame 3 to hold all the buttons needed to be added for the search feature and pack it.
        frame3= tk.Frame(self.root,height=100,width=200, border= 4,relief= tk.FLAT,bg= "black")
        frame3.pack(fill=tk.BOTH,padx=10, pady=5)
        # Label for search bar and pack it. 
        label_3 = tk.Label(frame3, text="Search Transactions:",fg="white",font=("Arial",11,"bold"), bg="black")
        label_3.pack(side= "left")
        # search bar entry and pack it.
        self.search_entry = tk.Entry(frame3,width=50)
        self.search_entry .pack(side="left")

        # To get the selected column (default is Category).
        self.selected_column = tk.StringVar()
        self.selected_column.set("Category") 

        # The radio button frame to select which column data the user wants to search.
        radio_buttons_frame = tk.Frame(frame3)
        radio_buttons_frame.pack(side="left") 

        #creating the radio button options.
        for col in columns:
            # here the variable associated with the radio button will be "selected_column" and the value assigned to that variable will be "col".
            rb = tk.Radiobutton(radio_buttons_frame, text=col, variable=self.selected_column, value=col, bg="black", fg="white", selectcolor="black") 
            rb.pack(side="left")

        # The search execution button that calls search() function.
        search_button = tk.Button(frame3, text="Search",relief=tk.RAISED, command=self.search)
        search_button.pack(side="left")

        # The search reset button that calls reset() function.
        reset_button = tk.Button(frame3, text="Reset", command=self.reset)
        reset_button.pack(side="left")





        # create a big frame to hold the all the other frames.
        bigframe= tk.Frame(self.root,height=100,width=200, border= 4,relief= tk.FLAT,bg= "black")
        bigframe.pack(fill=tk.BOTH,expand=True,padx=10, pady=5)


        # create a frame 4 to hold the all the buttons to be inserted to frame 4.
        frame4= tk.Frame(bigframe,height=40,width=200, border= 4,relief= tk.FLAT,bg= "white")
        frame4.pack(fill=tk.BOTH,padx=1, pady=0)

        # Add transaction button that call toggle_frame5() function.
        add_trans_button = tk.Button(frame4, text="Add Transaction",command=self.toggle_frame5,bg="yellow",fg="black",font=("Arial",8,"bold"))
        add_trans_button.pack(side="left")

        # update transaction button that call toggle_frame6() function.
        update_trans_button = tk.Button(frame4, text="Update Transaction",command=self.toggle_frame6, bg="#02E283",fg="black",font=("Arial",8,"bold"))
        update_trans_button.pack(side="left", padx= 10)

        # Delete transaction button that call toggle_frame7_and_8() function.
        delete_trans_button = tk.Button(frame4, text="Delete Transaction",command=self.toggle_frame7_and_8, bg="#4dff4d",fg="black",font=("Arial",8,"bold"))
        delete_trans_button.pack(side="left", padx= (0,10))

        # Display summary of transactions button that call toggle_frame9() function.
        dis_sum_trans_button = tk.Button(frame4, text="Display summary of Transactions",command= self.toggle_frame9,bg="#0ed50e",fg="black",font=("Arial",8,"bold"))
        dis_sum_trans_button.pack(side="left", padx= (0,10))

        # To bulk read transactions from  a text file and add the data to the transactions variable.
        # Enter transactions in bulks button that call toggle_frame10() function.
        trans_bulk_read_button = tk.Button(frame4, text="Enter transactions in bulks",command=self.toggle_frame10, bg="#4dffff",fg="black",font=("Arial",8,"bold"))
        trans_bulk_read_button.pack(side="left", padx= (0,10))

        # Save transaction and quit button that call save_and_quit() function.
        save_quit_button = tk.Button(frame4, text="Save & Quit",command=lambda: self.save_and_quit(),bg="silver", fg="red",font=("Arial",8,"bold"))
        save_quit_button.pack(side="right")





        # create frame for entering values to add transaction function.
        self.frame5= tk.Frame(bigframe,height=200,width=200, border= 4,relief= tk.FLAT,bg= "yellow")
        self.frame5.pack_forget()  # Initially hide the frame

        # label for category input.
        label_4 = tk.Label(self.frame5, text="Transactions Category:",fg="black",font=("Arial",11,"bold"), bg="yellow")
        label_4.pack(side= "left")

        # Category entry for add transaction function.
        self.Add_Category_entry = tk.Entry(self.frame5,width=10)
        self.Add_Category_entry.pack(side="left") 

        # label for amount input.
        label_5 = tk.Label(self.frame5, text="Transactions Amount:",fg="black",font=("Arial",11,"bold"), bg="yellow")
        label_5.pack(side="left")

        # Amount entry for add transaction function.
        self.Add_amount_entry = tk.Entry(self.frame5,width=10)
        self.Add_amount_entry.pack(side="left") 

        # label for transaction type input.
        label_6 = tk.Label(self.frame5, text="Transactions type [ i / e ]:",fg="black",font=("Arial",11,"bold"), bg="yellow")
        label_6.pack(side="left")

        # transaction type entry for add transaction function.
        self.Add_type_entry = tk.Entry(self.frame5,width=10)
        self.Add_type_entry.pack(side="left") 
        
        # label for Date input.
        label_7 = tk.Label(self.frame5, text="Transactions Date:",fg="black",font=("Arial",11,"bold"), bg="yellow")
        label_7.pack(side="left")

        # Date entry for add transaction function.
        self.Add_Date_entry = tk.Entry(self.frame5,width=10)
        self.Add_Date_entry.pack(side="left") 

        # reset buttons for Add transaction function that call reset_frame5_entries() function.
        reset_frame5_button = tk.Button(self.frame5, text="Reset", command=self.reset_frame5_entries)
        reset_frame5_button.pack(side="right", padx=(5, 0))

        #Submit button of add transaction feature that call add_transaction_from_input() and self.toggle_frame5() functions.
        add_trans_submit_button = tk.Button(self.frame5, text="Submit",relief=tk.RAISED,command=lambda: (self.add_transaction_from_input(),self.toggle_frame5()))
        add_trans_submit_button.pack(side="right", anchor="w", padx=(10,0))



        
        # create frame for entering values to Update transaction function.
        self.frame6= tk.Frame(bigframe,height=200,width=200, border= 4,relief= tk.FLAT,bg= "#02E283")
        self.frame6.pack_forget()  # Initially hide the frame

        
        # label for Serial NO. input.
        label_8 = tk.Label(self.frame6, text="Transactions Serial No:",fg="black",font=("Arial",11,"bold"), bg="#02E283")
        label_8.pack(side="left")

        # Serial No. entry for update transaction function.
        self.upd_serialno_entry = tk.Entry(self.frame6,width=10)
        self.upd_serialno_entry.pack(side="left") 

        # label for amount input.
        label_9 = tk.Label(self.frame6, text="Transactions Amount:",fg="black",font=("Arial",11,"bold"), bg="#02E283")
        label_9.pack(side="left")

        # Amount entry for update transaction function.
        self.upd_amount_entry = tk.Entry(self.frame6,width=10)
        self.upd_amount_entry.pack(side="left") 

        # label for transaction type input.
        label_10 = tk.Label(self.frame6, text="Transactions type [ i / e ]:",fg="black",font=("Arial",11,"bold"), bg="#02E283")
        label_10.pack(side="left")

        # transaction type entry for update transaction function.
        self.upd_type_entry = tk.Entry(self.frame6,width=10)
        self.upd_type_entry.pack(side="left") 
        
        # label for Date input.
        label_11 = tk.Label(self.frame6, text="Transactions Date:",fg="black",font=("Arial",11,"bold"), bg="#02E283")
        label_11.pack(side="left")

        # Date entry for update transaction function.
        self.upd_Date_entry = tk.Entry(self.frame6,width=10)
        self.upd_Date_entry.pack(side="left") 

        # reset button for update transaction function that calls reset_frame6_entries()function.
        reset_frame6_button = tk.Button(self.frame6, text="Reset", command=self.reset_frame6_entries)
        reset_frame6_button.pack(side="right", padx=(5, 0))

        #Submit update transaction changes using this button.
        upd_trans_submit_button = tk.Button(self.frame6, text="Submit",relief=tk.RAISED, command=lambda :(self.update_transaction_from_input(),self.toggle_frame6()))
        upd_trans_submit_button.pack(side="right", anchor="w", padx=(10,0))




        # create frame for  delete transaction function.
        self.frame7= tk.Frame(bigframe,height=100,width=200, border= 4,relief= tk.FLAT,bg= "#4dff4d")
        self.frame7.pack_forget()  # Initially hide the frame

        # label for value input for deletion.
        label_12 = tk.Label(self.frame7, text="Transactions delete by value(Serial No./Category):",fg="black",font=("Arial",11,"bold"), bg="#4dff4d")
        label_12.pack(side="left")

        # Value entry for delete transaction function.
        self.del_value_entry = tk.Entry(self.frame7,width=10)
        self.del_value_entry.pack(side="left")

        self.var_del_by_category = tk.BooleanVar() #boolean variable to maintain the status of the Checkbutton. 
        #selected ==> True
        #not selected ==> False
        category_del_checkbutton = tk.Checkbutton(self.frame7, text="Delete by category", variable=self.var_del_by_category,fg="red") # created to get the choice of deletion method from user.
        category_del_checkbutton.pack(side="left",padx=(10,0))

        # Reset button for resetting previous delete transaction by value.
        reset_frame7_button = tk.Button(self.frame7, text="Reset", command=self.reset_frame7_entries)
        reset_frame7_button.pack(side="right", padx=(5, 0))


        #Submit deleted transaction changes button.
        del_trans_submit_button = tk.Button(self.frame7, text="Submit",relief=tk.RAISED, command= lambda: (self.delete_transaction_from_input(),self.toggle_frame7_and_8()))
        del_trans_submit_button.pack(side="right", anchor="e", padx=(10,0))



        # create frame for  delete transaction function.
        self.frame8= tk.Frame(bigframe,height=100,width=200, border= 4,relief= tk.FLAT,bg= "#4dff4d")
        self.frame8.pack_forget()  # Initially hide the frame

        # label for  deleted transaction.
        label_13 = tk.Label(self.frame8, text="Transaction deleted:",fg="black",font=("Arial",11,"bold"), bg="#4dff4d", width=16)
        label_13.pack(side="left",padx=(0,10))

        # label for Showing deleted transaction.
        self.label_14 = tk.Label(self.frame8, text="Deleted transaction....",fg="Black",font=("Arial",11,"bold"), bg="white", width=100)
        self.label_14.pack(side="left",padx=(0,10)) 

        # reset button for resetting  Label 14.
        reset_frame8_button = tk.Button(self.frame8, text="Reset", command=self.reset_frame8_label)
        reset_frame8_button.pack(side="right", padx=(0, 0))



        # create frame for  display summary transaction function.
        self.frame9= tk.Frame(bigframe,height=50,width=200, border= 4,relief= tk.FLAT,bg="#0ed50e")
        self.frame9.pack_forget()  # Initially hide the frame

        # label for display summary transaction.
        self.label_15 = tk.Label(self.frame9, text="Summary of transactions:",fg="black",font=("Arial",11,"bold"), bg="#0ed50e", width=20)
        self.label_15.pack(side="left",padx=(0,5)) 

        # Create a Text widget to show the summary of transactions.
        self.text_widget = tk.Text(self.frame9, wrap="word", width=50, height=10,font=("Arial",11,"bold"))
        self.text_widget.pack(side="left",padx=10, pady=10)

        #Submit display summary transaction changes button.
        dis_summary_submit_button = tk.Button(self.frame9, text="Generate summary",relief=tk.RAISED, command= lambda: (self.display_summary_transaction()))
        dis_summary_submit_button.pack(side="left", anchor="e", padx=(10,0))

        # Reset button for display summary.
        reset_frame9_button = tk.Button(self.frame9, text="Reset", command=self.reset_frame9_text)
        reset_frame9_button.pack(side="left", padx=(5,0))

        # Create a vertical scrollbar and attach it to the Text widget.
        self.v_scrollbar = tk.Scrollbar(self.frame9, orient=tk.VERTICAL, command=self.text_widget.yview)
        self.text_widget.config(yscrollcommand=self.v_scrollbar.set)
        self.v_scrollbar.pack(side="right",fill="y")




        # create frame for read transactions in bulks function.
        self.frame10= tk.Frame(bigframe,height=50,width=200, border= 4,relief= tk.FLAT,bg= "#4dffff")
        self.frame10.pack_forget()  # Initially hide the frame

        # label for read transactions in bulks from file.
        self.label_16 = tk.Label(self.frame10, text="Bulk read transactions from file:",fg="black",font=("Arial",11,"bold"), bg="#4dffff", width=25)
        self.label_16.pack(side="left",padx=(0,5)) 


        # Create a label for displaying the selected file.
        self.label_file = tk.Label(self.frame10, text="No file selected", wraplength=400)
        self.label_file.pack(side="left",padx=(5,0))

        # Create a button to browse for a file.
        browse_button = tk.Button(self.frame10, text="Browse", command=lambda :(self.browse_for_file())) 
        browse_button.pack(side="left",padx=(5,0))


        # Create a reset button to clear the selected file
        reset_button = tk.Button(self.frame10, text="Reset", command=lambda: self.reset_file_selection())
        reset_button.pack(side="right", padx=(5, 0))

        # Create a button to submit the selected file to read using the bulk_read_transactions() function.
        submit_file_for_read_button = tk.Button(self.frame10, text="submit file", command=lambda :(self.bulk_read_transactions())) 
        submit_file_for_read_button.pack(side="right",padx=(5,0))
        
    # ------------------------------------------------------------------------------------------------------------------------------------------------
    # Define all the Reset methods for each frames.


    def reset_frame5_entries(self):
        # Reset entry fields in frame 5
        self.Add_Category_entry.delete(0, tk.END) # here delete() method delete the string value entered from starting index "0" to index at "tk.END"("end").
        self.Add_amount_entry.delete(0, tk.END) 
        self.Add_type_entry.delete(0, tk.END)
        self.Add_Date_entry.delete(0, tk.END)

    def reset_frame6_entries(self):
        # Reset entry fields in frame 6
        self.upd_serialno_entry.delete(0, tk.END)
        self.upd_amount_entry.delete(0, tk.END)
        self.upd_type_entry.delete(0, tk.END)
        self.upd_Date_entry.delete(0, tk.END)

    def reset_frame7_entries(self):
        # Reset entry fields in frame 7
        self.del_value_entry.delete(0, tk.END)

    def reset_frame8_label(self):
        # Reset label text in frame 8
        self.label_14.config(text="Deleted transaction...")

    def reset_frame9_text(self):
        # Clear text in frame 9 (Text widget)
        self.text_widget.delete(1.0, tk.END) # here "1.0" indicates the beginning of the line.

    # To reset file selection label and selected file.
    def reset_file_selection(self):
        self.label_file.config(text="No file selected")
        self.filename = None


    #--------------------------------------------------------------------------------------------------------------------------------------------------------
    # define all toggle_frame functions to make them visible and invisible when the specific button is clicked to call them. 
    
    # define toggle_frame5() method.
    def toggle_frame5(self): 
        if self.frame5.winfo_ismapped(): # checks if the specified frame is mapped(displayed) in the window.
            self.frame5.pack_forget() # If True, remove the frame from the window.
        else:
            self.active_frame=[self.frame5] # create a list called "active_frame" and include the frames that need to be mapped in the window.
            self.hide_other_frames(self.active_frame) # call the hide_other_frames() method with the list "active_frame" as it's parameter.
            self.frame5.pack(fill=tk.BOTH, padx=1, pady=(5,0)) # if not mapped in the window, then map(displayed) it in the window.

    # define toggle_frame6() method.
    def toggle_frame6(self):
        if self.frame6.winfo_ismapped(): # checks if the specified frame is mapped(displayed) in the window.
            self.frame6.pack_forget() # If True, remove the frame from the window.
        else:
            self.active_frame=[self.frame6] # create a list called "active_frame" and include the frames that need to be mapped in the window.
            self.hide_other_frames(self.active_frame) # call the hide_other_frames() method with the list "active_frame" as it's parameter.
            self.frame6.pack(fill=tk.BOTH, padx=1, pady=(5,0))  # if not mapped in the window, then map(displayed) it in the window.

    # define toggle_frame7_and_8() Method.
    def toggle_frame7_and_8(self):
        if self.frame7.winfo_ismapped() and self.frame8.winfo_ismapped(): # checks if the specified frames are mapped(displayed) in the window.
            self.frame7.pack_forget()# If True, remove the frame 7 from the window.
            self.frame8.pack_forget()# If True, remove the frame 8 from the window.
        else:
            self.active_frame=[self.frame7,self.frame8] # create a list called "active_frame" and include the frames that need to be mapped in the window.
            self.hide_other_frames(self.active_frame) # call the hide_other_frames() method with the list "active_frame" as it's parameter.

            self.frame7.pack(fill=tk.BOTH, padx=1, pady=(5,0))  # if not mapped in the window, then map(displayed) it in the window.
            self.frame8.pack(fill=tk.BOTH, padx=1, pady=(0,0))  # if not mapped in the window, then map(displayed) it in the window.

    # define toggle_frame9() method.
    def toggle_frame9(self):
        if self.frame9.winfo_ismapped(): # checks if the specified frame is mapped(displayed) in the window.
            self.frame9.pack_forget() # If True, remove the frame from the window.
        else:
            self.active_frame=[self.frame9] # create a list called "active_frame" and include the frames that need to be mapped in the window.
            self.hide_other_frames(self.active_frame) # call the hide_other_frames() method with the list "active_frame" as it's parameter.
            self.frame9.pack(fill=tk.BOTH, padx=1, pady=(5,0))  # if not mapped in the window, then map(displayed) it in the window.

    # define toggle_frame10() method.
    def toggle_frame10(self):
        if self.frame10.winfo_ismapped():  # checks if the specified frame is mapped(displayed) in the window.
            self.frame10.pack_forget() # If True, remove the frame from the window.
        else:
            self.active_frame=[self.frame10] # create a list called "active_frame" and include the frames that need to be mapped in the window.
            self.hide_other_frames(self.active_frame) # call the hide_other_frames() method with the list "active_frame" as it's parameter.
            self.frame10.pack(fill=tk.BOTH, padx=1, pady=(5,0))  # if not mapped in the window, then map(displayed) it in the window.
 
    # define the hide_other_frames() Method and passes a list called "active_frame".
    def hide_other_frames(self,active_frame):
        # initialize a list with all the frames created for the GUI.
        frames= [self.frame5,self.frame6,self.frame7,self.frame8,self.frame9,self.frame10]
        # iterates through the frames list one by one.
        for frame in frames:
            # checks if the frame is not an element of the list "active_frame"
            if frame not in active_frame:
                frame.pack_forget() # if true make that frame invisible by removing it from the window.

    #--------------------------------------------------------------------------------------------------------------------------------------------------------
    
    # define the add_transaction_from_input() method.
    def add_transaction_from_input(self):
        # Get values from entry widgets
        category_ = self.Add_Category_entry.get() # Retrieve category from the input entry field.
        amount_ = self.Add_amount_entry.get() # Retrieve amount from the input entry field.
        transaction_type_ = self.Add_type_entry.get() # Retrieve transaction type from the input entry field.
        date_ = self.Add_Date_entry.get() # Retrieve date from the input entry field.

        #Call add_transaction method with the input values as parameters
        add_transaction(category_,amount_,transaction_type_,date_ ,self.transactions)
        
        # Generate a new transaction list based on the changes of the transactions dictionary, and Update Treeview table with the new transaction list
        self.transactions_list = gen_transaction_list(self.transactions) # Generate new transaction list.
        self.update_treeview(self.transactions_list) # Update the Treeview table with the new transaction list.



    # define the update_transaction_from_input() method.
    def update_transaction_from_input(self):
        # Retrieve values from entry widgets.
        serial_no = self.upd_serialno_entry.get() # Retrieve serial number from the input entry field.
        amount = self.upd_amount_entry.get() # Retrieve amount from the input entry field.
        transaction_type = self.upd_type_entry.get() # Retrieve transaction type from the input entry field.
        date = self.upd_Date_entry.get() # Retrieve date from the input entry field.

        # Call the update_transaction METHOD with the input values as parameters.
        update_transaction(serial_no, amount, transaction_type, date, self.transactions)

        # Generate a new transaction list based on the changes of the transactions dictionary and Update Treeview table with the new transaction list.
        self.transactions_list = gen_transaction_list(self.transactions) # Generate new transaction list.
        self.update_treeview(self.transactions_list) #  Update the Treeview table with the new transaction list.

    # define the delete_transaction_from_input() method.
    def delete_transaction_from_input(self):
        # Retrieve the value used to identify the transaction to be deleted from the transactions dictionary.
        delete_val= self.del_value_entry.get() # Retrieve delete value from the input entry field.
        # Retrieve the choice of deletion (category / individual deletion using serial number).
        del_by_category= self.var_del_by_category.get() # Retrieve deletion choice from the input entry field.

        # Call delete_transaction method with the input values as parameters.
        del_message = delete_transaction(delete_val,del_by_category,self.transactions)

        # Generate a new transaction list based on the changes of the transactions dictionary and Update Treeview table with the new transaction list.
        self.transactions_list = gen_transaction_list(self.transactions) # Generate new transaction list.
        self.update_treeview(self.transactions_list) # Update the Treeview table with the new transaction list.

        # Update the text of the Label widget
        self.label_14.config(text=del_message) # Update the Label widget text with the deletion message.

    # define the display_summary_transaction() method.
    def display_summary_transaction(self):
        # Call the display_summary METHOD to extract the transactions summary and assign it to the variable "summary_text".
        summary_text= display_summary(self.transactions)

        # Clear previous content in the Text widget.
        self.text_widget.delete(1.0, tk.END)
        
        # Insert the new text into the Text widget.
        self.text_widget.insert(tk.END, summary_text)

    # define the bulk_read_transactions() method.
    def bulk_read_transactions(self):
        # initialize the invalid transaction count.
        invalid_trans=0
        valid_trans=0
        # To handle the instance where the user presses the submit button without selecting a file.
        if not self.filename:
            mbox.showerror("Read transactions in bulks Error", "No file selected") # GUI message to displayed to the user.
            return
        # Assigning the value of self.filename to  variable "filename". 
        filename = self.filename 
        # get number of valid and invalid transactions.
        invalid_trans,valid_trans = read_bulk_transactions_from_file(filename,self.transactions)
        if valid_trans != 0:
            # To display GUI messages  indicating the number of valid transactions.
            mbox.showinfo("Read transactions in bulks",f"{valid_trans} Transactions added successfully, Make sure save changes!")
        else:
            # To display GUI messages indicating that There were no valid transactions.
            mbox.showinfo("Read transactions in bulks","No transactions were added!")

        if invalid_trans !=0:
            # To display messages indicating the number of invalid transactions.
            mbox.showwarning("Read transactions in bulks",f"{invalid_trans} invalid transactions detected!")

        # Generate a new transaction list based on the changes of the transactions dictionary and Update Treeview table with the new transaction list
        self.transactions_list = gen_transaction_list(self.transactions)
        self.update_treeview(self.transactions_list)  

    # define the save_and_quit() method.
    def save_and_quit(self):
        # Invoke the save_transactions method to save the transactions.
        save_transactions(self.transactions)
        
        # Quit the main program.
        self.root.quit() 

    # define the browse_for_file() method.
    def browse_for_file(self):
        '''
        Define file types to allow only text files:
        This variable will be used as an argument specifies the types of files that the file dialog should display to the user.
        Here inside the tuple the first element describes the file type to the user. 
        And second element describes the file extension
        '''
        filetypes_allowed = [('Text files', '*.txt')] 
        
        # Display file dialog and get selected file
        self.filename = filedialog.askopenfilename(filetypes=filetypes_allowed)

        # display the selected file in the label "label_file"
        if self.filename:
            self.label_file.config(text="Selected File: " + self.filename)
        else:
            self.label_file.config(text="No file selected")

    # define the update_treeview() method.
    def update_treeview(self, new_transaction_list):
        # Clear existing items in Treeview.
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert new data from the new transaction_list into the Treeview.
        for transaction in new_transaction_list:
            # insert(), here has no parent so "", values are insert at the end of the list of items("end"), and the values will be individual elements of the transaction_list.
            self.tree.insert("", "end", values=transaction)  

    #------------------------------------------------------------------------------------------------------------------------------------------

    # define the sort_column() method.
    def sort_column(self, col, reverse):
        """
        The line below is a list comprehension that iterates over each child item(row) of the tree widget.
        For each child item,"self.tree.set(child, col)",this method returns the value stored in the specified column for the given child item.
        "child", This part of the tuple simply represents the child item itself.In tkinter each row has an item ID,
        so that is the value extracted here.
        (self.tree.set(child, col), child), this simply creates a tuple including the values and IDs extracted.
        """
        if col == "Amount":  # Check if sorting the amount column.
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


    #---------------------------------------------------------------------------------------------------------------------

    # define the search() method.
    def search(self):
        search_text = self.search_entry.get().lower() #  Get the search text value entered and convert it to lowercase.
        selected_column = self.selected_column.get() # Get the selected column for the search (from the radio button group for column selection).
 
        found = False # initialize the "found" variable as False.

        self.tree.selection_remove(self.tree.selection()) # Removes any selected items before the search.

        for child in self.tree.get_children(""):# Iterate through each row of the tree widget.

            # Retrieves values of the current item (row), and get only the value of the row that represent the selected column(uses index).Then convert the value to lowercase.
            values = str(self.tree.item(child)['values'][self.tree['columns'].index(selected_column)]).lower()# when serial number with leading zero are converted the leading zero is removed.

            # Checks if the column for search is "Serial No." and values are digits.
            if selected_column == "Serial No." and values.isdigit():
                values = values.zfill(4) # Adds a leading Zero for serial number which are less than 4 digits.

            # Checks if the search feature was given a value to search.
            if search_text != "":
                if selected_column == 'Amount': # if the column seleted for search is the Amount column
                    try:
                        search_text =str(float(search_text)) # convert the search text to float and again convert it back to string.
                    except ValueError:
                        found = False # If the value entered for amount search is invalid error message will be displayed.
                # Checks if the search text matches the values.
                if search_text == values:
                    found = True # Assign True as the value of 'found' variable.
                    self.tree.selection_add(child) # Adds the child (row) where the matching value was found as the selection in the treeview. 
                    self.tree.see(child) # scrolls the treeview to make the selected item visible.
            else:
                found = False # if the search button was pressed without any search value, set 'found' to False.
        # Checks if the search was found or not.        
        if not found:
            mbox.showerror("Search", "No matching results found.") #display this message if the search was not found.

    # define the reset() method.
    def reset(self):
        '''
        The line below is used to delete the content of the search entry, here delete() method removes characters from the widget.
        "0" here is the starting index and "end" means the ending index (which is the absolute end).
        ''' 
        self.search_entry.delete(0, 'end')
        '''
        The line below is used to deselect any item selected in the tree widget.
        Here the parameter "self.tree.selection()" create a tuple including IDs of all selected items.
        And the "selection_remove()" method removes the selection from those items,
        this remove the blue highlight given to the selected items.
        '''
        self.tree.selection_remove(self.tree.selection())
        '''
        see() method is used to scroll the treewidget to make the item specified as parameters visible,since the parameter is (''),
        it means that the treewidget will not scrolled to make any item visible.
        '''
        self.tree.see('')

    # define the run() method.
    def run(self):# Method to run the application in the mainloop.
        self.root.mainloop()

# Define main() function.
def main():
    root = tk.Tk() # Create a Tkinter root window.
    app = FinanceTrackerGUI(root) # Create an instance of FinanceTrackerGUI with the root window.
    app.run() # Call the run method of the FinanceTrackerGUI instance to start the application.

# Checks if the code currently being executed is the main program, if so calls the function main().
if __name__ == "__main__":
    main()

# IF you are paid to do this assignment  please delete this line of comment.