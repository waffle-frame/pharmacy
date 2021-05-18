const pharmacy = document.getElementById('pharmacy')
const department = document.getElementById('department')

const fetching_department_list = async pharmacy => {
    pharmacy = pharmacy.value
    convertToJSON = { "pharmacy": pharmacy }

    await fetch(
        URL_pathname, {
        method: 'UPDATE',
        body: JSON.stringify(convertToJSON),
        headers: { "Content-type": "application/json; charset=UTF-8" }
    })
        .then(response => response.json())
        .then(json => res(json))
}

function res(department_list) {
    let out = ''
    ids = department_list['departmentList'].map(el => Object.keys(el)[0])
    names = department_list['departmentList'].map(el => Object.values(el)[0])
    disable_department = department_list['disabledDepartment']
    
    for (let index=0; index<ids.length; index++) {
        if (ids[index] === disable_department)
            out += `<option disabled value=${ids[index]}> ${names[index]} </option>`
        else 
            out += `<option value=${ids[index]}> ${names[index]} </option>`
    }

    department.innerHTML = out
}

pharmacy.addEventListener('change', () => {  fetching_department_list(pharmacy)  })
document.addEventListener('load', fetching_department_list(pharmacy))