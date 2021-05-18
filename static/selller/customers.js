let customerID = -1

name_customer.addEventListener('change', () => {
    phone_customer.selectedIndex = name_customer.selectedIndex
})

radioOriginCustomer.addEventListener('click', () => {
    name_customer.disabled = true
    customerID = -1
})

radioRegularCustomer.addEventListener('click', () => {
    name_customer.disabled = false
    customerID = +name_customer.selectedOptions[0].id+1
})