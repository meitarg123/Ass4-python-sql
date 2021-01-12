#Data Transfer Object
class Vaccine:
    def _init_(self, id, date, supplier, quantity):
        self.id = id
        self.date = date
        self.supplier = supplier
        self.quantity = quantity

class Supplier:
    def _init_(self, id, name, logistic):
        self.id = id
        self.name = name
        self.logistic = logistic

class Clinic:
    def _init_(self, id, location, demand, logistic):
        self.id = id
        self.location = location
        self.demand = demand
        self.logistic = logistic

class Logistic:
    def _init_(self, id, name, count_sent, count_recive):
        self.id = id
        self.name = name
        self.count_sent = count_sent
        self.count_recive = count_recive