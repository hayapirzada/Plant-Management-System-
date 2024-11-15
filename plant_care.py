import sqlite3



def db():
    # connect to sqlite
    # connection to object
    connection_obj = sqlite3.connect('plant.db')

    # cursor object
    cursor_obj = connection_obj.cursor()


    # cursor_obj.execute("DROP TABLE IF EXISTS PLANT")
    # cursor_obj.execute("DROP TABLE IF EXISTS USERS")


    # create users table only if it doesn't exist
    table1 = """CREATE TABLE IF NOT EXISTS USERS (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE,
                            password TEXT
                        );"""
    cursor_obj.execute(table1)

    # Create plant table only if it doesn't exist
    table2 = """CREATE TABLE IF NOT EXISTS PLANT (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        watering_freq INTEGER,
                        last_watered DATE,
                        health TEXT,
                        reminder TEXT,
                        user_id INTEGER,
                        FOREIGN KEY (user_id) REFERENCES USERS(id)
                    );"""
    cursor_obj.execute(table2)
    print("Tables are Ready")

    # close connection
    connection_obj.close()

def register():
    # ask for user input
    username = input("Enter a username: ")
    password = input("Enter a password: ")

    # connect to db
    conn = sqlite3.connect('plant.db')
    cursor = conn.cursor()

    # Check if the username already exists
    cursor.execute("SELECT * FROM USERS WHERE username = ?", (username,))
    if cursor.fetchone():
        print("Username already exists. Please choose a different username.")
    else:
        # Queries to insert
        cursor.execute('''INSERT INTO USERS (username, password) VALUES (?, ?)
            ''', (username, password))

    # commit changes
    # close connection
    conn.commit()
    conn.close()
    print("registered successfully")



def login():
    # ask for user input
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # connect db
    conn = sqlite3.connect('plant.db')
    cursor = conn.cursor()

    cursor.execute('''
            SELECT id FROM USERS WHERE username = ? AND password = ?
        ''', (username, password))
    user = cursor.fetchone()

    # close connection
    conn.close()

    if user:
        # return user id
        return user[0]
    else:
        print("Invalid credentials")
        return None


def add_plant(user_id):
    # ask user input
    name = input("Enter plant's name: ")
    watering_freq = int(input("Enter watering_freq (Days): "))
    last_watered = input("Enter last watered date (MM/DD/YYYY): ")
    health = input("Enter plant's health (bad, good, excellent): ")
    reminder = input("Enter any notes: ")

    # connect to db
    conn = sqlite3.connect('plant.db')
    cursor = conn.cursor()

    # Queries to insert
    cursor.execute('''INSERT INTO PLANT (name, watering_freq, last_watered, health, reminder, user_id) VALUES 
    (?, ?, ?, ?, ?, ?)
     ''', (name, watering_freq, last_watered, health, reminder, user_id))

    print("Data entered success")

    # commit changes in db
    # close connection
    conn.commit()
    conn.close()


def view_plants(user_id):
    # connect to db
    conn = sqlite3.connect('plant.db')
    cursor = conn.cursor()

    # Display plants for the logged-in user
    cursor.execute('''
           SELECT * FROM PLANT WHERE user_id = ?
       ''', (user_id,))
    plants = cursor.fetchall()

    if plants:
        print("Your plants: ")
        for plant in plants:
            print(plant)
    else:
        print("You have no plants")

    conn.close()

def water_plant(user_id):
    # id number and date of watering from user
    plant_id = int(input("Enter plant ID # to water: "))
    date_today = input("Enter today's date (MM/DD/YYYY): ")

    # connect to db
    conn = sqlite3.connect('plant.db')
    cursor = conn.cursor()

    # update last_watered
    cursor.execute('''
        UPDATE PLANT
        SET last_watered = ?
        WHERE id = ? AND user_id = ?
    ''', (date_today, plant_id, user_id))

    conn.commit()
    conn.close()
    print("plant watered")

def update_health(user_id):
    # id number and date of watering from user
    plant_id = int(input("Enter plant ID #: "))
    new_health = input("Enter plant's health (bad, good, excellent): ")

    # connect to db
    conn = sqlite3.connect('plant.db')
    cursor = conn.cursor()

    # update health
    cursor.execute('''
           UPDATE PLANT
           SET health = ?
           WHERE id = ? AND user_id = ?
       ''', (new_health, plant_id, user_id))

    conn.commit()
    conn.close()
    print("plant health updated")

def delete_data():
    # ask user input
    plant_id = int(input("Enter plant's id #: "))

    # connect to db
    conn = sqlite3.connect('plant.db')
    cursor = conn.cursor()

    # delete
    cursor.execute('''
            DELETE FROM PLANT WHERE id = ?
        ''', (plant_id,))

    # commit changes
    conn.commit()

    # Check if any rows were affected (i.e., if the 'delete' was successful)
    if cursor.rowcount > 0:
        print(f"Plant with ID {plant_id} deleted successfully.")
    else:
        print(f"No plant found with ID {plant_id}.")

    # close connection
    conn.close()

def main():
    db()
    # check_user_table()
    user_id = None
    while True:
        print("Welcome to plant care")
        # user authentication
        print("1. register")
        print("2. login")
        print("3. EXIT")

        # ask for user input
        choice1 = input("Enter your choice [1-3]: ")

        # if/else to go through choices
        if choice1 == "1":
            register()
        elif choice1 == "2":
            user_id = login()
            if user_id:
                print("Login successful!")
            else:
                print("Login failed")
        elif choice1 == "3":
            break
        else:
            print("Invalid choice")


        # plant management
        if user_id:
            while True:
                print("1. Add a new plant")
                print("2. View my plants")
                print("3. Water my plant")
                print("4. UPDATE health")
                print("5. delete data")
                print("6. EXIT")

                # ask for user input
                choice2 = input("Enter your choice [1-6]: ")

                # if/else to go through choices
                if choice2 == "1":
                    add_plant(user_id)
                elif choice2 == "2":
                    view_plants(user_id)
                elif choice2 == "3":
                    water_plant(user_id)
                elif choice2 == "4":
                    update_health(user_id)
                elif choice2 == "5":
                    delete_data()
                elif choice2 == "6":
                    user_id = None
                    print("logout successful")
                    break
                else:
                    print("INVALID CHOICE, TRY AGAIN")


main()
