import mysql.connector

try:
    def connect_to_database():
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="anandhu",
            database="Travelitineraryplanner"
        )
        return mydb

    def create_destinations_table(cursor):
        cursor.execute("CREATE TABLE IF NOT EXISTS Destinations (ID INT NOT NULL,name VARCHAR(255) NOT NULL,description TEXT,PRIMARY KEY(ID))")

    def create_activities_table(cursor):
        cursor.execute("CREATE TABLE IF NOT EXISTS Activities (id INT NOT NULL,destination_id INT,name VARCHAR(255) NOT NULL,date DATE,time TIME,notes TEXT,PRIMARY KEY(ID),FOREIGN KEY (destination_id) REFERENCES Destinations (id))")

except Exception as e:
    print("DB ALREADY EXISTS!!!!!!!!!")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="anandhu",
        database="Travelitineraryplanner"
    )

    cursor = mydb.cursor()

def add_destination(cursor, name, description):
    cursor.execute('INSERT INTO Destinations (name, description) VALUES (%s, %s)', (name, description))

def add_activity(cursor, destination_id, name, date, time, notes):
    cursor.execute('''
        INSERT INTO Activities (destination_id, name, date, time, notes)
        VALUES (%s, %s, %s, %s, %s)
    ''', (destination_id, name, date, time, notes))

def get_itinerary(cursor, destination_id):
    cursor.execute('''
        SELECT Destinations.name as destination, Activities.name as activity, date, time, notes
        FROM Activities
        JOIN Destinations ON Activities.destination_id = Destinations.id
        WHERE Destinations.id = %s
    ''', (destination_id,))
    return cursor.fetchall()

def delete_destination(cursor, connection, destination_name):
    cursor.execute('DELETE FROM Destinations WHERE name = %s', (destination_name,))
    connection.commit()
    print("Destination deleted successfully!")

def display_destinations(cursor):
    cursor.execute('SELECT * FROM Destinations')
    destinations = cursor.fetchall()
    print("\nDestinations:")
    for destination in destinations:
        print(destination)

def main():
    connection = None
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        create_destinations_table(cursor)
        create_activities_table(cursor)

        while True:
            print("\nTravel Itinerary Planner")
            print("1. Add Destination")
            print("2. Add Activity")
            print("3. View Itinerary")
            print("4. Delete Destination")
            print("5. Display Destinations")
            print("6. Exit")

            choice = input("Enter your choice (1/2/3/4/5/6): ")

            if choice == '1':
                name = input("Enter destination name: ")
                description = input("Enter destination description: ")
                add_destination(cursor, name, description)
                connection.commit()
                print("Destination added successfully!")

            elif choice == '2':
                destination_id = int(input("Enter destination ID: "))
                name = input("Enter activity name: ")
                date = input("Enter date (YYYY-MM-DD): ")
                time = input("Enter time (HH:MM): ")
                notes = input("Enter notes: ")
                add_activity(cursor, destination_id, name, date, time, notes)
                connection.commit()
                print("Activity added successfully!")

            elif choice == '3':
                destination_id = int(input("Enter destination ID: "))
                itinerary = get_itinerary(cursor, destination_id)
                print("\nItinerary for Destination ID", destination_id)
                for item in itinerary:
                    print(item)

            elif choice == '4':
                print("Deletion")
                destination_name = input("Enter destination name:")
                delete_destination(cursor, connection, destination_name)

            elif choice == '5':
                display_destinations(cursor)

            elif choice == '6':
                print("Exiting the Travel Itinerary Planner. Goodbye!")
                break

            else:
                print("Invalid choice. Please enter a valid option.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection:
            if connection.is_connected():
                cursor.close()
                connection.close()

if __name__ == "__main__":
    main()