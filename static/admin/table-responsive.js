const report_row = document.querySelectorAll('.report-row')
const employee_row = document.querySelectorAll('.employee-row')

let id = null

report_row.forEach(i => {
    i.addEventListener("click", () => {
        id = i.getAttribute('id')
        window.location.href = `/admin/report/show/${+id}`;
    })
});

employee_row.forEach(i => {
    i.addEventListener("click", () => {
        id = i.getAttribute('id')
        window.location.href = `/admin/employees/show/${+id}`;
    })
});