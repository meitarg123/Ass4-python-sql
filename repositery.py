#The Repository singelton
import atexit
import sqlite3
#import os
from dao import _Vaccines, _Suppliers, _Clinics, _Logistics

class repositery:
    def __init__(self):
        self.conn = sqlite3.connect('databsde.db')
        self.vaccines = _Vaccines(self.conn)
        self.suppliers = _Suppliers(self.conn)
        self.clinics = _Clinics(self.conn)
        self.logistics = _Logistics(self.conn)
        self.max_id_vaccine = 0

    def close(self):
        self.conn.commit()
        self.conn.close()

    def create_tables(self):
        self.conn.execute(""" DROP TABLE IF EXISTS vaccines""")
        self.conn.execute(""" DROP TABLE IF EXISTS suppliers""")
        self.conn.execute(""" DROP TABLE IF EXISTS clinics""")
        self.conn.execute(""" DROP TABLE IF EXISTS logistics""")
        self.conn.execute("""
        CREATE TABLE vaccines (
        id       INTEGER    PRIMARY KEY,
        date     DATE   NOT NULL,
        supplier INTEGER    REFERENCES Supplier(id),
        quantity INTEGER    NOT NULL )
        """)

        self.conn.execute("""
        CREATE TABLE suppliers (
        id  INTEGER  PRIMARY KEY,
        name     STRING NOT NULL,
        logistic INTEGER REFERENCES Logistic(id))
        """)

        self.conn.execute("""
        CREATE TABLE clinics(
        id       INTEGER PRIMARY KEY,
        location STRING  NOT NULL,
        demand   INTEGER NOT NULL,
        logistic INTEGER REFERENCES Logistic(id))
        """)

        self.conn.execute("""
        CREATE TABLE logistics(
        id             INTEGER PRIMARY KEY ,
        name           TEXT NOT NULL, 
        count_sent     INTEGER NOT NULL, 
        count_received INTEGER NOT NULL)
        """)

    def send_shipment(self, location, amount):
        cursor = self.conn
        max_id_vaccine = cursor.execute("""SELECT id FROM vaccines ORDER BY id DESC """).fetchone()[0]
        self.max_id_vaccine = max_id_vaccine
        tmpamount= int(amount)
        amount = int(amount)
        counter = 0
        list_clinics_by_location = cursor.execute("""SELECT * FROM clinics WHERE location=?""", [location]).fetchone()
        demand = int(list_clinics_by_location[2])
        ans = demand - amount
        cursor.execute("""UPDATE clinics SET demand=? WHERE location=?""", [ans, location])
        vaccine_by_date = cursor.execute("""SELECT * FROM vaccines ORDER BY date ASC """).fetchall()
        vaccine = vaccine_by_date[counter]
        vaccsine_quantity = vaccine[3]
        id =vaccine[0]
        if vaccsine_quantity > amount:
            quantity = vaccsine_quantity - amount
            cursor.execute("""UPDATE vaccines SET quantity=? WHERE ID=?""", [ quantity, id])
        else:
            while amount > 0:
                curr_id = vaccine[0]
                inventory = vaccine[3]
                if inventory > amount:
                    inventory = inventory-amount
                    cursor.execute("""UPDATE vaccines SET quantity=? WHERE ID=?""", [inventory, curr_id])
                    amount = 0
                else:
                    amount = amount - inventory
                    cursor.execute("""DELETE FROM vaccines WHERE id=?""", [curr_id])
                    counter = counter + 1
                vaccine = vaccine_by_date[counter]

        logistic_id = list_clinics_by_location[3]
        sent_inventory = cursor.execute("""SELECT count_sent FROM logistics WHERE id=?""", [logistic_id]).fetchone()
        count_sent = sent_inventory[0]
        count_sent = count_sent + tmpamount
        cursor.execute(""" UPDATE logistics SET count_sent=? WHERE id=?""", [count_sent, logistic_id])

    def receive_shipment(self, name, amount, date):
        cursor = self.conn
        amount = int(amount)
        suplier_id = cursor.execute("""SELECT id FROM suppliers WHERE name=? """, [name]).fetchone()
        supid=suplier_id[0]
        self.max_id_vaccine = self.max_id_vaccine + 1
        cursor.execute("""INSERT INTO vaccines (id, date, supplier, quantity) VALUES (?, ?, ?, ?)""", [self.max_id_vaccine, date, supid, int(amount)])

        logistic_id = cursor.execute("""SELECT logistic FROM suppliers where name=?""", [name]).fetchone()
        log_id = logistic_id[0]
        receive = cursor.execute(""" SELECT count_received FROM logistics WHERE id=?""", [log_id]).fetchone()[0]
        count_received = int(receive) + amount
        cursor.execute("""UPDATE logistics SET count_received=? WHERE id=?""", [count_received, log_id])
        check = cursor.execute("""SELECT  count_received FROM logistics WHERE id=?""",[log_id]).fetchone()[0]
        print(check)

    def summary(self):
        cursor = self.conn
        total_inventory = cursor.execute(""" SELECT SUM(quantity) FROM vaccines """).fetchone()[0]
        total_demant = cursor.execute("""SELECT SUM(demand) FROM clinics""").fetchone()[0]
        total_received = cursor.execute("""SELECT SUM(count_received) FROM logistics""").fetchone()[0]
        total_sent = cursor.execute("""SELECT SUM(count_sent) FROM logistics""").fetchone()[0]
        list = [str(total_inventory), str(total_demant), str(total_received), str(total_sent)]
        ans = ', '.join(list) + '\n'

        return ans


repo = repositery()
atexit.register(repo.close)
