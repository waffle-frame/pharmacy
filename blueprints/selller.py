from operator import ne
from re import S
import barcode
from models import *
from datetime import date
from random import randint
from fuzzywuzzy import fuzz
from flask.json import jsonify
from time import localtime, strftime
from flask import Blueprint, render_template, request, redirect, session


bp = Blueprint('selller', __name__)


def check_session():
    if (not 'username' in session) or (not 'networkid' in session):
        return redirect('/login/')
def GetName():
    username = Users.get_by_id(session['userid'])
    return username.fio

@bp.route('logout', methods=['GET', 'POST'])
def Logout():
    print(session)
    session.clear()
    return redirect('/login')


# *ПРОДАЖА
@bp.route('/sale', methods=['GET', 'POST', 'PUT'])
def Sale():
    is_first_request = False
    pharmacy = session.get('pharmacy')
    department = session.get('department')

    if request.method == 'GET':
        customer = Clients.select().where(
            Clients.pharmacy == session['pharmacy'])
        return render_template('selller/selller_Sale.html', customer=customer, name=GetName())

    if request.method == 'PUT':
        filtred = []
        value = request.json['value']
        type_search = request.json['type_search']

        if is_first_request == False:
            is_first_request = True
            db_data = Drugs.select().where(Drugs.pharmacy == pharmacy,
                                           Drugs.department == department)

        if type_search == 'by_name':
            for i in db_data:
                filter = fuzz.partial_ratio(value.lower(), i.name.lower())
                if filter >= 50:
                    filtred_item_obj = {'name': i.name, 'barcode': i.barcode,
                                        'shelf_life': i.shelf_life, 'price': i.price_sale}
                    filtred.append(filtred_item_obj)
        if type_search == 'by_barcode':
            for i in db_data:
                filter = fuzz.partial_ratio(str(value), str(i.barcode))
                if filter >= 60:
                    filtred_item_obj = {'name': i.name, 'barcode': i.barcode,
                                        'shelf_life': i.shelf_life, 'price': i.price_sale}
                    filtred.append(filtred_item_obj)

        return jsonify(filtred)

    try:
        _data = request.json
        jsonDrug = {}

        type_compare = request.json['type']
        value = request.json['value']
        if type_compare == 'by_name':
            drugData = Drugs.get_or_none(Drugs.name == value, Drugs.department ==
                                         session['department'], Drugs.pharmacy == session['pharmacy'])
        if type_compare == 'by_barcode':
            drugData = Drugs.get_or_none(Drugs.barcode == value, Drugs.department ==
                                         session['department'], Drugs.pharmacy == session['pharmacy'])

        if drugData != None:
            jsonDrug = {
                "val": 0,
                "quantity": 0,
                "id": drugData.id,
                "name": drugData.name,
                "unit": drugData.unit,
                "barcode": drugData.barcode,
                "price": drugData.clean_price,
                "price_sale": drugData.price_sale,
                "shelf_life": drugData.shelf_life,
                "server_quantity": drugData.quantity,
                "country_of_origin": drugData.city_of_dev,
            }

            return jsonify(jsonDrug)

        else:
            return jsonify({'error': 'notExists'})

    except:
        print({'error': 'notExists'})
        return jsonify({'error': 'notExists'})

# *ОПЛАТА
@bp.route('/payment/pay', methods=['POST'])
def PaymentAdd():
    check_session()

    products = request.json['products']
    secondary_data = request.json['secondary_data']
    print(secondary_data)

    try:
        payment = Payment(
            date = '2021-01-01',
            # date=date.today(),
            is_auto_transfer=False,
            employee=session['userid'],
            pharmacy=session['pharmacy'],
            networkID=session['networkid'],
            department=session['department'],
            time=strftime("%H:%M", localtime()),
            total_amount=secondary_data.get('total_amount'),
            payment_type=secondary_data.get('payment_type'),
            total_sold_product=secondary_data.get('total_quantity_products'),
        )
        payment.save()

        for i in products:
            Drugs.update(
                quantity=i.get('server_quantity') - i.get('quantity')
            ).where(
                Drugs.id == i.get('id'),
                Drugs.pharmacy == session['pharmacy'],
                Drugs.department == session['department'],
            ).execute()

            SoldProduct(
                payment=payment.id,
                drug_id=i.get('id'),
                discount=i.get('discount'),
                total_quantity_sold=i.get('quantity'),
                total_amount_sold=i.get('quantity') * i.get('price_sale')
            ).save()

        if secondary_data['customer'] > 0:
            ClientHistory(
                payment=payment.id,
                client=secondary_data['customer']
            ).save()

        return jsonify({"status": "payment_pay"})

    except:
        return jsonify({"status": "error", "error": "payment_pay"})




# *ПРЕПАРАТЫ
# Выведение
@bp.route('show/drug', methods=['GET'])
def ShowDrug():
    check_session()

    if request.method == 'GET':
        drugData = Drugs.select().where(Drugs.pharmacy == session['pharmacy'], Drugs.department == session['department'])
        department = Department.select().where(Department.pharmacy == session['pharmacy'])
        return render_template('selller/selller_Drug_show.html', data=drugData, name=GetName())

# Добавление
@bp.route('/add/drug', methods=['GET', 'POST'])
def AddDrug():
    check_session()

    if request.method == "GET":
        data = Department.get(
            Department.pharmacy == session['pharmacy'], Department.id == session['department'])
        return render_template('selller/selller_Drug_add.html', data=data, name=GetName)

    data = request.json

    try:
        Drugs(department_id=session['department'],
              pharmacy=session['pharmacy'],
              category=data.get('category'),
              subcategory=data.get('subcategory'),
              barcode=data.get('barcode'),
              name=data.get('name'),
              price=data.get('price'),
              quantity=data.get('quantity'),
              unit=data.get('unit'),
              shelf_life=data.get('shelf_life')).save()

        return jsonify({"status": "drug_add"})

    except:
        return jsonify({"status": "error", "error": "drug_add"})

# Перемещение
@bp.route('drugs/transfer/<drugID>', methods=['GET', 'POST'])
def TransferDrug(drugID):
    new_method = []
    new_method.append(Drugs.get_by_id(drugID))
    if request.method == 'GET':
        new_method.append(Department.select().where(Department.pharmacy == session['pharmacy']))
        return render_template('selller/selller_Drug_transfer.html', datas=new_method, name=GetName())

    try:
        _data = request.json
        quantity = new_method[0].quantity
        _quantity = float(_data['quantity'])

        if _quantity > quantity:
            return jsonify({"status": "error", "error": "drug_exceeded_quantity_limit"})

        if _quantity == quantity or _quantity < quantity:
            Drugs.update(
                quantity = quantity - _quantity
            ).where(Drugs.id == drugID).execute()        
            
            Drugs(
                unit = new_method[0].unit,
                name = new_method[0].name,
                pharmacy = session['pharmacy'],
                barcode = new_method[0].barcode,
                department = _data['department'],
                category = new_method[0].category,
                shelf_life = new_method[0].shelf_life,
                price_sale = new_method[0].price_sale,
                subcategory = new_method[0].subcategory,
                clean_price = new_method[0].clean_price,
                city_of_dev = new_method[0].city_of_dev,
                quantity = float(_data.get('quantity')),
                price_with_discount = new_method[0].price_with_discount,
            ).save()
    
        return jsonify({"status": "drug_transfer"})

    except:
        return jsonify({"status": "error", "error": "drug_transfer"})



# *КЛИЕНТЫ
# Выведение
@bp.route('show/client', methods=['GET'])
def ShowClient():
    if request.method == 'GET':
        clients = Clients.select().where(Clients.pharmacy ==
                                         session['pharmacy'], Clients.network == session['networkid'])

        return render_template('selller/selller_Clients_show.html', clients=clients, name=GetName())

#*  
@bp.route('show/client/<idClient>', methods=['GET'])
def ShowAboutClient(idClient):
    if request.method == 'GET':
        history = ClientHistory.select().where(ClientHistory.client == idClient)
        client_info = Clients.get_by_id(idClient)
        return render_template('selller/selller_Client_About_show.html', history=history, client=client_info, name=GetName())

#* Добавление
@bp.route('add/client', methods=['GET', 'POST'])
def AddClient():
    if request.method == 'GET':
        return render_template('selller/selller_Client_add.html', name=GetName())

    _data = request.json
    print(_data)
    if _data.get('balance') == None:
        _balance = 0
    else:
        _balance = _data.get('balance')

    if _data.get('email') == None:
        _email = 'Не указано'
    else:
        _email = _data.get('email')

    try:
        Clients(
            email=_email,
            balance=_balance,
            pharmacy=session['pharmacy'],
            fio=_data.get('name'),
            phone=_data.get('phone'),
            network=session['networkid'],
            type_client=_data.get('type_client')
        ).save()
        return jsonify({"status": "client_add"})

    except:
        return jsonify({"status": "error", "error": "client_add"})




# *ОТЧЕТЫ
# Все отчеты
@bp.route('/show/report', methods=['GET', 'POST'])
def GetReport():

    payment_data = Payment.select().where(Payment.department == session['department'],
                                          Payment.pharmacy == session['pharmacy'],
                                          Payment.employee == session['userid'])

    # print(payment_data)

    return render_template('selller/selller_Reports_show.html', payment_data=payment_data, name=GetName())

# Подробности
@bp.route('show/report/<idReport>', methods=['GET', 'POST'])
def ShowReport_byID(idReport):

    getReport_byID = SoldProduct.select().where(SoldProduct.payment == idReport)

    print(getReport_byID)

    return render_template('selller/selller_Report_show.html', getReport_byID=getReport_byID, name=GetName())




# PURCHASE BLOCK
# * ДОБАВЛЕНИЕ
@bp.route('purchase/add', methods=['GET', 'POST', 'UPDATE', 'PUT'])
def AddPurchase():
    if request.method == 'GET':
        idPharmacy = session.get('pharmacy')
        _pharmacy = Pharmacy.get_by_id(idPharmacy)
        _departs = Department.select().where(Department.pharmacy == idPharmacy)
        nextPurchase = Purchase.select(fn.MAX(Purchase.id)+1).scalar()

        return render_template('selller/selller_Purchase_add.html', departments=_departs, pharmacy=_pharmacy, nextPurchase=nextPurchase, name=GetName())

    if request.method == 'UPDATE':
        data = {}
        _data = request.json

        if _data.get('name'):
            temp = Drugs.get_or_none(Drugs.name==_data.get('name'))
            if temp == None:
                temp = DrugsCatalog.get_or_none(DrugsCatalog.name==_data.get('name'))
                
        else:
            temp = Drugs.get_or_none(Drugs.barcode==_data.get('barcode'))
            if temp == None:
                temp = DrugsCatalog.get_or_none(DrugsCatalog.barcode==_data.get('barcode'))

        if temp != None:
            data = { 
                'status': 'ok',
                'id' : temp.id,
                'unit': temp.unit,
                'name': temp.name,
                'barcode': temp.barcode,
                'city_of_dev': temp.city_of_dev}
        else:
            data = {'status' : 'noExsists'}

        return jsonify(data)

    if request.method == 'PUT':
        generated_code = '96'
        generated_code += str(randint(0, 6))

        for i in range(10):
            generated_code += str(randint(0,9))

        ISBN_code = barcode.generate(name='EAN13', code=generated_code, output='PNG')
        print(generated_code, barcode.EAN13(generated_code))

        return jsonify({'generated_barcode' : generated_code})

    try:
        _data = request.json
        _drug_data_from_db = DrugsCatalog.get_or_none(DrugsCatalog.barcode == _data.get('barcode'))

        maxValueOfDepartment = int(str(max(Department.select(fn.MAX(Department.id)).where(Department.pharmacy == session['pharmacy']))))
        minValueOfDepartment = int(str(min(Department.select(fn.MIN(Department.id)).where(Department.pharmacy == session['pharmacy']))))

        if _drug_data_from_db == None:
            _drug_data_from_db = DrugsCatalog(
                barcode = _data.get('barcode'),
                name = _data.get('name').capitalize(),
                unit = _data.get('unit'),
                category = _data.get('category').capitalize(),
                subcategory = _data.get('subcategory').capitalize(),
                city_of_dev = 'no'.capitalize())
            _drug_data_from_db.save()

        for i in range(minValueOfDepartment, maxValueOfDepartment+1):
            if _data.get(f'department_{i}') != '':
                tempDrug = Drugs(
                    department  = i,
                    city_of_dev ='no'.capitalize(),
                    pharmacy =session['pharmacy'],
                    unit =_drug_data_from_db.unit,
                    barcode =_data.get('barcode'),
                    price_sale =_data.get('price_sale'),
                    shelf_life =_data.get('shelf_life'),
                    name =_data.get('name').capitalize(),
                    clean_price =_data.get('clear_price'),
                    quantity =_data.get(f'department_{i}'),
                    category =_drug_data_from_db.category.capitalize(),
                    price_with_discount =_data.get('price_with_discount'),
                    subcategory =_drug_data_from_db.subcategory.capitalize(),
                )
                tempDrug.save()

                Purchase(
                    department=i,
                    date=date.today(),
                    pharmacy_id=session['pharmacy'],
                    drug=tempDrug.id,
                    provide=_data.get('provide').capitalize(),
                    quantity=_data.get(f'department_{i}'),
                    total_sum=_data.get('price_with_discount'),
                ).save()
            
            if 'onlyForThisPharmacy' in _data:
                DrugsCatalog.delete_by_id(int(str(_drug_data_from_db)))

        return jsonify({"status": "purchase_add"})

    except IntegrityError:
        return jsonify({"status": "error", "error": "purchase_error_find_drug"})
    except:
        return jsonify({"status": "error", "error": "purchase_add"})

# *ВЫВОД
@bp.route('purchase/show', methods=['GET', 'POST'])
def ShowPurchase():

    purchaseList = Purchase.select().where(Purchase.pharmacy == session['pharmacy'])

    return render_template('selller/selller_Purchase_show.html', purchaseList=purchaseList, name=GetName())