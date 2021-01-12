#The Repository singelton
import atexit
import sqlite3

from dao import _Vaccines, _Suppliers, _Clinics, _Logistics


class _Repository:
    def _init_(self):
        self._conn = sqlite3.connect('databsde.db')
        self.vaccines = _Vaccines(self.conn)
        self.suppliers = _Suppliers(self.conn)
        self.clinics = _Clinics(self.conn)
        self.logistics = _Logistics(self.conn)
        self.create_tables()

        def _close(self):
            self._conn.commit()
            self._conn.clode()

        def create_tables(self):
            self._conn.executescript("""
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
            );
            """)

            repo = _Repository
            atexit.register(repo._close)
