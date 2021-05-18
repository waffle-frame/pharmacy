String.prototype.scapitalize = function () {
    return this.charAt(0).toUpperCase() + this.slice(1).toLowerCase()
}

const login = document.getElementById('login')
const pharmacy = document.getElementById('pharmacy')
const next_according = document.getElementById('next')
const department = document.getElementById('department')
const middleName = document.getElementById('middleName')
const headingOne = document.getElementById('headingOne')
const headingTwo = document.getElementById('headingTwo')
const no_middleName = document.getElementById('no-middleName')
const passport_according = document.getElementById('passport-data')
const personal_according = document.getElementById('personal-data')
const auto_generate = document.getElementById('auto-generate_login')
var vocabluary = {
    "Ё": "YO", "Й": "I", "Ц": "TS", "У": "U", "К": "K", "Е": "E", "Н": "N", "Г": "G", "Ш": "SH", "Щ": "SCH", "З": "Z", "Х": "H", "Ъ": "'",
    "ё": "yo", "й": "i", "ц": "ts", "у": "u", "к": "k", "е": "e", "н": "n", "г": "g", "ш": "sh", "щ": "sch", "з": "z", "х": "h", "ъ": "'",
    "Ф": "F", "Ы": "I", "В": "V", "А": "a", "П": "P", "Р": "R", "О": "O", "Л": "L", "Д": "D", "Ж": "ZH", "Э": "E", "ф": "f", "ы": "i", "в": "v",
    "а": "a", "п": "p", "р": "r", "о": "o", "л": "l", "д": "d", "ж": "zh", "э": "e", "Я": "Ya", "Ч": "CH", "С": "S", "М": "M", "И": "I", "Т": "T",
    "Ь": "'", "Б": "B", "Ю": "YU", "я": "ya", "ч": "ch", "с": "s", "м": "m", "и": "i", "т": "t", "ь": "'", "б": "b", "ю": "yu"
}





// functions
const translate = (word) => {
    return word.split('').map(function (char) {
        return vocabluary[char] || char;
    }).join("");
}

const fetching_department_list = async pharmacy => {
    departmentt = pharmacy.value
    convertToJSON = { "department": departmentt }

    await fetch(
        URL_pathname, {
        method: 'UPDATE',
        body: JSON.stringify(convertToJSON),
        headers: { "Content-type": "application/json; charset=UTF-8" }
    })
        .then(response => response.json())
        .then(json => res(json['departmentList']))
}

const res = (department_list) => {
    let out = ''

    ids = department_list.map(el => Object.keys(el)[0])
    names = department_list.map(el => Object.values(el)[0])

    for (let index = 0; index < ids.length; index++) {
        out += `<option value=${ids[index]}> ${names[index]} </option>`
    }
    department.innerHTML = out
}

const changeLogin = () => {
    let year_of_birthday = new Date(Date.parse(document.querySelector('#birthday').value)).getFullYear()
    let no_translate_login = document.querySelector('#surname').value[0].toUpperCase() + document.querySelector('#name').value.scapitalize() + year_of_birthday
    let translate_login = translate(no_translate_login)
    login.value = translate_login
}

const checkFieldsToValid = () => {
    forms = document.querySelectorAll('.personal')
    for (i of forms) {
        if (i.value === "" && i.hidden != true) { Value = false; break; }
        else Value = true
        if (i.value <= 0 && i.hidden != true) { Numbr = false; break; }
        else Numbr = true
        if (i.id == 'phone' && (i.value.length < 9 || i.value.length > 9)) { Phone = false; break; }
        else Phone = true
    }
    if (!Value) { modalWindowError('empty_field'); return false }
    else if (!Numbr) { modalWindowError('value_below_zero'); return false }
    else if (!Phone) { modalWindowError('wrong_phone_format'); return false }
    else return true
}



// events
auto_generate.addEventListener('click', () => {
    if (auto_generate.checked == true) {
        login.disabled = true
        changeLogin()
    }
    else login.disabled = false
})
no_middleName.addEventListener('click', () => {
    if (no_middleName.checked == true) middleName.hidden = true
    else middleName.hidden = false
})

next_according.addEventListener('click', () => {
    let next = checkFieldsToValid()
    if (next) {
        headingOne.classList.remove('bg-primary') ; headingOne.classList.add('bg-gray-500')
        headingTwo.classList.remove('bg-gray-300') ; headingTwo.classList.add('bg-primary')
        passport_according.classList.remove('text-gray-900'); passport_according.classList.add('text-white')
        passport_according.disabled = false
        $('#collapseTwo').collapse('show')
    }
    else {
        $('#collapseTwo').collapse('hide')
        headingOne.classList.add('bg-primary') ; headingOne.classList.remove('bg-gray-500')
        headingTwo.classList.add('bg-gray-300') ; headingTwo.classList.remove('bg-primary')
        passport_according.classList.add('text-gray-900'); passport_according.classList.remove('text-white')
        passport_according.disabled = true
    }
})

document.getElementById('surname').addEventListener('input', () => {
    if (auto_generate.checked == true) changeLogin()
})
document.getElementById('name').addEventListener('input', () => {
    if (auto_generate.checked == true) changeLogin()
})
document.getElementById('birthday').addEventListener('input', () => {
    if (auto_generate.checked == true) changeLogin()
})

personal_according.addEventListener('click', () => {
    headingOne.classList.add('bg-primary') ; headingOne.classList.remove('bg-gray-500')
    headingTwo.classList.add('bg-gray-300') ; headingTwo.classList.remove('bg-primary')
    passport_according.classList.add('text-gray-900'); passport_according.classList.remove('text-white')
    passport_according.disabled = true
})

pharmacy.addEventListener('change', () => { fetching_department_list(pharmacy) })