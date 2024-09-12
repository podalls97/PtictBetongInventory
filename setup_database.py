import psycopg2

# Connect to PostgreSQL database
conn = psycopg2.connect(
    dbname="ptict",
    user="postgres",
    password="root",
    host="localhost",  # Or your PostgreSQL server IP
    port="5432"  # Default port
)

cursor = conn.cursor()

# Create devices table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS devices (
    id SERIAL PRIMARY KEY,
    school VARCHAR(255) NOT NULL,
    device_type VARCHAR(255) NOT NULL,
    model VARCHAR(255) NOT NULL,
    serial_number VARCHAR(255) NOT NULL,
    status VARCHAR(255) NOT NULL
);
''')

# Create schools table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS schools (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);
''')

conn.commit()
conn.close()

print("Database setup complete!")
