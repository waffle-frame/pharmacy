const submit_button = document.getElementById('modalSubmit')
const modal_success = document.getElementById('modal-success')
const modal_error = document.getElementById('modal-error')
const URL_pathname = window.location.pathname
let length_of_departments = document.querySelectorAll('.input-department').length
let forms = document.querySelectorAll('.checkToValid')
let last_value = window.location.pathname.length-1
let objectsForServer = {}
let Value = true
let Numbr = true
let Phone = true
let Departments
let Departmnets_quantity
let i

// Texts for modal window
const Errors = {
    client_add: 'Произошла ошибка при добавлении клиента',
    drug_add: 'Произошла ошибка при добавлении препарата',
    drug_edit: 'Произошла ошибка при попытке редактирования данных препарата',
    drug_transfer: 'Произошла ошибка при попытке переместить препарат',
    drug_exceeded_quantity_limit: 'Перемещаемое количество превышает существующую',
    employee_add: 'Произошла ошибка при добавлении нового сотрудникa',
    pharmacy_add: 'Произошла ошибка при добавлении создании новой аптеки',
    pharmacy_edit: 'Произошла ошибка при обновлении данных аптеки',
    purchase_add: 'Произошла ошибка при попытке закупить товар',
    purchase_error_find_drug: 'Сгенерируйте штрих-код, или введите правильный',
    purchase_empty_department_fields: 'Необходимо заполнить минимум 1 поле отделов',
    purchase_wrong_value_quantity_on_departments: 'Неправильное распределение по отделам',


    departments_outnumber: 'Количество отделов не должно быть больше 10',
    incorrect_discount_price: 'Цена закупа со скидкой не должна превосходить чистую цену закупа',
    wrong_layout: 'Раскладка клавиатуры должна быть на русском языке',
    empty_field: 'Заполните все поля!',
    value_below_zero: 'Цена продажи не должна !',
    value_below_zero: 'Значение не должно быть ниже нуля!',
    wrong_phone_format: 'Моб.телефон не соответствует формату XX-XXX-XXXX',
}
const Pass = {
    client_add: 'Клиент успешно добавлен',
    purchase_add: 'Закуп был успешно произведен',
    drug_add: 'Препарат успешно добавлен',
    drug_edit: 'Данные препарата были успешно обновлены',
    drug_transfer: 'Преперат был успешно перенесен',
    employee_add: 'Сотрудник успешно добавлен в базу данных аптеки',
    pharmacy_add: 'Аптека успешно создана',
    pharmacy_edit: 'Данные аптеки были успешно обновлены',
}



const fetching = async data => {
    await fetch(URL_pathname, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    })
        .then(response => response.json())
        .then(json => {
            status = json.status
            console.log(json, status)
            if (status != 'error') modalWindowSuccess(status)
            else {
                let error = json.error
                modalWindowError(error)
            }
        })
}

submit_button.addEventListener('click', e => {
    e.preventDefault()
    forms = document.querySelectorAll('.checkToValid')
    Departments=0
    Departmnets_quantity=0

    for (i of forms) {
        if ((URL_pathname == `/admin/purchase/add/${URL_pathname[last_value]}` && i.classList[0]=='input-department')
            || (URL_pathname == `/selller/purchase/add` && i.classList[0]=='input-department')) {
                console.log('sad')
            if (i.value == '' || i.value == 0) {
                Departments += 1} 
            Departmnets_quantity+=+i.value
        continue}

        if (i.value === "" && i.hidden != true) { Value = false; break; }
        else Value = true
        if (i.value <= 0 && i.hidden != true) { Numbr = false; break; }
        else Numbr = true
        if (i.id == 'phone' && (i.value.length < 9 || i.value.length > 9)) { Phone = false; break; }
        else Phone = true
    }

    if      (!Value) { modalWindowError('empty_field') }
    else if (!Numbr) { modalWindowError('value_below_zero') }
    else if (!Phone) { modalWindowError('wrong_phone_format') }
    else if ((URL_pathname == `/admin/purchase/add/${URL_pathname[last_value]}` && Departments==length_of_departments)
            || (URL_pathname == `/selller/purchase/add` && Departments==length_of_departments)) { 
        modalWindowError('purchase_empty_department_fields'); console.log('fifiiffiifififiififiiffifif') }
    else if ((URL_pathname == `/admin/purchase/add/${URL_pathname[last_value]}` && Departmnets_quantity!=document.getElementById('quantity').value)
            || (URL_pathname == `/selller/purchase/add` && Departmnets_quantity!=document.getElementById('quantity').value)) {
        modalWindowError('purchase_wrong_value_quantity_on_departments'); console.log('elsesleslelslelselslelselle')
    }
    else {
    submit_button.disabled = true
    forms.forEach(tmp => {
        field = tmp.getAttribute('id')
        value = tmp.value
        objectsForServer[field] = value})

    fetching(objectsForServer)
}})



// Modal events
const modalWindowSuccess = (status) => {
    console.log(status)
    modal_success.innerHTML = Pass[status]

    $('#modalInfo').modal({ backdrop: 'static', keyboard: false })          // Call modal window
    setTimeout(() => {
        $('#modalInfo').modal('hide')
        location.href = document.referrer; 
        return false;
        }, 1800);
}
const modalWindowError = (status) => {
    modal_error.innerHTML = Errors[status]
    submit_button.disabled = false

    $('#modalError').modal({ backdrop: 'static', keyboard: false })          // Call modal window
    setTimeout(() => {
        $('#modalError').modal('hide')
    }, 1750);
}