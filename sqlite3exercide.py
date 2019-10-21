import sqlite3

connection = sqlite3.connect("user_data.db")

cursor = connection.cursor()

# Query to create table
create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

# Insert single record
user = (1, "yogendra", "pass")
insert_user = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_user, user)


# Insert Mutliple records
users = [
     (2, "Pramod", "pass11"),
     (3, "Amit", "pass22")
]
cursor.executemany(insert_user, users)

# Retrieve data

select_users = "SELECT * FROM users"

for row in cursor.execute(select_users):
    print(row)


# Save data
connection.commit()

# Close connection
connection.close()