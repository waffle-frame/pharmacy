import random
from re import T
import barcode
from peewee import _date_part, format_date_time, simple_date_time
from models import *
from amodels import Drugs as dr
from calendar import month, monthrange
from datetime import date, datetime
from barcode.writer import ImageWriter
from barcode.errors import WrongCountryCodeError


Network(name = 'Сеть аптек "Домовой Кашимир"').save()
# net = Network(name = 'Сеть аптек "Балдежный патруль"').save()
# net = Network(name = 'Сеть аптек "Ясное Солнышко"').save()
# # 
pharmacies = Pharmacy(name = 'Косынка моряка', network = 1, address="main street", date=date.today(), disabled=False).save()
# pharmacies = Pharmacy(name = 'Сеть аптек Котелок ведьмы', network = 1, address="Excalibur street", date=date.today(), disabled=False).save()
# pharmacies = Pharmacy(name = 'Косынка моряка', network = 1, address="XFCE avenue 57 st", date=date(year=2008, month=3, day=7), disabled=True).save()
Department(name="Оптом", pharmacy=1).save()
Department(name="Розница", pharmacy=1).save()
# Department(name="Подвал", pharmacy=2).save()
# Department(name="Яйце-склад", pharmacy=2).save()
# Department(name="Мертвые опоссумы", pharmacy=3).save()
# Department(name="Для богатеньких", pharmacy=3).save()

# drugs = Drugs( category='shuu1', subcategory="PLMKO1", barcode=34234234, name='Амоксиклав', city_of_dev='USA', price_with_discount=1 , clear_price=999, pharmacy=1, unit = "шт.", department=1, quantity=934, shelf_life='05-23-2021' ).save()
# drugs = Drugs( category='shuu2', subcategory="PLMKO2", barcode=234, name='Алайбалай', city_of_dev='USA', price_with_discount=2 , clear_price=1546, pharmacy=1, unit = "шт.", department= 1 , quantity=21, shelf_life='06-14-2022').save()
# drugs = Drugs( category='shuu3', subcategory="PLMKO3", barcode=3444, name='Балалай', city_of_dev='USA', price_with_discount=3 , clear_price=5, pharmacy=1, unit = "шт.", department= 1 , quantity=1, shelf_life='08-08-2022').save()
# drugs = Drugs( category='shuu4', subcategory="PLMKO4", barcode=23444, name='Пирит', city_of_dev='USA', price_with_discount=4 , clear_price=167, pharmacy=1, unit = "шт.", department= 1, quantity=459, shelf_life='01-19-2023').save()
# drugs = Drugs( category='shuu5', subcategory="PLMKO5", barcode=67545, name='Пенталгин', city_of_dev='USA', price_with_discount=5 , clear_price=0.5, pharmacy=1, unit = "шт.", department= 1 , quantity=4, shelf_life='09-17-2029').save()
# drugs = Drugs( category='shuu6', subcategory="PLMKO6", barcode=300000, name='Жумайсынба', city_of_dev='USA', price_with_discount=6 , clear_price=565, pharmacy=1, unit = "шт.", department= 1 , quantity=74, shelf_life='11-29-2025').save()
# drugs = Drugs( category='shuu7', subcategory="PLMKO7", barcode=347643, name='Жашкалдыш', price=324, pharmacy=1, unit = "шт.", department= 1 , quantity=123, shelf_life='12.05').save()
# drugs = Drugs( category='shuu8', subcategory="PLMKO8", barcode=67545, name='Полистирол', price=0.5, pharmacy=1, unit = "шт.", department= 1 , quantity=2222, shelf_life='6.9.2069' ).save()
# drugs = Drugs( category='shuu9', subcategory="PLMKO9", barcode=67545, name='ooooo', price=0.5, pharmacy=1, unit = "шт.", department= 1 , quantity=2222, shelf_life='6.9.2069' ).save()

# drugs = Drugs( category='shuu6', subcategory="PLMKO6", barcode=300000, name='Жумайсынба', price=565, pharmacy=1, unit = "шт.", department= 2 , quantity=74, shelf_life='2.05.').save()
# drugs = Drugs( category='shuu7', subcategory="PLMKO7", barcode=347643, name='Жашкалдыш', price=324, pharmacy=1, unit = "шт.", department= 2 , quantity=123, shelf_life='12.05').save()
# drugs = Drugs( category='shuu8', subcategory="PLMKO8", barcode=67545, name='Полистирол', price=0.5, pharmacy=1, unit = "шт.", department= 2 , quantity=2222, shelf_life='6.9.2069' ).save()
# drugs = Drugs( category='shuu9', subcategory="PLMKO9", barcode=67545, name='ooooo', price=0.5, pharmacy=1, unit = "шт.", department= 2 , quantity=2222, shelf_life='6.9.2069' ).save()

Users(username="Admin", password='admin', role='admin', fio="Adminov Admin Adminovich", network=1).save()
# Users(username="Admino", password='adminn', role='admin', fio="Adminov Admin Adminovich", network=2).save()

# Users(username='pharm', password = 'pharm', role='pharm', fio = 'Киро Ким', network = 1).save()
# Users(username='pharm2', password='pharm2', role='pharm', fio='Ashab Baban', network=1).save()
# # Users(username='p', password='1', role='pharm', fio='Сосо павлиашвили', network=1).save()

# Employees(network=1, userID=2, age=23, position="Кассир", birthday="123", pharmacy=1, department=2, date_of_dismissal="", is_dismissed=False, employment_date="21-02-2019", phone=123456789).save()
# Employees(network=1, userID=3, age=56, position="Кассир", birthday="123", pharmacy=2, department=4, date_of_dismissal="", is_dismissed=False, employment_date="21-02-2022", phone=987654321).save()
# Employees(network=4, age=15, position="Кассир", pharmacy=3, department=1, date_of_dismissal="", is_dismissed=False, employment_date="21-02-2022").save()
# Employees(userID=2, age=23, position="Кассир", pharmacy=1, department=2, date_of_dismissal="", is_dismissed=False, employment_date="21-02-2019").save()

# Clients(fio="Асхабов Влад Григорьевич", type_client="Льготник", phone=939939094, email="ashab1991@gmail.com", balance=2333, pharmacy=1, network=1).save()

# # update = Pharmacy.select().where(Pharmacy.id==1)
# # update(network_id=1).save()
# # print(update)

# # отделы
# # # закуп - аптека
# # Purchase(quantity=23, unit=3, price=213,  clear_price=2345, summ=123, 
# #         date=date.today(), provide='Lyps Inc.', pharmacy=1).save()


# drug = Drugs.select().where(Drugs.department_id==3, Drugs.pharmacy_id==2, Drugs.id==1)

# drug = Drugs.get_by_id(1)
# Drugs.update(
#     quantity = drug.quantity - 34 
# ).where(Drugs.id ==1).execute()

# year = date.today().year
# day = monthrange(year, date.today().month)[1]
# month = date.today().month
# print(datetime(year,month,day).strftime('%Y-%m-%d'))
# print(datetime(year, monthrange()))
# print(Payment.select().where(Payment.date.between())

# print(dir(barcode))
# print(barcode.Code128('1234567891235').save('name', text='dddd') )
# s = barcode.get('Code128', '112233445566', writer=ImageWriter())

# s=[]
# for i in range(10):
#     s += str(random.randint(0,9))

# print('ASDewvsf dsfwe wefgw ESDD'.capitalize())

# for i in DrugsCatalog:
    # print(i.name.capitalize())

# print(s, type(s))
# ss = s.save('ssss')
# ################################################################################################################################################
# for i in dr.select():
#     # print(d.get(int(str(i.barcode))))
#     # print(i.barcode)
#     DrugsCatalog(
#         barcode = i.barcode,
#         name = i.name,
#         unit = i.unit,
#         category = '',
#         subcategory = '',
#         city_of_dev = ''
#     ).save()

# a = '2020-12-12'
# print(datetime.strptime(a, '%Y-%m-%d'))

# a = [0,1,2,3,4,5,6,7,8,9,10,11]
# a = [0] * 12
# print(a)