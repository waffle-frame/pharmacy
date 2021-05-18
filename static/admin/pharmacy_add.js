var items = 0
const add_to = document.getElementById('more-department')
const btn_add_department = document.getElementById('add-department')


// Functions
const add_department = () => {
    out = `
        <div class="form-group d-flex justify-content-around block" id="delete-department_${items + 1}">
            <button class="btn btn-danger mr-3 delete" type="button" onclick="remove(${items + 1})"><i class="fas fa-trash text-white"></i></button>
            <input class="department-input checkToValid form-control col" type="text" id="department_${items + 1}" placeholder="Отдел №${items+2}">
        </div>`

    items++
    add_to.insertAdjacentHTML('beforeend', out)
}

const remove = div_block => {
    set_div_block = `delete-department_${div_block}`
    document.getElementById(set_div_block).remove()
    items--    
    rename()
}

const rename = () => {
    for (let i=0; i<=$(".department-input").length-1; i++) {

        document.querySelectorAll('.delete')[i].setAttribute('onclick', `remove(${i+1})`)
        document.querySelectorAll('.block')[i].setAttribute('id', `delete-department_${i+1}`)
        document.querySelectorAll(".department-input")[i].setAttribute('id', `department_${i+1}`)
        document.querySelectorAll(".department-input")[i].setAttribute('placeholder', `Отдел №${i+2}`)
}}

const check_fields = () => {
    for (let i of $('.department-input')) {
        console.log(i)
    }
}

// Event
btn_add_department.addEventListener('click', () => {
    if ($('.department-input').length < 9) add_department()
    else modalWindowError('departments_outnumber')
})