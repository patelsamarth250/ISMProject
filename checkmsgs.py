import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Query the messages table to fetch all messages
c.execute("SELECT * FROM messages")

# Fetch all rows
messages = c.fetchall()

# Print the messages
for message in messages:
    print(message)

# Close the connection
conn.close()
