const unit_box = document.getElementById('unit')
const name_input = document.getElementById('name')
const barcode_input = document.getElementById('barcode')
const quantity_input = document.getElementById('quantity')
const shelf_life_input = document.getElementById('shelf_life')
const date_input = document.getElementById('shelf_life')
const generate_barcode = document.getElementById('generate-barcode')
const walrus = document.getElementById('walrus')

const alert_window = document.getElementById('alert_oops')
const next_on_alert = document.getElementById('next-on-alert')

const modalDrugWith_ISBN = document.getElementById('modalDrugWith-ISBN-code')
const modalDrugWithout_ISBN = document.getElementById('modalDrugWithout-ISBN-code')
const modalDrugWith_ISBN_save = document.getElementById('modalDrugWith-ISBN-save')
const modalDrugWith_ISBN_close = document.getElementById('modalDrugWith-ISBN-close')
const modalDrugWithout_ISBN_save = document.getElementById('modalDrugWithout-ISBN-save')
const modalDrugWithout_ISBN_close = document.getElementById('modalDrugWithout-ISBN-close')

let quantity = document.getElementById('quantity')
let total_sum = document.getElementById('total_sum')
let price_sale = document.getElementById('price_sale')
let clear_price = document.getElementById('clear_price')
let discount_percent = document.getElementById('discount_percent')
let price_with_discount = document.getElementById('price_with_discount')




// - - - - - - - - - - - - - - - - - - - - - - - - - - - \\
// Function
const fetch_get_data = async (value, field) => {
    convertToJSON = {}
    convertToJSON[field] = value

    await fetch(
        URL_pathname, {
        method: 'UPDATE',
        body: JSON.stringify(convertToJSON),
        headers: { "Content-type": "application/json; charset=UTF-8" }
    })
        .then(response => response.json())
        .then(json => change_fields(json, field))
}
const fetch_generate_barcode = async () => {
    await fetch(
        URL_pathname, {
        method: 'PUT',
        body: JSON.stringify(1),
        headers: { "Content-type": "application/json; charset=UTF-8" }
    })
        .then(response => response.json())
        .then(json => get_generate_barcode(json))
}

const disable_fields = bool => {
    shelf_life.disabled = bool
    name_input.disabled = bool
    clear_price.disabled = bool
    quantity_input.disabled = bool
    price_with_discount.disabled = bool
}

const get_generate_barcode = async barcode => {
    document.getElementById('modalDrugWithout-ISBN-barcode').value = barcode['generated_barcode']
    $('#modalDrugWithout-ISBN-code').modal({ backdrop: 'static', keyboard: false })
}
const calculate_discount_price = () => {
    var calc = +quantity.value * +price_with_discount.value
    total_sum.value = calc.toFixed(2)
}
const calculate_discount_percent = () => {
    var calc = 100 - ((100 * +price_with_discount.value) / +clear_price.value)
    discount_percent.value = calc.toFixed(2) + ' %'
}
const calculate_walrus = () => {
    var walrusT = +price_with_discount.value - +price_sale.value
    if (walrusT <= 0 ) modalWindowError('')
    walrus.value = walrusT
    
}
const change_fields = (data, field) => {
    convert = { 'barcode': 'name', 'name': 'barcode' }

    if (data['status'] != 'noExsists') {
        console.log(data, field)
        document.getElementById(convert[field]).value = data[convert[field]]
        unit_box.innerHTML = data['unit']
        $('#alert_oops').fadeOut(200)
        disable_fields(false)
        document.getElementById('name').disabled = true

        generate_barcode.hidden = true

    }
    else if (data['status'] == 'noExsists') {
        if (barcode_input.value.length == 13) {
            disable_fields(true)
            $('#alert_oops').fadeIn(250)
            generate_barcode.hidden = true
        }
        else {
            generate_barcode.hidden = false
            disable_fields(false)
            $('#alert_oops').fadeOut(200)
        }
        document.getElementById('name').disabled = false
        unit_box.innerHTML = ''
    }
}



// - - - - - - - - - - - - - - - - - - - - - - - - - - - \\
// Events
next_on_alert.addEventListener('click', () => {
    $('#alert_oops').fadeOut(250)
    document.getElementById('modalDrugWith-ISBN-barcode').value = barcode_input.value
    $('#modalDrugWith-ISBN-code').modal({ backdrop: 'static', keyboard: false })
})

modalDrugWith_ISBN_save.addEventListener('click', () => {
    modal_input = document.querySelectorAll('.checkToValidWith-ISBN')
    for (let i of modal_input) {
        if (i.value == '') { modalDrugWith_ISBN_Value = false; break }
        else modalDrugWith_ISBN_Value = true
    }

    if (modalDrugWith_ISBN_Value == false) {
        modalWindowError('empty_field')
    }
    else {
        disable_fields(false)
        barcode_input.value = +document.getElementById('modalDrugWith-ISBN-barcode').value
        name_input.value = document.getElementById('modalDrugWith-ISBN-name').value
        unit_box.innerHTML = document.getElementById('modalDrugWith-ISBN-unit').value
        barcode_input.disabled = true
        name_input.disabled = true

        unit = document.getElementById('modalDrugWith-ISBN-unit')
        ctg = document.getElementById('modalDrugWith-ISBN-category')
        subctg = document.getElementById('modalDrugWith-ISBN-subcategory')

        let ss =`<input id="${ctg.name}" class="checkToValid" value="${ctg.value}">
                <input id="${unit.name}" class="checkToValid" value="${unit.value}">
                <input id="${subctg.name}" class="checkToValid" value="${subctg.value}">`
        modal_data_hidden.innerHTML = ss
        $('#modalDrugWith-ISBN-code').modal('hide')
        generate_barcode.hidden = true
    }
})
modalDrugWith_ISBN_close.addEventListener('click', () => {
    $('#alert_oops').fadeIn(250)
})

modalDrugWithout_ISBN_save.addEventListener('click', () => {
    modal_input = document.querySelectorAll('.checkToValidWithout-ISBN')
    for (let i of modal_input) {
        if (i.value == '') { modalDrugWithout_ISBN_Value = false; break }
        else modalDrugWithout_ISBN_Value = true
    }

    if (modalDrugWithout_ISBN_Value == false) {
        modalWindowError('empty_field')
    }
    else {
        disable_fields(false)
        barcode_input.value = +document.getElementById('modalDrugWithout-ISBN-barcode').value
        name_input.value = document.getElementById('modalDrugWithout-ISBN-name').value
        unit_box.innerHTML = document.getElementById('modalDrugWithout-ISBN-unit').value
        barcode_input.disabled = true
        name_input.disabled = true

        unit = document.getElementById('modalDrugWithout-ISBN-unit')
        ctg = document.getElementById('modalDrugWithout-ISBN-category')
        subctg = document.getElementById('modalDrugWithout-ISBN-subcategory')

        let ss=`<input id="onlyForThisPharmacy" class="checkToValid" value="True">
                <input id="${ctg.name}" class="checkToValid" value="${ctg.value}">
                <input id="${unit.name}" class="checkToValid" value="${unit.value}">
                <input id="${subctg.name}" class="checkToValid" value="${subctg.value}">`
        modal_data_hidden.innerHTML = ss
        $('#modalDrugWithout-ISBN-code').modal('hide')
        generate_barcode.hidden = true
    }
})


barcode_input.addEventListener('input', () => {
    fetch_get_data(barcode_input.value, 'barcode')
})
barcode_input.addEventListener('change', () => {
    fetch_get_data(barcode_input.value, 'barcode')
})

name_input.addEventListener('input', () => {
    fetch_get_data(name_input.value, 'name')
})
name_input.addEventListener('change', () => {
    fetch_get_data(name_input.value, 'name')
})

$('#generate-barcode').popover({ trigger: "hover" })


quantity.addEventListener('input', () => {
    calculate_discount_price()
})
clear_price.addEventListener('input', () => {
    if (+price_with_discount.value > +clear_price.value) {
        modalWindowError('incorrect_discount_price')
        price_with_discount.value = +clear_price.value
    }
    else if (clear_price.value != '')
        calculate_discount_percent()
    calculate_discount_price()
})
price_sale.addEventListener('input', () => {
    calculate_walrus()
})
price_with_discount.addEventListener('input', () => {
    if (+price_with_discount.value > +clear_price.value) {
        price_with_discount.value = +clear_price.value

        modalWindowError('incorrect_discount_price')
    }
    else if (+clear_price.value != '')
        calculate_discount_percent()
    calculate_discount_price()
    calculate_walrus()
})


date_input.addEventListener('input', () => {
})



const popover = () => {
    console.log('eter   ')
    $('#generate-barcode').popover('show')
    setTimeout(() =>
        {$('#generate-barcode').popover('hide')},1700
)}
generate_barcode.addEventListener('click', () => {
    fetch_generate_barcode()
})
document.addEventListener('load', popover()) 