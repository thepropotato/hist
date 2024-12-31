import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from upload import *
from HiSt import *
from images import bg_image as bg2
from images import refresh as refresh2
from images import upload_file as upload_file2
from images import upload_folder as upload_folder2
from images import upload_password as upload_password2
from images import download_file as download_file2
from images import download_folder as download_folder2
from images import delete_file as delete_file2
from images import delete_folder as delete_folder2
from images import delete_password as delete_password2
from images import view_password as view_password2
from images import remove_acc as remove_acc2
import io
import os
import sys

s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

def page2(username, password):
    
    def on_upload_file_click(username, password, s3):
        hist_log_textbox.delete(1.0, tk.END)
        hist_log_textbox.insert(tk.END, "Encrypting and Uploading Data...")
        out = upload_file_gui(username, password, s3)
        hist_log_textbox.delete(1.0, tk.END)
        hist_log_textbox.insert(tk.END, f"{out}\n\n")
        
    def on_upload_folder_click(username, password, s3):
        hist_log_textbox.delete(1.0, tk.END)
        hist_log_textbox.insert(tk.END, "Encrypting and Uploading Data...")
        out = upload_folder_gui(username, password, s3)
        hist_log_textbox.delete(1.0, tk.END)
        hist_log_textbox.insert(tk.END, f"{out}\n\n")
    
    def on_upload_password_click():
        # Create a new window for password upload
        upload_password_window = tk.Toplevel(main_window)
        upload_password_window.title("Upload Password")

        # Application Name Entry
        app_name_label = tk.Label(upload_password_window, text="Application Name :")
        app_name_label.grid(row=0, column=0, padx=10, pady=10)
        app_name_entry = tk.Entry(upload_password_window)
        app_name_entry.grid(row=0, column=1, padx=10, pady=10)

        # Username Entry
        username_label = tk.Label(upload_password_window, text="Username :")
        username_label.grid(row=1, column=0, padx=10, pady=10)
        username_entry = tk.Entry(upload_password_window)
        username_entry.grid(row=1, column=1, padx=10, pady=10)

        # Password Entry
        password_label = tk.Label(upload_password_window, text="Password :")
        password_label.grid(row=2, column=0, padx=10, pady=10)
        password_entry = tk.Entry(upload_password_window)
        password_entry.grid(row=2, column=1, padx=10, pady=10)
        
        # Upload Button
        def on_upload_password_button_click():
            # Get the values from the entries
            app_name = app_name_entry.get()
            uname = username_entry.get()
            pword = password_entry.get()

            # Call your upload function with the obtained values
            #upload_function(app_name, username, password)
            hist_log_textbox.delete(1.0, tk.END)
            hist_log_textbox.insert(tk.END, "Encrypting and Uploading Data...")
            
            out = upload_password_gui(username, password, s3, app_name, uname, pword)
            
            hist_log_textbox.delete(1.0, tk.END)
            hist_log_textbox.insert(tk.END, f"{out}\n\n")

            # Close the upload password window
            upload_password_window.destroy()


        upload_button = tk.Button(upload_password_window, text="Upload", command=on_upload_password_button_click)
        upload_button.grid(row=3, column=0, columnspan=2, pady=10)
        
    def on_download_file_click():
        # Create a new window for password upload
        download_file_window = tk.Toplevel(main_window)
        download_file_window.title("Download File")

        # Application Name Entry
        file_name_label = tk.Label(download_file_window, text="Enter the File Name :")
        file_name_label.grid(row=0, column=0, padx=10, pady=10)
        file_name_entry = tk.Entry(download_file_window)
        file_name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Upload Button
        def on_download_file_button_click():
            # Get the values from the entries
            filename = file_name_entry.get()

            hist_log_textbox.delete(1.0, tk.END)
            hist_log_textbox.insert(tk.END, "Decrypting and Downloading Data...")
            
            # Call your upload function with the obtained values
            #upload_function(app_name, username, password)
            out = download_file_gui(username, password, s3, filename)
            
            hist_log_textbox.delete(1.0, tk.END)
            hist_log_textbox.insert(tk.END, f"{out}\n\n")

            # Close the upload password window
            download_file_window.destroy()

        download_button = tk.Button(download_file_window, text="Download File", command=on_download_file_button_click)
        download_button.grid(row=3, column=0, columnspan=2, pady=10)
        
    def on_download_folder_click():
        # Create a new window for password upload
        download_folder_window = tk.Toplevel(main_window)
        download_folder_window.title("Download Folder")

        # Application Name Entry
        folder_name_label = tk.Label(download_folder_window, text="Enter the Folder Name :")
        folder_name_label.grid(row=0, column=0, padx=10, pady=10)
        folder_name_entry = tk.Entry(download_folder_window)
        folder_name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Upload Button
        def on_download_folder_button_click():
            # Get the values from the entries
            foldername = folder_name_entry.get()

            hist_log_textbox.delete(1.0, tk.END)
            hist_log_textbox.insert(tk.END, "Decrypting and Downloading Data...")
            
            # Call your upload function with the obtained values
            #upload_function(app_name, username, password)
            out = download_folder_gui(username, password, s3, foldername)
            
            hist_log_textbox.delete(1.0, tk.END)
            hist_log_textbox.insert(tk.END, f"{out}\n\n")

            # Close the upload password window
            download_folder_window.destroy()

        download_button = tk.Button(download_folder_window, text="Download Folder", command=on_download_folder_button_click)
        download_button.grid(row=3, column=0, columnspan=2, pady=10)
        
    def on_download_password_click():
        # Create a new window for password upload
        download_password_window = tk.Toplevel(main_window)
        download_password_window.title("View Password")

        # Application Name Entry
        app_name_label = tk.Label(download_password_window, text="Enter the Application Name :")
        app_name_label.grid(row=0, column=0, padx=10, pady=10)
        app_name_entry = tk.Entry(download_password_window)
        app_name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Upload Button
        def on_download_password_button_click():
            # Get the values from the entries
            appname = app_name_entry.get()

            # Call your upload function with the obtained values
            #upload_function(app_name, username, password)
            download_password_gui(username, appname, password, s3)

            # Close the upload password window
            download_password_window.destroy()

        download_button = tk.Button(download_password_window, text="View Password", command=on_download_password_button_click)
        download_button.grid(row=3, column=0, columnspan=2, pady=10)
        
    def on_delete_file_click():
        # Create a new window for password upload
        delete_file_window = tk.Toplevel(main_window)
        delete_file_window.title("Delete File")

        # Application Name Entry
        file_name_label = tk.Label(delete_file_window, text="Enter the File Name :")
        file_name_label.grid(row=0, column=0, padx=10, pady=10)
        file_name_entry = tk.Entry(delete_file_window)
        file_name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Upload Button
        def on_delete_file_button_click():
            # Get the values from the entries
            filename = file_name_entry.get()
            
            hist_log_textbox.delete(1.0, tk.END)
            hist_log_textbox.insert(tk.END, "Deleting Data...")

            # Call your upload function with the obtained values
            #upload_function(app_name, username, password)
            out = deletefile(username, filename, s3)
            
            hist_log_textbox.delete(1.0, tk.END)
            hist_log_textbox.insert(tk.END, f"{out}\n\n")

            # Close the upload password window
            delete_file_window.destroy()

        delete_button = tk.Button(delete_file_window, text="Delete File", command=on_delete_file_button_click)
        delete_button.grid(row=3, column=0, columnspan=2, pady=10)
        
    def on_delete_folder_click():
        # Create a new window for password upload
        delete_folder_window = tk.Toplevel(main_window)
        delete_folder_window.title("Delete Folder")

        # Application Name Entry
        folder_name_label = tk.Label(delete_folder_window, text="Enter the Folder Name :")
        folder_name_label.grid(row=0, column=0, padx=10, pady=10)
        folder_name_entry = tk.Entry(delete_folder_window)
        folder_name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Upload Button
        def on_delete_folder_button_click():
            # Get the values from the entries
            foldername = folder_name_entry.get()

            hist_log_textbox.delete(1.0, tk.END)
            hist_log_textbox.insert(tk.END, "Deleting Data...")
            # Call your upload function with the obtained values
            #upload_function(app_name, username, password)
            out = deletefolder(username, foldername, s3)
            
            hist_log_textbox.delete(1.0, tk.END)
            hist_log_textbox.insert(tk.END, f"{out}\n\n")

            # Close the upload password window
            delete_folder_window.destroy()
            
        delete_button = tk.Button(delete_folder_window, text="Delete Folder", command=on_delete_folder_button_click)
        delete_button.grid(row=3, column=0, columnspan=2, pady=10)
        
    def on_delete_password_click():
        # Create a new window for password upload
        delete_password_window = tk.Toplevel(main_window)
        delete_password_window.title("Delete Password")

        # Application Name Entry
        app_name_label = tk.Label(delete_password_window, text="Enter the Application Name :")
        app_name_label.grid(row=0, column=0, padx=10, pady=10)
        app_name_entry = tk.Entry(delete_password_window)
        app_name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Upload Button
        def on_delete_password_button_click():
            # Get the values from the entries
            webname = app_name_entry.get()

            hist_log_textbox.delete(1.0, tk.END)
            hist_log_textbox.insert(tk.END, "Deleting Data...")
            # Call your upload function with the obtained values
            #upload_function(app_name, username, password)
            out = deletepass(username, webname, s3)
            hist_log_textbox.delete(1.0, tk.END)
            hist_log_textbox.insert(tk.END, f"{out}\n\n")

            # Close the upload password window
            delete_password_window.destroy()
            
        delete_button = tk.Button(delete_password_window, text="Delete Password", command=on_delete_password_button_click)
        delete_button.grid(row=3, column=0, columnspan=2, pady=10)
    
    # Create a function to handle the power symbol icon click
    def on_power_symbol_click():
        # Create a new window for password upload
        delete_account_window = tk.Toplevel(main_window)
        delete_account_window.title("Delete HiSt Account")

        # Application Name Entry
        app_name_label = tk.Label(delete_account_window, text="Enter the Password :")
        app_name_label.grid(row=0, column=0, padx=10, pady=10)
        app_name_entry = tk.Entry(delete_account_window)
        app_name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Upload Button
        def on_delete_account_button_click():
            # Get the values from the entries
            pword = app_name_entry.get()

            # Call your upload function with the obtained values
            #upload_function(app_name, username, password)
            out = deleteuser_gui(username, s3, pword)
            
            hist_log_textbox.delete(1.0, tk.END)
            hist_log_textbox.insert(tk.END, f"{out}\n\n")
            
            if "Exiting HiSt" in out :
                hist_log_textbox.delete(1.0, tk.END)
                hist_log_textbox.insert(tk.END, "Account deleted. Exiting HiSt in 5 seconds.")
                main_window.destroy()

            # Close the upload password window
            delete_account_window.destroy()
            
        delete_button = tk.Button(delete_account_window, text="Delete Account", command=on_delete_account_button_click)
        delete_button.grid(row=3, column=0, columnspan=2, pady=10)

    # Create a function to handle the refresh button click
    def on_refresh_click():
        # Implement the refresh functionality here
        r1, r2, r3 = getstuff(username, s3) # Replace this with the actual output
        
        result = str(printstuff_gui(r1, r2, r3))
        
        # Clear existing text and insert the new content
        your_stuff_textbox.config(state=tk.NORMAL)  # Allow modifications
        your_stuff_textbox.delete(1.0, tk.END)  # Clear existing text
        your_stuff_textbox.insert(tk.END, result)  # Insert new content
        your_stuff_textbox.config(state=tk.DISABLED)  # Set back to read-only

    # Create the main window
    main_window = tk.Tk()
    main_window.title("HiSt - Hide Stuff")

    # Set the window to full screen
    main_window.attributes('-fullscreen', True)

    # Set the font style for the entire GUI
    font_style = ("Arial", 12)  # Replace with your preferred font name and size

    # Load background image without zooming
    bg_image = Image.open(io.BytesIO(base64.b64decode(bg2)))  # Replace with your image path
    bg_image = bg_image.resize((main_window.winfo_screenwidth(), main_window.winfo_screenheight()), Image.LANCZOS)
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(main_window, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)

    # Create tabs
    notebook = ttk.Notebook(main_window)
    style = ttk.Style()
    style.configure("TNotebook.Tab", font=("Arial", 12), background="black")  # Set the tab header background color

    # Your Stuff Tab
    your_stuff_tab = ttk.Frame(notebook)
    notebook.add(your_stuff_tab, text="   Your Stuff   ")  # Rename the tab here

    # Refresh Button
    refresh_image = Image.open(io.BytesIO(base64.b64decode(refresh2)))  # Replace with your image path
    refresh_image = refresh_image.resize((50, 50), Image.BICUBIC)  # Resize the image
    refresh_image = ImageTk.PhotoImage(refresh_image)

    # Create the Refresh Button
    refresh_button = tk.Button(your_stuff_tab, image=refresh_image, command=on_refresh_click, bd=0, relief=tk.FLAT, highlightthickness=0)  # Set relief to FLAT
    refresh_button.image = refresh_image
    refresh_button.place(x=753, y=0)  # Adjust the placement as needed

    # "Your Stuff" Textbox
    your_stuff_label = tk.Label(your_stuff_tab, text="Find Your Stuff, "+ username + " !", font=("Arial", 16))  # You can adjust the font and size
    your_stuff_label.pack(pady=(20, 10))

    your_stuff_textbox = tk.Text(your_stuff_tab, height=33, width=98, wrap=tk.WORD, state=tk.DISABLED)  # Set initially as read-only
    your_stuff_textbox.pack(padx=20, pady=(0, 20))

    # "HiSt Log" Textbox
    hist_log_textbox = tk.Text(main_window, height=5, width=90, wrap=tk.WORD)
    hist_log_textbox.place(x=650, y=50)  # Adjust the position as needed

    # Buttons Tab
    buttons_tab = ttk.Frame(notebook)
    notebook.add(buttons_tab, text="   Menu   ")  # Rename the tab here

    # Upload File Button
    upload_file_image = Image.open(io.BytesIO(base64.b64decode(upload_file2)))
    upload_file_image = upload_file_image.resize((160, 160), Image.BICUBIC)
    upload_file_image = ImageTk.PhotoImage(upload_file_image)
    upload_file_button = tk.Button(buttons_tab, image=upload_file_image, bd=0, relief=tk.FLAT, highlightthickness=0, command=lambda: on_upload_file_click(username, password, s3))
    upload_file_button.image = upload_file_image
    upload_file_button.place(x=75, y=25)  # Adjust the placement as needed

    # Upload Folder Button
    upload_folder_image = Image.open(io.BytesIO(base64.b64decode(upload_folder2)))
    upload_folder_image = upload_folder_image.resize((160, 160), Image.BICUBIC)
    upload_folder_image = ImageTk.PhotoImage(upload_folder_image)
    upload_folder_button = tk.Button(buttons_tab, image=upload_folder_image, bd=0, relief=tk.FLAT, highlightthickness=0, command=lambda: on_upload_folder_click(username, password, s3))
    upload_folder_button.image = upload_folder_image
    upload_folder_button.place(x=335, y=25)  # Adjust the placement as needed

    # Upload Password Button
    upload_password_image = Image.open(io.BytesIO(base64.b64decode(upload_folder2)))
    upload_password_image = upload_password_image.resize((160, 160), Image.BICUBIC)
    upload_password_image = ImageTk.PhotoImage(upload_password_image)
    upload_password_button = tk.Button(buttons_tab, image=upload_password_image, bd=0, relief=tk.FLAT, highlightthickness=0, command=lambda : on_upload_password_click())
    upload_password_button.image = upload_password_image
    upload_password_button.place(x=595, y=25)  # Adjust the placement as needed

    # Download File Button
    download_file_image = Image.open(io.BytesIO(base64.b64decode(download_file2)))
    download_file_image = download_file_image.resize((160, 160), Image.BICUBIC)
    download_file_image = ImageTk.PhotoImage(download_file_image)
    download_file_button = tk.Button(buttons_tab, image=download_file_image, bd=0, relief=tk.FLAT, highlightthickness=0, command=lambda : on_download_file_click())
    download_file_button.image = download_file_image
    download_file_button.place(x=75, y=225)  # Adjust the placement as needed

    # Download Folder Button
    download_folder_image = Image.open(io.BytesIO(base64.b64decode(download_folder2)))
    download_folder_image = download_folder_image.resize((160, 160), Image.BICUBIC)
    download_folder_image = ImageTk.PhotoImage(download_folder_image)
    download_folder_button = tk.Button(buttons_tab, image=download_folder_image, bd=0, relief=tk.FLAT, highlightthickness=0, command=lambda : on_download_folder_click())
    download_folder_button.image = download_folder_image
    download_folder_button.place(x=335, y=225)  # Adjust the placement as needed

    # View Password Button
    view_password_image = Image.open(io.BytesIO(base64.b64decode(view_password2)))
    view_password_image = view_password_image.resize((160, 160), Image.BICUBIC)
    view_password_image = ImageTk.PhotoImage(view_password_image)
    view_password_button = tk.Button(buttons_tab, image=view_password_image, bd=0, relief=tk.FLAT, highlightthickness=0, command=lambda : on_download_password_click())
    view_password_button.image = view_password_image
    view_password_button.place(x=595, y=225)  # Adjust the placement as needed

    # Delete File Button
    delete_file_image = Image.open(io.BytesIO(base64.b64decode(delete_file2)))
    delete_file_image = delete_file_image.resize((160, 160), Image.BICUBIC)
    delete_file_image = ImageTk.PhotoImage(delete_file_image)
    delete_file_button = tk.Button(buttons_tab, image=delete_file_image, bd=0, relief=tk.FLAT, highlightthickness=0, command=lambda : on_delete_file_click())
    delete_file_button.image = delete_file_image
    delete_file_button.place(x=75, y=425)  # Adjust the placement as needed

    # Delete Folder Button
    delete_folder_image = Image.open(io.BytesIO(base64.b64decode(delete_folder2)))
    delete_folder_image = delete_folder_image.resize((160, 160), Image.BICUBIC)
    delete_folder_image = ImageTk.PhotoImage(delete_folder_image)
    delete_folder_button = tk.Button(buttons_tab, image=delete_folder_image, bd=0, relief=tk.FLAT, highlightthickness=0, command=lambda : on_delete_folder_click())
    delete_folder_button.image = delete_folder_image
    delete_folder_button.place(x=335, y=425)  # Adjust the placement as needed

    # Delete Password Button
    delete_password_image = Image.open(io.BytesIO(base64.b64decode(delete_password2)))
    delete_password_image = delete_password_image.resize((160, 160), Image.BICUBIC)
    delete_password_image = ImageTk.PhotoImage(delete_password_image)
    delete_password_button = tk.Button(buttons_tab, image=delete_password_image, bd=0, relief=tk.FLAT, highlightthickness=0, command=lambda : on_delete_password_click())
    delete_password_button.image = delete_password_image
    delete_password_button.place(x=595, y=425)  # Adjust the placement as needed

    # Power Symbol Icon
    power_symbol_image = Image.open(io.BytesIO(base64.b64decode(remove_acc2)))  # Replace with your image path
    power_symbol_image = power_symbol_image.resize((60, 60), Image.BICUBIC)  # Resize the image
    power_symbol_image = ImageTk.PhotoImage(power_symbol_image)
    power_symbol_button = tk.Button(main_window, image=power_symbol_image, command=on_power_symbol_click, bd=0, relief=tk.FLAT, highlightthickness=0)  # Set relief to FLAT
    power_symbol_button.image = power_symbol_image
    power_symbol_button.place(x=main_window.winfo_screenwidth() - 135, y=60)

    # Place the whole 3-tab box at specified coordinates (adjust as needed)
    notebook.place(x=650, y=170)

    # Run the main loop
    main_window.mainloop()

# Call the function to run the GUI