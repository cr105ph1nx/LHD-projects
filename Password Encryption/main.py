from tkinter import * # sudo apt install tkinter
from tkinter import ttk
from tkinter import messagebox
from cryptography.fernet import Fernet  # pip install cryptography
import pickle   # pip install pickle
import pyperclip    # pip install pyperclip
from random import seed, randint
import os

# Generate keyfile once with "generate_key()" and hide it in a secure place
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Load key from keyfile
def load_key():
    return open("secret.key", "rb").read()

# Return encrypted password
def encrypt_message(message):
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)

    return(encrypted_message)

# Return decrypted password
def decrypt_message(encrypted_message):
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)

    return(decrypted_message.decode())

def clicked_store():
    website = website_entry_store.get()
    password = password_entry_store.get()
    # Encrypt password
    password = encrypt_message(password)
    # if file doesn't exist, create a new file and record encrypted password
    if(not(os.path.isfile('./passwords.bin'))):
        passwords_file = open("passwords.bin", "wb")
        passwords_dict = {website: password}
        pickle.dump(passwords_dict, passwords_file)
        passwords_file.close()
    else:
        # if file exists and if record already exists, exit with prompt
        passwords_file = open("passwords.bin", "rb")
        passwords_dict = pickle.load(passwords_file)

        if website in passwords_dict:
            messagebox.showinfo('Error', 'Password already stored')
            passwords_file.close()
        else:
        # if record doesn't exist, save record and exit
            passwords_file.close()

            passwords_file = open('passwords.bin', 'wb')
            passwords_dict[website] = password
            pickle.dump(passwords_dict, passwords_file)
            messagebox.showinfo('Success', 'Password stored')
            passwords_file.close()


def clicked_load():
    website = website_entry_load.get()
    # if file doesn't exist, exit with prompt
    if(not(os.path.isfile('./passwords.bin'))):
        messagebox.showinfo('Error', 'No password stored')
    else:
        # if file exists and if website already recorded, retrieve decrypted password
        passwords_file = open("passwords.bin", "rb")
        passwords_dict = pickle.load(passwords_file)

        if website in passwords_dict:
            pyperclip.copy(decrypt_message(passwords_dict[website]))
            messagebox.showinfo('Success', 'Password copied to clipboard')
            passwords_file.close()
        else:
            # if website doesn't exist, exit with prompt
            messagebox.showinfo('Error', 'This password is not stored')
            passwords_file.close()


if __name__ == "__main__":
    # Generate secret key
    if(not(os.path.isfile('./secret.key'))):
        generate_key()
        print("Secret Key generated.")

    # Create window
    window = Tk()
    window.geometry('350x200')
    window.title("Welcome to password manager")

    # Create tabs
    tab_control = ttk.Notebook(window)
    store = ttk.Frame(tab_control)
    load = ttk.Frame(tab_control)

    # Add tabs to tab_control
    tab_control.add(store, text='Store')
    tab_control.add(load, text='Load')

    # Fill tab Store
    website_label_store = Label(store, text="Website :")
    website_label_store.grid(column=0, row=0)

    password_label_store = Label(store, text="Password :")
    password_label_store.grid(column=0, row=1)

    website_entry_store = Entry(store,width=10)
    website_entry_store.grid(column=1, row=0)

    password_entry_store = Entry(store,width=10)
    password_entry_store.grid(column=1, row=1)

    store_btn_store = Button(store, text="Store", command=clicked_store)
    store_btn_store.grid(column=1, row=3)


    # Fill tab Load
    website_label_load = Label(load, text="Website :")
    website_label_load.grid(column=0, row=0)

    website_entry_load = Entry(load,width=10)
    website_entry_load.grid(column=1, row=0)

    store_btn_load = Button(load, text="Load", command=clicked_load)
    store_btn_load.grid(column=1, row=3)

    tab_control.pack(expand=1, fill='both')

    window.mainloop()
