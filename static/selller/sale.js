const URL_pathname = window.location.pathname
const div_table = document.querySelector('#paste')
const input_search = document.querySelector('#search')
const input_subbtn = document.querySelector('#subbtn')
const set_unit = document.querySelector('#fromGroupText')
const input_quantity = document.querySelector('#quantity')
const info_table = document.querySelector('#paste_info_table')
const name_customer = document.getElementById('customer-name')
const phone_customer = document.getElementById('customer-phone')
const amount_accepted = document.getElementById('amount-accepted')
const surrender = document.getElementById('surrender')
const button_toPaymentModal = document.getElementById('toPaymentModal')
const button_payment = document.getElementById('payment')
const select_payment_type = document.getElementById('payment-type')


const modal_error = document.getElementById('modal-error')

const radioName = document.getElementById('radioName')
const radioBarcode = document.getElementById('radioBarcode')
const radioOriginCustomer = document.getElementById('origin-customer')
const radioRegularCustomer = document.getElementById('regular-customer')

let search_status = 'by_name'

let totalSumm = 0
let totalQuantity = 0
let soldProducts = []

let products = []
let serverProducts = null
let barcode = ''
let quantity = ''

let barcode_access = false
let quantity_access = false

let errorText = 'Заполните поля правильно'
let errorTexts = {
    NoProducts: "Вы ничего не добавили в список",
    WrongEnter: "Заполните поля правильно",
    DiscountOverflow: "Скидка на товар не должна превышать 100%",
    EmptyAcceptedAmount: "EmptyAcceptedAmount",
    AmountAcceptedIsLessThanTotal: "Принятая сумма меньше, чем итоговая",
}



/* функции */
const calculateForInfoBar = () => {
    totalSumm = 0
    totalQuantity = 0

    products.forEach(e => totalQuantity += e.quantity)
    products.forEach(e => totalSumm += ((100 - +e.val) * (+e.price_sale * +e.quantity)) / 100)
    document.querySelector('#sum span').innerHTML = totalSumm.toFixed(2)
    document.querySelector('#qnt span').innerHTML = totalQuantity.toFixed(2)
}
const modalWindowSuccess = () => {
    $('#modalInfo').modal({ backdrop: 'static', keyboard: false })          // Call modal window
    setTimeout(() => {
        $('#modalInfo').modal('hide')
        window.location.reload()
    }, 1800);
}
const modalWindowError = e => {
    modal_error.innerHTML = errorTexts[e]

    $('#modalError').modal({ backdrop: 'static', keyboard: false })          // Call modal window
    setTimeout(() => {
        $('#modalError').modal('hide')
    }, 1050);
}
const drug_info = data => {
    out = `
        <h4>${data.name}</h4>
        <h4>${data.country_of_origin}</h4>
        <h4>${data.server_quantity}</h4>
        <h4>${data.price_sale}</h4>`
    document.getElementById('info').innerHTML = out
}
const refresh = () => {
    document.querySelectorAll(".discount-products").forEach(element => {
        products.find(e => { if (+e.id == +element.id) e.val = element.value; })
    })
}


const quantityAccess = value => {
    quantity_stataus = value ? 'is-valid' : 'is-invalid'
    input_quantity.classList.replace(input_quantity.classList[0], quantity_stataus)
    set_unit.innerHTML = value ? serverProducts.unit : ""
    quantity_access = value
}
const barcodeAccess = value => {
    if (value) {
        input_search.classList.add('is-valid')
        input_search.classList.remove('is-invalid')
    } else {
        input_search.classList.remove('is-valid')
        input_search.classList.add('is-invalid')
    }
    barcode_access = value
}


const deleteProduct = id => {
    products = products.filter(prod => prod.id !== +id).concat()
    soldProducts = soldProducts.filter(prod => prod.id !== +id).concat()

    if (quantity !== '')
        quantityAccess(true)
    check()
    render()
}
const check = () => {
    if (serverProducts !== null)
        if (quantity > serverProducts.server_quantity) {
            quantityAccess(false)
            errorText = 'Больше низя'
        }

    inpType = input_search.getAttribute('type')

    if (inpType === 'text') {
        if (serverProducts !== null && products.find(prod => prod.name === barcode))
            if (products.find(prod => prod.name === barcode).quantity + quantity > serverProducts.server_quantity) {
                quantityAccess(false)
                errorText = 'Больше низя'
            }
    }
    if (inpType === 'number') {
        if (serverProducts !== null && products.find(prod => prod.barcode === barcode))
            if (products.find(prod => prod.barcode === barcode).quantity + quantity > serverProducts.server_quantity) {
                quantityAccess(false)
                errorText = 'Больше низя'
            }
    }
}





const changeQuantity = value => {
    if (value === '' || value === 0 || serverProducts === null)
        quantityAccess(false)
    else
        quantityAccess(true)

    input_quantity.value = value
    quantity = value

    if (serverProducts === null) {
        input_quantity.value = ''
        quantity = ''
    }
    if (value === 0) {
        input_quantity.value = ''
        quantity = ''
    }

    check()
}
const changeBarcode = value => {
    search_input.value = value.toString()
    barcode = value
}

const fetchProduct = () => {
    fetch(URL_pathname, {
        method: 'POST',
        body: JSON.stringify({ type: search_status, value: input_search.value }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    })
        .then(res => res.json())
        .then(json => {
            console.log(json)
            if (json.error === 'notExists') {
                serverProducts = null
                changeQuantity('')
                quantityAccess(false)
                barcodeAccess(false)
                errorText = 'Данные не найдены'
                check()
            }
            else {
                serverProducts = json
                changeQuantity(1)
                quantityAccess(true)
                barcodeAccess(true)
                drug_info(json)
                check()
                errorText = 'Заполните поля правильно'
            }
        })
}

const add = () => {
    check()

    if (!barcode_access || !quantity_access)
        return alert(errorText)

    let product
    inpType = input_search.getAttribute('type')

    if (inpType === 'text') {
        if (!products.find(product => product.name === barcode))
            products.push({ ...serverProducts })
        product = products.find(prod => prod.name === barcode)
    }
    if (inpType === 'number') {
        if (!products.find(product => product.barcode === barcode))
            products.push({ ...serverProducts })
        product = products.find(prod => prod.barcode === barcode)
    }
    product.quantity += quantity


    if (!soldProducts.find(e => e.id == +product.id)) {
        idT = product.id
        priceSaleT = product.price
        discountT = product.discount
        quantityT = product.quantity
        sQuantityT = product.server_quantity

        soldProducts.push({
            'id': idT,
            'discount': 0,
            'quantity': quantityT,
            'server_quantity': sQuantityT,
            'price_sale': priceSaleT
        })
    }
    else {
        soldProducts.find(e => {
            if (e.id == +product.id) {
                e.quantity += quantity
            }
        })
    }

    render()
    check()
}

const render = () => {

    refresh()

    const out = products.map(product =>
        `<tr>
            <th>0</th>
            <th>${product.name}</th>
            <th>${product.quantity.toFixed(2)} ${product.unit}</th>
            <th>${product.price_sale} cом.</th>
            <th class="w-10"><input class="form-control discount-products" value="${product.val}" min="0.1" step="0.1" type="number" id="${product.id}"></th>
            <th>
                <button class="btn btn-danger remove-product" id=${product.id}><i class="fas fa-trash"></i></button>
            </th>
        </tr>`
    )

    div_table.innerHTML = out.join('')

    const remove_btns = document.querySelectorAll('.remove-product')

    document.querySelectorAll(".discount-products").forEach(element => {
        element.addEventListener('input', () => {
            if (+element.value > 100) {
                element.value = 100
                modalWindowError('DiscountOverflow')
            }
            refresh()
            calculateForInfoBar()
        })
    })
    remove_btns.forEach(btn => {
        btn.addEventListener('click', e => {
            deleteProduct(e.target.getAttribute('id'))
        })
    })
    calculateForInfoBar()
}



/* события на сайте */
input_search.addEventListener('input', e => {
    const inpType = e.target.getAttribute('type')
    const val = inpType === 'text' ? e.target.value : +e.target.value
    changeBarcode(val)
    fetchProduct()
})
input_quantity.addEventListener('input', e => {
    changeQuantity(e.target.value !== '' ? +e.target.value : '')
})

input_subbtn.addEventListener('click', e => {
    e.preventDefault()
    add()
})

radioBarcode.addEventListener('click', () => {
    search_input.placeholder = 'ISBN-Код'
    search_input.setAttribute('type', 'number')
    search_status = 'by_barcode'
    fetchProduct()
})
radioName.addEventListener('click', () => {
    search_input.placeholder = 'Наименование'
    search_input.setAttribute('type', 'text')
    search_status = 'by_name'
    fetchProduct()
})



amount_accepted.addEventListener('input', () => {
    surrender.value = (+amount_accepted.value - +totalSumm).toFixed(2)
})

button_toPaymentModal.addEventListener('click', () => {
    if (products.length == 0)
        modalWindowError('NoProducts')

    else {
        $('#modalPayment').modal('show')
        document.querySelectorAll(".discount-products").forEach(element => {
            soldProducts.find(e => {
                if (+e.id == +element.id) {
                    e.discount += +element.value
                }
            })
        })
    }
})

button_payment.addEventListener('click', () => {
    if (amount_accepted.value == 0 || amount_accepted.value == '')
        modalWindowError('EmptyAcceptedAmount')
    if (amount_accepted.value < totalSumm)
        modalWindowError('AmountAcceptedIsLessThanTotal')

    else {
        secondary_data = {
            'total_amount': totalSumm,
            'total_quantity_products': totalQuantity,
            'customer': customerID,
            'amount_accepted': amount_accepted.value,
            'surrender': surrender.value,
            'payment_type': select_payment_type.value,
        }

        fetch('/selller/payment/pay', {
            method: 'POST',
            body: JSON.stringify({ 'products': soldProducts, 'secondary_data': secondary_data }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        })
        $('#modalPayment').modal('hide')
        modalWindowSuccess()
    }
})