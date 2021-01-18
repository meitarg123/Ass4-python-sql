# Data Access Objects:
# All of these are meant to be Singleton

class _Vaccines:
    def _init_(self, conn):
        self._conn = conn

    def insert(self, vaccine):
        self._conn.executr("""INSERT INTO Vaccines (id, date, supplier, quantity) VALUES (?,?,?,?)""",
                           [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])

    def find(self, vaccine_id):
        c = self._conn.cursor()
        c.execute("""SELECT id FROM vaccines WHERE  id =?""", [vaccine_id])

    def creat_index(self):
        ("""CREATE INDEX vaccins_by_date ON _Vaccines date """)


class _Suppliers:
    def _init_(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.executr("""INSERT INTO Supplier (id, name, logistic) VALUES (?,?,?)""",
                           [supplier.id, supplier.name, supplier.logistic])

    def find(self, supplier_id):
        c = self._conn.cursor()
        c.execute("""SELECT id FROM suppliers WHERE  id =?""", [supplier_id])


class _Clinics:
    def _init_(self, conn):
        self._conn = conn

    def insert(self, clinic):
        self._conn.executr("""INSERT INTO Clinics (id, location, demand, logistic) VALUE (?,?,?,?)""",
                           [clinic.id, clinic.location, clinic.demand, clinic.logistic])

    def find(self, clinic_id):
        c = self._conn.cursor()
        c.execute("""SELECT id FROM clinics WHERE  id =?""", [clinic_id])

    def find_demand_by_location(self, location, amount):
        c = self._conn.executr()
        demand = c.execute("""SELECT demand FROM clinics WHERE location=?""", [location])
        demand = demand - amount


class _Logistics:
    def _init_(self, conn):
        self._conn = conn

    def insert(self, logistic):
        self._conn.executr("""INSERT INTO Logistics(id, name, count_sent, count_recive) Value (?,?,?,?)""",
                           [logistic.id, logistic.name, logistic.count_sent, logistic.count_recive])

    def find(self, logistic_id):
        c = self._conn.cursor()
        c.execute("""SELECT id From logistics WHERE id =?""", [logistic_id])
