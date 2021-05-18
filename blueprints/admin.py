from time import perf_counter
import barcode
from peewee import Query
from models import *
from random import choice
from random import randint
from calendar import monthrange
from datetime import date, datetime
from string import ascii_letters, ascii_lowercase, digits
from flask import Blueprint, render_template, request, redirect, session, jsonify


bp = Blueprint('admin', __name__)

def check_session():
    if (not 'username' in session) or (not 'networkid' in session):
        return redirect('/login/')        
def translate(text):
    symbols = (
        u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ ",
        (*list(u'abvgdee'), 'zh', *list(u'zijklmnoprstuf'), 'kh', 'z', 'ch', 'sh', 'sh', '',
        'y', '', 'e', 'yu','ya', *list(u'ABVGDEE'), 'ZH', *list(u'ZIJKLMNOPRSTUF'), 'KH', 'Z', 'CH', 'SH', 'SH', *list(u'_Y_E'), 'YU', 'YA', ' '))
        
    translate = lambda x: ''.join([coding_dict[i] for i in x])
    coding_dict = {source: dest for source, dest in zip(*symbols)}
    return translate(text)
def DropdownPharmacies():
    check_session()

    dropdownPharmacies = Pharmacy.select().where(Pharmacy.network == session['networkid'], Pharmacy.disabled == 0)
    return dropdownPharmacies
def date_generate():
    this_year = date.today().year
    this_month = date.today().month

    this_year_last_day = monthrange(this_year, 12)[1]
    this_month_last_day = monthrange(this_year, date.today().month)[1]

    # YEAR
    first_month = datetime(this_year, 1, 1).strftime('%Y-%m-%d')
    last_month = datetime(this_year, 12, this_year_last_day).strftime('%Y-%m-%d')
    # MONTH
    first_day_month = datetime(this_year, this_month, 1).strftime('%Y-%m-%d')
    last_day_month = datetime(this_year, this_month, this_month_last_day).strftime('%Y-%m-%d')

    return first_day_month, last_day_month, first_month, last_month
def password_generate():
    source = ascii_letters + digits
    result_str = ''.join((choice(source) for i in range(8)))

    return result_str
def GetName():
    username = Users.get_by_id(session['userid'])
    return username.fio

@bp.route('/', methods=['GET', 'UPDATE'])
def MainGet():
    if request.method == 'GET':
        return render_template('admin/index.html', dropdownPharmacies=DropdownPharmacies(), name=GetName())
    
    if request.method == 'UPDATE':
        temp_month = 1
        temp_amount = 0

        data = {}
        profit_day = 0.0
        profit_year = 0.0
        profit_month = 0.0
        monthly_profit_12 = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}
        dates = date_generate()
        networkid = session.get('networkid')

        annual_profit = Payment.select().order_by(Payment.date).where(
            Payment.networkID==networkid, 
            Payment.date.between(dates[2], dates[3]))
        monthly_report = Payment.select().order_by(Payment.date).where(
            Payment.networkID==networkid, 
            Payment.date.between(dates[0], dates[1]))

        for i in annual_profit:
            monthly_profit_12[i.date.month] += i.total_amount
            profit_year += i.total_amount
        
        if monthly_report != None:
            for i in monthly_report:
                profit_month += i.total_amount

        print(monthly_profit_12)
        data['profit_day'] = profit_day
        data['profit_year'] = profit_year
        data['profit_month'] = profit_month
        data['monthly_profit_12'] = monthly_profit_12

        return jsonify(data)

@bp.route('logout', methods=['GET', 'POST'])
def Logout():
    print(session)
    session.clear()
    return redirect('/login')




# PHARMACIES BLOCK
#* ВЫВОД
@bp.route('pharmacies', methods=['GET'])
def GetPharhmacies():

    networkid = session.get('networkid')
    pharmacy = Pharmacy.select().where(
        Pharmacy.network == networkid, 
        Pharmacy.disabled == 0
    )

    return render_template('admin/pharmacies_Show.html', pharmacy=pharmacy, dropdownPharmacies=DropdownPharmacies(), name=GetName())

#* АРХИВ
@bp.route('pharmacies/archive', methods=['GET'])
def GotoArchive():

    networkid = session.get('networkid')
    disPharmacy = Pharmacy.select().where(
        Pharmacy.network == networkid, 
        Pharmacy.disabled == 1
    )

    return render_template('/admin/pharmacies_Archive.html', disPharmacy=disPharmacy, dropdownPharmacies=DropdownPharmacies(), name=GetName())

#* ОТКЛЮЧЕНИЕ
@bp.route('pharmacies/disable/<pharmacyID>', methods=['GET'])
def DisablePharmacy(pharmacyID):

    Pharmacy.update(disabled=1).where(Pharmacy.id == pharmacyID).execute()
    return redirect('/admin/pharmacies')

#* ВКЛЮЧЕНИЕ
@bp.route('pharmacies/enable/<pharmacyID>', methods=['GET'])
def EnablePharmacy(pharmacyID):

    Pharmacy.update(disabled=0).where(Pharmacy.id == pharmacyID).execute()
    return redirect('/admin/pharmacies/archive')

#* ДОБАВЛЕНИЕ
@bp.route('pharmacies/add', methods=['GET', 'POST'])
def NewPharmacy():
    if request.method == 'GET':
        return render_template('/admin/pharmacies_Add.html', dropdownPharmacies=DropdownPharmacies(), name=GetName())

    try:
        _data = request.json
        pharmacy = Pharmacy(
            disabled=False,
            date=date.today(),
            name=_data.get('name'), 
            address=_data.get('address'),
            network=session['networkid'])
        pharmacy.save()

        for i in range(11):                                                                             # Поиск и сохранение имени отдела
            temp_departments = (_data.get(f'department_{i}'))

            if temp_departments != None: 
                Department(
                    name=temp_departments, 
                    pharmacy_id=pharmacy.id
                ).save()
            else: break
            
        return jsonify({"status": "pharmacy_add"})
    
    except:
        return jsonify({"status": "error", "error": "pharmacy_add"})

#* ИЗМЕНЕНИЕ
@bp.route('pharmacies/edit/<idPharmacy>', methods=['GET', 'POST'])
def EditPharmacy(idPharmacy):
    if request.method == 'GET':
        _edit_pharmacy = Pharmacy.get_by_id(idPharmacy)
        _edit_department = Department.select().where(Department.pharmacy_id == idPharmacy)

        return render_template('admin/pharmacies_Edit.html', department=_edit_department, pharmacy=_edit_pharmacy, dropdownPharmacies=DropdownPharmacies())

    try:
        _data = request.json
        Pharmacy.update(
            network_id=session['networkid'],
            address=_data.get('address'),
            name=_data.get('name')
        ).where(Pharmacy.id == idPharmacy).execute()

        return jsonify({"status": "pharmacy_edit"})

    except:
        return jsonify({"status": "error", "error": "pharmacy_edit"})



# DRUGS BLOCK 
#* ВЫВОД СПИСКА АПТЕК         # ДЛЯ ОТОБРАЖЕНИЯ ОПРЕДЕЛЕННЫХ ПРЕПАРАТОВ
@bp.route('drugs', methods=['GET'])
def GetDrugsNetwork():
    check_session()

    netID = session['networkid']
    networks = Pharmacy.select().where(Pharmacy.network == netID, Pharmacy.disabled==0)
    return render_template('admin/drugs_Network.html', data=networks, dropdownPharmacies=DropdownPharmacies(), name=GetName())

#* ВЫВОД
@bp.route('drugs/show/<idPharmacy>', methods=['GET'])
def ShowDrugs(idPharmacy):

    drugs = Drugs.select().where(Drugs.pharmacy == idPharmacy)

    return render_template('admin/drugs_Show.html', data=drugs, dropdownPharmacies=DropdownPharmacies(), pharmacy=idPharmacy, name=GetName())

#* ДОБАВЛЕНИЕ
@bp.route('drugs/add/<idPharmacy>', methods=['GET', 'POST'])
def AddDrug(idPharmacy):
    if request.method == 'GET':
        _pharm = Pharmacy.get_by_id(idPharmacy)
        departments = Department.select().where(Department.pharmacy == idPharmacy)

        return render_template('admin/drugs_Add.html', departments=departments, pharm_name=_pharm.name, dropdownPharmacies=DropdownPharmacies(), name=GetName())

    try:
        _data = request.json
        Drugs(
            pharmacy = idPharmacy, 
            unit = _data.get('unit'), 
            name = _data.get('name'), 
            price = _data.get('price'), 
            barcode= _data.get('barcode'),
            quantity = _data.get('quantity'),
            category = _data.get('category'), 
            shelf_life = _data.get('shelf_life'), 
            department = _data.get('department'), 
            subcategory = _data.get('subcategory')).save()

        return jsonify({"status": "drug_add"})

    except:
        return jsonify({"status": "error", "error": "drug_add"})

#* ИЗМЕНЕНИЕ =============================================================== FETCH FETCH FETCH FETCH FETCH
@bp.route('drugs/edit/<idPharmacy>/<idDepartment>/<idDrug>', methods=['POST', 'GET'])
def EditDrugs(idPharmacy, idDepartment, idDrug):
    if request.method == 'GET':
        drug = Drugs.get_by_id(idDrug)

        return render_template('admin/drugs_Edit.html', drug=drug, dropdownPharmacies=DropdownPharmacies(), name=GetName())

    # try:
    _data = request.json
    print(_data)
    Drugs.update(
        department_id= idDepartment,
        pharmacy_id=idPharmacy,
        name= _data.get('name'),
        unit= _data.get('unit'),
        price= _data.get('price'),
        barcode= _data.get('barcode'),
        quantity= _data.get('quantity'),
        shelf_life= _data.get('shelf_life')
    ).where(
            Drugs.id==idDrug, 
            Drugs.pharmacy==idPharmacy,
            Drugs.department==idDepartment 
        ).execute()

    return jsonify({"status": "drug_edit"})
    
    # except:
        # return jsonify({"status": "error", "error": "drug_edit"})

#* ПЕРЕМЕЩЕНИЕ
@bp.route('drugs/transfer/<idPharmacy>/<idDepartment>/<idDrug>', methods=['GET', 'POST', 'UPDATE'])
def Transfer(idDrug, idPharmacy, idDepartment):
    drug = Drugs.get_by_id(idDrug)
    Quantity = drug.quantity

    if request.method == 'GET':
        pharmacies_list = Pharmacy.select().where(Pharmacy.disabled == 0, Pharmacy.network==session['networkid'])
        return render_template('admin/drugs_Transfer.html', pharmacies_list=pharmacies_list,dropdownPharmacies=DropdownPharmacies(), drug_pharm_dep=drug, name=GetName())

    if request.method == 'UPDATE':
        temp_department_list = []
        _pharmacy_selected = request.json['pharmacy']
        departmentList = Department.select().where(Department.pharmacy == _pharmacy_selected)
        
        for i in departmentList:
            temp_department_list.append({ i.id : i.name })

        return jsonify({'departmentList' : temp_department_list, 'disabledDepartment': idDepartment})

    try:
        _data = request.json
        _quantity = float(_data['quantity'])
        print(_data)
        if _quantity > Quantity:
            return jsonify({"status": "error", "error": "drug_exceeded_quantity_limit"})

        if _quantity == Quantity or _quantity < Quantity:
            Drugs.update(
                quantity = drug.quantity - float(_data.get('quantity'))
            ).where(Drugs.id == idDrug).execute()        
            
            Drugs(
                unit = drug.unit,
                name = drug.name,
                barcode = drug.barcode,
                category = drug.category,
                shelf_life = drug.shelf_life,
                price_sale = drug.price_sale,
                pharmacy = _data['pharmacy'],
                subcategory = drug.subcategory,
                clean_price = drug.clean_price,
                city_of_dev = drug.city_of_dev,
                department = _data['department'],
                quantity = float(_data.get('quantity')),
                price_with_discount = drug.price_with_discount,
            ).save()
    
        return jsonify({"status": "drug_transfer"})

    except:
        return jsonify({"status": "error", "error": "drug_transfer"})

#* УДАЛЕНИЕ ==================================================================
@bp.route('drugs/delete/<pharmacyID>/<drugID>', methods=['GET'])
def DeleteDrugs(pharmacyID, drugID):
    Drugs.delete_by_id(drugID)

    return redirect(f'/admin/drugs/show/{pharmacyID}', dropdownPharmacies=DropdownPharmacies(), name=GetName())







# PURCHASE BLOCK
#* ЗАКУП
@bp.route('purchase/add/<idPharmacy>', methods=['GET', 'POST', 'UPDATE', 'PUT'])
def AddPurchase(idPharmacy):
    if request.method == 'GET':
        _pharmacy = Pharmacy.get_by_id(idPharmacy)
        _departs = Department.select().where(Department.pharmacy==idPharmacy)
        nextPurchase = Purchase.select(fn.MAX(Purchase.id)+1).scalar()

        return render_template('admin/purchase_Add.html', dropdownPharmacies=DropdownPharmacies(), departments=_departs, pharmacy=_pharmacy , nextPurchase=nextPurchase, name=GetName())

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

        maxValueOfDepartment = int(str(max(Department.select(fn.MAX(Department.id)).where(Department.pharmacy == idPharmacy))))
        minValueOfDepartment = int(str(min(Department.select(fn.MIN(Department.id)).where(Department.pharmacy == idPharmacy))))

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
                    pharmacy =idPharmacy,
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
                    pharmacy_id=idPharmacy,
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

#* ВЫВОД
@bp.route('purchase/show/<idPharmacy>', methods=['GET', 'POST'])
def ShowPurchase(idPharmacy):

    purchaseList = Purchase.select().where(Purchase.pharmacy == idPharmacy)
    print(purchaseList)

    return render_template('admin/purchase_Show.html', purchaseList=purchaseList, pharmacy=idPharmacy ,dropdownPharmacies=DropdownPharmacies(), name=GetName())




#* Отчеты
@bp.route('report/show', methods=['GET', 'POST'])
def ShowReport():
    networkid = session.get('networkid')
    payment_data = Payment.select().where(Payment.networkID==networkid)
    
    return render_template('admin/reports_Show.html', payment_data=payment_data, dropdownPharmacies=DropdownPharmacies(), name=GetName())

@bp.route('report/show/<idReport>', methods=['GET', 'POST'])
def ShowReport_byID(idReport):
    getReport_byID = SoldProduct.select().where(SoldProduct.payment == idReport)

    return render_template('admin/report_Show.html', getReport_byID=getReport_byID, dropdownPharmacies=DropdownPharmacies(), name=GetName())








# EMPLOYEES BLOCK
# Сотрудники
@bp.route('employees/show', methods=['GET', 'POST'])
def GetEmpoyeesNetwork():

    networkid = session.get('networkid')
    network = Employees.select().where(Employees.network == networkid)

    return render_template('admin/employees_Network.html', network=network, dropdownPharmacies=DropdownPharmacies(), name=GetName())

# Информация о сотруднике
@bp.route('employees/show/<idEmployee>', methods=['GET', 'POST'])
def ListEmployees(idEmployee):

    passportData = Passports.get(Passports.employeeID == idEmployee)
    return render_template('admin/employees_Show.html', passport=passportData, dropdownPharmacies=DropdownPharmacies(), name=GetName())

# Добавление
@bp.route('employees/add', methods=['GET', 'POST', 'UPDATE'])
def AddEmployees():
    if request.method == 'GET':
        networkid = session.get('networkid')
        pharmaciesList = Pharmacy.select().where(Pharmacy.network == networkid, Pharmacy.disabled == 0)

        return render_template('admin/employees_Add.html', pharmaciesList=pharmaciesList, dropdownPharmacies=DropdownPharmacies(), name=GetName())

    if request.method == 'UPDATE':
        temp_department_list = []
        _department_selected = request.json['department']
        departmentList = Department.select().where(Department.pharmacy == _department_selected)
        
        for i in departmentList:
            temp_department_list.append({ i.id : i.name })

        return jsonify({'departmentList' : temp_department_list})

    try:
        data = request.json
        password = password_generate()
        networkid = session.get('networkid')

        Users(
            fio = data['surname'] +' '+ data['name'] +' '+ data['middleName'] ,
            role = data['position'],
            username = data['login'], 
            password = password,
            network  = networkid).save()
        employee = Employees(
            userID = Users.select(Users.id).where(Users.username == data['login'], Users.network==networkid),
            network = networkid,
            birthday = data['birthday'],
            position = data['position'],
            phone = data['phone'],
            pharmacy = data['pharmacy'],
            department = data['department'],
            date_of_dismissal = '',
            is_dismissed = False,
            employment_date = date.today())
        employee.save()
        
        Passports(
            employeeID = employee.id,
            passportID = data['passportID'],
            INN = data['INN'],
            date_of_Issue = data['dateOfIssue'],
            date_of_Expiration = data['dateOfExpiration'],
            place_of_Issue = data['placeOfIssue'],
        ).save()
        
        return jsonify({"status": "employee_add"})

    except KeyError:
        return jsonify({"status": "error", "error": "wrong_layout"})





#* CUSTOMERS BLOCK
#* СЕТЬ АПТЕК
@bp.route('clients', methods=['GET'])
def ShowClientNetwork():
    
    netID = session['networkid']
    networks = Pharmacy.select().where(Pharmacy.network == netID, Pharmacy.disabled==0)

    return render_template('admin/clients_Network.html', pharmacies_network=networks, dropdownPharmacies=DropdownPharmacies(), name=GetName())

#* ВЫВОД
@bp.route('clients/show/<idPharmacy>', methods=['GET'])
def ShowClients(idPharmacy):
    
    netID = session['networkid']
    clients = Clients.select().where(Clients.network==netID, Clients.pharmacy==idPharmacy)

    return render_template('admin/clients_Show.html', clients=clients, pharmacy=idPharmacy, dropdownPharmacies=DropdownPharmacies())

#* ДОБАВЛЕНИЕ
@bp.route('clients/add/<idPharmacy>', methods=['GET', 'POST'])
def AddClients(idPharmacy):
    if request.method == 'GET':
        return render_template('admin/clients_Add.html', dropdownPharmacies=DropdownPharmacies(), name=GetName())

    _data = request.json
    print(_data)
    if _data.get('balance') == None: _balance = 0
    else: _balance = _data.get('balance')

    if _data.get('email') == None: _email = 'Не указано'
    else: _email = _data.get('email')

    try:
        Clients(
            email=_email,
            balance=_balance,
            pharmacy=idPharmacy,
            fio=_data.get('name'),
            phone=_data.get('phone'),
            network=session['networkid'],
            type_client=_data.get('type_client')
        ).save()
        
        return jsonify({"status": "client_add"})

    except:
        return jsonify({"status": "error", "error": "client_add"})