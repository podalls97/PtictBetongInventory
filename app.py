from flask import Flask, render_template, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Initialize the database with devices and schools tables
def init_db():
    conn = psycopg2.connect(
        dbname="ptict",
        user="postgres",
        password="root",
        host="localhost",  # Or your PostgreSQL server IP
        port="5432"
    )
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id SERIAL PRIMARY KEY,
            school VARCHAR(255) NOT NULL,
            device_type VARCHAR(255) NOT NULL,
            model VARCHAR(255) NOT NULL,
            serial_number VARCHAR(255) NOT NULL,
            status VARCHAR(255) NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schools (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE
        )
    ''')

    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

# Add new school to the database
@app.route('/add_school', methods=['POST'])
def add_school():
    school_name = request.form.get('school_name')

    if not school_name:
        return jsonify({'error': 'School name is required!'}), 400

    conn = psycopg2.connect(
        dbname="ptict",
        user="postgres",
        password="root",
        host="localhost",  # Or your PostgreSQL server IP
        port="5432"
    )
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO schools (name) VALUES (%s)', (school_name,))
        conn.commit()
    except psycopg2.IntegrityError:
        conn.close()
        return jsonify({'error': 'School already exists!'}), 400

    conn.close()
    return jsonify({'message': 'School added successfully!'})

# Get list of schools from the database
@app.route('/get_schools', methods=['GET'])
def get_schools():
    conn = psycopg2.connect(
        dbname="ptict",
        user="postgres",
        password="root",
        host="localhost",  # Or your PostgreSQL server IP
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM schools')
    rows = cursor.fetchall()
    conn.close()

    schools = [{'name': row[0]} for row in rows]
    return jsonify(schools)

# Get inventory based on school and device type
@app.route('/get_inventory', methods=['POST'])
def get_inventory():
    school = request.form.get('school')
    device_type = request.form.get('device_type')

    if not school or not device_type:
        return jsonify([]), 400

    conn = psycopg2.connect(
        dbname="ptict",
        user="postgres",
        password="root",
        host="localhost",  # Or your PostgreSQL server IP
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute('''
        SELECT model, serial_number, status FROM devices
        WHERE school = %s AND device_type = %s
    ''', (school, device_type))
    rows = cursor.fetchall()
    conn.close()

    devices = [{'model': row[0], 'serial_number': row[1], 'status': row[2]} for row in rows]
    return jsonify(devices)

# Add new device to the database
@app.route('/add_device', methods=['POST'])
def add_device():
    school = request.form.get('school')
    device_type = request.form.get('device_type')
    model = request.form.get('model')
    serial_number = request.form.get('serial_number')
    status = request.form.get('status')

    if not (school and device_type and model and serial_number and status):
        return jsonify({'error': 'All fields are required!'}), 400

    conn = psycopg2.connect(
        dbname="ptict",
        user="postgres",
        password="root",
        host="localhost",  # Or your PostgreSQL server IP
        port="5432"
    )
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO devices (school, device_type, model, serial_number, status)
        VALUES (%s, %s, %s, %s, %s)
    ''', (school, device_type, model, serial_number, status))
    
    conn.commit()
    conn.close()

    return jsonify({'message': 'Device added successfully!'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
