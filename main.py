from tkinter import *
from tkinter import messagebox
import datetime
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
#Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []

    #generate a random letters , symbols and number list
    letters_list = [ random.choice(letters) for _ in range(random.randint(8, 10)) ]
    symbols_list = [ random.choice(symbols) for _ in range(random.randint(2, 4)) ]
    number_list = [ random.choice(numbers) for _ in range(random.randint(2, 4)) ]

    #concatinate the generated random letter , symbols and number.
    #shuffle the list and join to create a random password.
    password_list = letters_list + symbols_list + number_list 
    random.shuffle(password_list)
    password = "".join(password_list) 

    # print(f"Your password is: {password}") # for testing purposes only.
    #add and show the generated password in password entry text box.
    password_entry.insert(0, password)
    #save generated password in clipboard
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    #get the data in the field.
    website = website_entry.get()
    email = email_username_entry.get()
    password = password_entry.get()
    new_data = {
        website.title() : {
            "email": email,
            "password": password,
            "date_created": formatted_date,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="Warning", message="Please don't leave any field blank")
    else:
        # write the data into the file.
        try:
            with open("data.json", "r") as data_file:
                #Reading old data.
                data = json.load(data_file) 
        except FileNotFoundError:
            #if json file not existing, create it
            print("No Data file found / existing.")
            print("Creating json file..")
            with open("data.json", "w") as data_file:
                #Saving updated data.
                json.dump(new_data, data_file, indent=4)
        else:
            #update password of existing website 
            current_password = data[website.title()]['password']

            #check if password is already used or not updated the password to new password.
            if password != current_password:
                is_yes = messagebox.askyesno(title="Update", message="Would you like to update your password?")

                if is_yes:
                    #Updating old data with new data.
                    data.update(new_data)
                    with open("data.json", "w") as data_file:
                        #Saving updated data.
                        json.dump(data, data_file, indent=4)

            else:
                messagebox.showwarning(title="Update", message="Password already used from the past. Please use a different password.") 
                clear()



        finally:
            #use the clear function.
            clear()


def clear():
    #CLEAR ALL Data in the field.
    website_entry.delete(0,"end")
    password_entry.delete(0,"end")
    website_entry.focus()


def find_password():
    #get the website name 
    website = website_entry.get().title()
    
    #check if the json file exist if not show error message and create a json file.
    #if json file exist get the email and password information and return in messagebox if not show error message
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)

    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")
        save()
    else:
        if website in data:
            email = data[website]['email']
            password = data[website]['password']
            messagebox.showinfo(title=f"{website.title()}", message=f"Email:{email}\nPassword:{password}")
        else:
            messagebox.showinfo(title="Error", message="Website does not exist")





# ---------------------------- UI SETUP ------------------------------- #
#Main window for tkinter 
window = Tk()
window.title("Oath Keeper Password Manager")
window.config(padx=20,pady=20)

#Main for application logo and picture.
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="C:\RaymartFiles\Learning\Python\projects\TKinter\password-manager-start\oath_keeper.png")
canvas.create_image(50, 100, image=logo_img)
canvas.create_text(150, 100, text="Oath-Keeper", font=("Arial", 9, "bold"))
canvas.create_text(150, 120, text="Safe and Secure", font=("Arial", 9, "bold"))
canvas.grid(row=0,column=0, columnspan=2)

# Formatting dates and times
now = datetime.datetime.now()
formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")

#label 
website_label = Label(text="Website:")
website_label.grid(row=1,column=0)
email_username_label = Label(text="Email/Username:")
email_username_label.grid(row=2,column=0)
paassword_label = Label(text="Password:")
paassword_label.grid(row=3,column=0)

#entries 
website_entry = Entry(width=17)
website_entry.grid(row=1, column=1)
website_entry.focus()

email_username_entry = Entry(width=35)
email_username_entry.grid(row=2, column=1, columnspan=2)
email_username_entry.insert(0, "raymart.orbita@gmail.com")


password_entry = Entry(width=17)
password_entry.grid(row=3, column=1)


#button
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=30, command=save)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(row=1, column=2)







window.mainloop()



