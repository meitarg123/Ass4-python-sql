#The Repository singelton
import atexit
import sqlite3
import os
from dao import _Vaccines, _Suppliers, _Clinics, _Logistics

class repositery:
    def __init__(self):
        self.conn = sqlite3.connect('databsde.db')
        self.vaccines = _Vaccines(self.conn)
        self.suppliers = _Suppliers(self.conn)
        self.clinics = _Clinics(self.conn)
        self.logistics = _Logistics(self.conn)

    def close(self):
        self.conn.commit()
        self.conn.close()

    def create_tables(self):
        self.conn.executescript("""
        CREATE TABLE vaccines (
        id INTEGER PRIMARY KEY,
        date DATE NOT NULL,
        supplier INTEGER REFERENCES Supplier(id),
        quantity INTEGER NOT NULL
        );
        
        CREATE TABLE suppliers (
        id INTEGER PRIMARY KEY
        name STRING NOT NULL,
        logistic INTEGER REFERENCES Logistic(id)
        );
        
        CREATE TABLE clinics(
        id INTEGER PRIMARY KEY
        location STRING NOT NULL,
        demand INTEGER NOT NULL,
        logistic INTEGER REFERENCES Logistic(id)
        );
        
        CREATE TABLE logistics(
        id INTEGER PRIMARY KEY 
        name STRING NOT NULL 
        count_sent INTEGER NOT NULL 
        count_received INTEGER NOT NULL
        );""")

    def send_shipment(self, location, amount):
        cursor = self.conn
        tuple_clinics_by_location = cursor.execute("""SELECT * FROM clinics WHERE location=?""", [location])
        tuple_clinics_by_location[2] = tuple_clinics_by_location[2]-amount
        vaccine_by_date = cursor.execute("""SELECT * FROM vaccines ORDER BY date ASK """)
        vaccine = vaccine_by_date.fetchone()
        vaccsine_quantity = vaccine[3]
        id =vaccine[0]
        if vaccsine_quantity > amount:
            vaccsine_quantity = vaccsine_quantity - amount
            cursor.execute("""UPDATE vaccines SET quantity=vaccsine_quantity WHERE ID=?""", [id])
        else:
            while amount > 0:
                curr_id = vaccine[0]
                inventory = vaccine[3]
                if inventory > amount:
                    inventory = inventory-amount
                    cursor.execute("""UPDATE vaccines SET quantity=inventory WHERE ID=?""", [id])
                    amount = 0
                else:
                    amount = amount - inventory
                    cursor.execute("""DELETE FROM vaccines WHERE id=?""", [curr_id])
                vaccine = vaccine_by_date.fetchone() #check if its in while(it should be in while out of else

        logistic_id = tuple_clinics_by_location[3]
        sent_inventory = cursor.execute("""SELECT count_sent FROM logistics WHERE id=?""", [logistic_id])
        sent_inventory = sent_inventory+amount
        cursor.execute(""" UPDATE logistics SET count_sent=sent_inventory WHERE id=?""", [logistic_id])

    def receive_shipment(self, name, amount, date):
        cursor = self.conn
        suplier_id = cursor.execute("""SELECT id FROM suppliers WHERE name=? """, [name])
        max_id = cursor.execute("""SELECT id FROM vaccines ORDER BY date ASK """).fetchone()
        new_id = max_id+1
        cursor.execute("""INSERT INTO vaccines (id, date, supplier, quantity) VALUES (?,?,?,? )""",[new_id,date, suplier_id, amount ])
        receive = cursor.execute(""" SELECT count_receive FROM logistics WHERE name=?""", [name])
        receive = receive+amount
        cursor.execute("""UPDATE logistics SET count_receive=receive WHERE name=?""", [name])

    def summary(self):
        cursor = self.conn
        total_inventory = cursor.execute(""" SELECT SUM quantity FROM vaccines """)
        total_demant = cursor.execute("""SELECT SUM demand FROM clinics""")
        total_received = cursor.execute("""SELECT SUM count_receive FROM logistics""")
        total_sent = cursor.execute("""SELECT SUM count_sent FROM logistics""")
        list = [total_inventory, total_demant, total_received, total_sent ]
        return list


repo = repositery()
atexit.register(repo.close)
