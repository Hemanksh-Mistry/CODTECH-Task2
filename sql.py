# Install requirements
import os
os.system('pip install mysql-connector-python')

# SQL Setup for the Library Management System

import mysql.connector

con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
)

cursor = con.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS LibraryDB")

cursor.execute("USE LibraryDB")

cursor.execute("""
CREATE TABLE Items (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        author VARCHAR(255),
        category ENUM('Book', 'Magazine', 'DVD') NOT NULL,
        available BOOLEAN DEFAULT TRUE,
        due_date DATE,
        overdue_fine DECIMAL(10, 2) DEFAULT 0.00
        );
""")