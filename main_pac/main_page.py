import mysql.connector
import time
import hashlib

print("\n*** Welcome to My First Python Project ***")

import mysql.connector

import mysql.connector


def delete_reservation(user_id):
    print("\nIf you want to cancel your reservation, please answer the following questions:(print exit for end)")
    reservation_id = int(input("Reservation ID: "))
    name = input("Reservation name: ")
    last_name = input("Reservation last name: ")

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="test"
    )

    try:
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM time_reservation WHERE id = %s AND name = %s AND lastname = %s AND user_id = %s",
            (reservation_id, name, last_name, user_id)
        )

        if cursor.rowcount > 0:
            print("Reservation has been successfully deleted.")
        else:
            print("No reservation found with the given details.")

        connection.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()
        connection.close()


def show_reservation(user_ID):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="test"
    )
    cursor = connection.cursor()

    try:

        cursor.execute("SELECT * FROM time_reservation WHERE user_id = %s", (user_ID,))
        reservations = cursor.fetchall()

        if reservations:
            print("Reservations:")
            for reservation in reservations:

                print(f"Reservation ID: {reservation[0]}, User ID: {reservation[7]}, Name: {reservation[1]}, "
                      f"Lastname: {reservation[2]}, Username: {reservation[3]}, Phone: {reservation[4]}, "
                      f"Email: {reservation[5]}, Time: {reservation[6]}")
        else:
            print("You don't have any reservations.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()
        connection.close()


def time_reservation_page(user_ID, username, name, lastname, phone, email):
    print(f"\nHello user {user_ID} : {name} {lastname} ## {phone} , {email} , {username}")
    time.sleep(2)

    start_hour = 8
    end_hour = 24

    print("Available Time Slots:")
    for hour in range(start_hour, end_hour):
        time_slot = f"{hour:02}:00 - {hour + 1:02}:00"
        print(f"{hour - start_hour + 1}) {time_slot}")

    while True:
        selected_slot = input("Please select a time slot by number (or type 'exit' to leave): ")
        if selected_slot.lower() == 'exit':
            break

        try:
            selected_slot = int(selected_slot)
            if 1 <= selected_slot <= (end_hour - start_hour):
                reserved_time = f"{start_hour + selected_slot - 1:02}:00 - {start_hour + selected_slot:02}:00"

                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="test"
                )
                cursor = connection.cursor()

                cursor.execute("SELECT * FROM time_reservation WHERE time=%s", (reserved_time,))
                existing_reservation = cursor.fetchone()

                if existing_reservation:
                    print("This time slot is already reserved. Please choose another time slot.")
                else:
                    cursor.execute(
                        "INSERT INTO time_reservation (user_id, name, lastname, username, phone, email, time) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (user_ID, name, lastname, username, phone, email, reserved_time)
                    )
                    connection.commit()
                    print(f"Reservation successful for time slot: {reserved_time}\n")
                    break

                cursor.close()
                connection.close()

            else:
                print("Invalid choice. Please select a valid time slot.")
        except ValueError:
            print("Please enter a valid number.")


def signup_page():
    print(
        "** Welcome to my system **\n\nPlease enter your info: \n##(if your inserted text is (EXit) the program has bin ended)##\n")
    while True:
        name = input("Enter your name: ")
        time.sleep(1.2)
        if name.lower() == "exit":
            break
        lastname = input("Enter your lastname: ")
        time.sleep(1.2)
        if lastname.lower() == "exit":
            break
        email = input("Enter your email: ")
        time.sleep(1.2)
        if email.lower() == "exit":
            break
        phone = input("Enter your phone number: ")
        time.sleep(1.2)
        if phone.lower() == "exit":
            break
        username = input("Enter your username: ")
        time.sleep(1.2)
        if username.lower() == "exit":
            break
        password = input("Enter your password: ")
        time.sleep(1.2)
        if password.lower() == "exit":
            break
        job = input("Enter your job: ")
        time.sleep(1.2)
        if job.lower() == "exit":
            break

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="test"
        )
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE username=%s OR email=%s", (username, email))
        existing_user = cursor.fetchone()

        if existing_user:
            print("Username or Email already exists. Please try again with different credentials.")
            continue
        else:
            cursor.execute(
                "INSERT INTO users (name, lastname, email, phone, username, password, job) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (name, lastname, email, phone, username, hashed_password, job))
            connection.commit()
            print("Signup Successful!\n")
            break

        cursor.close()
        connection.close()


def user_page(username, password):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="test"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    if user:
        print(f"*** Welcome {username} ***")
        time.sleep(2)
        print("\nYour info is: \n")
        print(
            f"ID: {user[1]}**, Name: {user[2]}**, Lastname: {user[3]}**, Phone: {user[5]}**, Email: {user[4]}**, Username: {user[6]}**, Password: {user[0]}**, job: {user[7]}\n")
        show_reservation(user[1])
        time.sleep(2)

        while True:
            choice = input("Do you want to continue? (y/n): ")
            if choice.lower() == "y":
                choice = input(
                    "Enter your choice: \n\t 1) Edit your name \n\t 2) Edit your lastname \n\t 3) Edit your phone \n\t 4) Edit your email \n\t 5) Edit your username \n\t 6) Edit your password \n\t 7) time reservation \n\t 8) delete reservations \n\t 9) Exit\n")

                if choice == "1":
                    new_name = input("Enter your new name: ")
                    cursor.execute("UPDATE users SET name=%s WHERE username=%s", (new_name, username))
                elif choice == "2":
                    new_lastname = input("Enter your new lastname: ")
                    cursor.execute("UPDATE users SET lastname=%s WHERE username=%s", (new_lastname, username))
                elif choice == "3":
                    new_phone = input("Enter your new phone: ")
                    cursor.execute("UPDATE users SET phone=%s WHERE username=%s", (new_phone, username))
                elif choice == "4":
                    new_email = input("Enter your new email: ")
                    cursor.execute("UPDATE users SET email=%s WHERE username=%s", (new_email, username))
                elif choice == "5":
                    new_username = input("Enter your new username: ")
                    cursor.execute("UPDATE users SET username=%s WHERE username=%s", (new_username, username))
                    username = new_username
                elif choice == "6":
                    new_password = input("Enter your new password: ")
                    cursor.execute("UPDATE users SET password=%s WHERE username=%s", (new_password, username))
                    password = new_password
                elif choice == "7":
                    time_reservation_page(user_ID=user[1], username=user[6], name=user[2], lastname=user[3],
                                          phone=user[5], email=user[4])
                elif choice == "8":
                    show_reservation(user[1])
                    delete_reservation(user[1])
                elif choice == "9":
                    break

                connection.commit()
                print("Your information has been updated successfully!\n")
            elif choice.lower() == "n":
                break
    else:
        print("User not found.")
    cursor.close()
    connection.close()


while True:
    choice = int(input("\nPlease enter your choice: \n\t 1) Login \n\t 2) Signup \n\t 3) Exit\n"))

    if choice == 1:
        print("** Welcome back to my system **")
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="test"
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            user = cursor.fetchone()
            if user:
                print("Login Successful")
                user_page(username, password)
            else:
                print("Login Failed: Incorrect username or password.")
            cursor.close()
        connection.close()

    elif choice == 2:
        signup_page()

    elif choice == 3:
        print("Exiting the system. Goodbye!")
        break

    else:
        print("Invalid choice, please try again.")


# sadra ghofran