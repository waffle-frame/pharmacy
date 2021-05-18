const report_row = document.querySelectorAll('.report-row')
let id = null

report_row.forEach(i => {
    i.addEventListener("click", () => {
        id = i.getAttribute('id')
        window.location.href = `/selller/show/report/${+id}`;
    })
});