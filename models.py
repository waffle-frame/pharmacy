from peewee import * 

db = SqliteDatabase('db.db')

class BaseModel(Model):
    class Meta:
        database = db
        
# Сеть аптек одного юзера
class Network(BaseModel):
    id = AutoField()
    name = CharField()

# Аптеки 
class Pharmacy(BaseModel):
    id = AutoField()
    network = ForeignKeyField(Network, related_name = 'pharmacies')
    address = CharField()
    name = CharField()
    disabled = BooleanField()
    date = TimeField()

# Пользователи
class Users(BaseModel):
    id = AutoField()
    fio = CharField()
    role = CharField()
    username = CharField()
    password = CharField()
    network = ForeignKeyField(Network, related_name = 'users')

# Отделы
class Department(BaseModel):
    id = AutoField()
    name = CharField()
    pharmacy = ForeignKeyField(Pharmacy, related_name='department')

# Препараты
class Drugs(BaseModel):
    id = AutoField()
    barcode = IntegerField()
    name = CharField()
    category = CharField()
    subcategory = CharField()
    unit = CharField()
    clean_price = FloatField()
    price_sale = IntegerField()
    price_with_discount = FloatField()
    quantity = FloatField()
    shelf_life = TimeField()
    city_of_dev = CharField()
    department = ForeignKeyField(Department, related_name='department')
    pharmacy = ForeignKeyField(Pharmacy, related_name='pharmacy')

# Общий каталог препаратов
class DrugsCatalog(BaseModel):
    id = AutoField()
    barcode = IntegerField()
    name = CharField()
    category = CharField()
    subcategory = CharField()
    unit = CharField()
    city_of_dev = CharField()


# Закуп
class Purchase(BaseModel):
    id = AutoField()
    drug = ForeignKeyField(Drugs, related_name="drug")
    provide = CharField()
    quantity = FloatField()
    total_sum = FloatField()
    date = DateField()
    pharmacy = ForeignKeyField(Pharmacy, related_name='pharmacy') 
    department = ForeignKeyField(Department, related_name='department')

# Сотрудники
class Employees(BaseModel):
    userID = ForeignKeyField(Users, related_name="userID")
    network = ForeignKeyField(Network, related_name="network")
    birthday = DateField()
    position = CharField()
    phone = IntegerField()
    pharmacy = ForeignKeyField(Pharmacy, related_name="pharmacy")
    department = ForeignKeyField(Department, related_name="department")
    date_of_dismissal = DateField()
    is_dismissed = BooleanField()
    employment_date = DateField()

# Паспорта
class Passports(BaseModel):
    id = AutoField()
    employeeID = ForeignKeyField(Employees, related_name='employee')
    passportID = CharField()
    INN = IntegerField()
    date_of_Issue = DateField()
    date_of_Expiration = DateField()
    place_of_Issue = CharField()
    # storage_location = CharField()

# Оплата
class Payment(BaseModel):
    id = AutoField()
    employee = ForeignKeyField(Users, related_name="employee")
    total_amount = FloatField()
    total_sold_product = FloatField()
    date = DateField()
    time = TimeField()
    payment_type = CharField()
    pharmacy = ForeignKeyField(Pharmacy, related_name="pharmacy")
    department = ForeignKeyField(Department, related_name="department")
    networkID = ForeignKeyField(Network, related_name="network")
    is_auto_transfer = BooleanField()

# Проданный товар
class SoldProduct(BaseModel):
    id = AutoField()
    drug_id = ForeignKeyField(Drugs, related_name="drugID")
    total_quantity_sold = FloatField()
    total_amount_sold = FloatField()
    discount = FloatField()
    payment = ForeignKeyField(Payment, related_name="payment")

# Клиенты
class Clients(BaseModel):
    id= AutoField()
    fio = CharField()
    type_client = CharField()
    phone = IntegerField()
    email = CharField()
    balance = FloatField()
    history = ForeignKeyField
    network = ForeignKeyField(Network, related_name="network")
    pharmacy = ForeignKeyField(Pharmacy, related_name="pharmacy")

# История покупок
class ClientHistory(BaseModel):
    id = AutoField()
    client = ForeignKeyField(Clients, related_name='client')
    payment = ForeignKeyField(Payment, related_name='payment')

# Поставщик
class Suppliers(BaseModel):
    id = AutoField()
    name = CharField()
    type_supp = CharField()
    phone = CharField()
    coming = FloatField()
    pay = FloatField()
    balance = FloatField()


# Категория
class Category(BaseModel):
    id = AutoField()
    name = CharField()

# Подктегория 
class Subcategory(BaseModel):
    id = AutoField()
    name = CharField()
    category = ForeignKeyField(Category, related_name='category')

if __name__ == '__main__':
    # DrugsCatalog.create_table()
    Network.create_table()
    Pharmacy.create_table()
    Users.create_table()
    Department.create_table()
    Drugs.create_table()
    Purchase.create_table()
    Employees.create_table()
    Passports.create_table()
    Payment.create_table()
    SoldProduct.create_table()
    Clients.create_table()
    ClientHistory.create_table()
    Suppliers.create_table()