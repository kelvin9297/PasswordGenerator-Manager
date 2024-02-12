from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
               's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
               'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_input.get().lower()
    email_username = email_username_input.get().lower()
    password = password_input.get()
    new_data = {
        website: {
            "email": email_username,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", mode="r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", mode="w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_input.delete(0, END)
            password_input.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_input.get().lower()
    try:
        with open("data.json", mode="r") as data_file:
            # Reading old data
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message=f"No details for {website} exists")
    except json.decoder.JSONDecodeError:
        messagebox.showinfo(title="Error", message=f"No matching results found in the database")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=f"{website.title()}",
                                message=f"email: {email}\n "
                                        f"password: {password}\n"
                                        f"Your password has been copied.")
            pyperclip.copy(data[website]['password'])
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists")
    finally:
        website_input.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Lock Image
canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

# texts
website_text = Label(text="Website:")
website_text.grid(column=0, row=1)
email_username_text = Label(text="Email/Username:")
email_username_text.grid(column=0, row=2)
password_text = Label(text="Password:")
password_text.grid(column=0, row=3)

# input bars
website_input = Entry(width=19)
website_input.grid(column=1, row=1)
website_input.focus()
website_input.get()
email_username_input = Entry(width=35)
email_username_input.grid(column=1, columnspan=2, row=2)
email_username_input.insert(0, "dummy@email.com")
email_username_input.get()
password_input = Entry(width=19)
password_input.grid(column=1, row=3)
password_input.get()

# buttons
generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(column=2, row=3)

add_button = Button(text="Add", width=35, command=save)
add_button.grid(column=1, columnspan=2, row=4)

search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(column=2, row=1)

window.mainloop()
