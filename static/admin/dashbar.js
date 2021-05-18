const URL_pathname = window.location.pathname
var values = []
var ctx = document.getElementById("myAreaChart")
const profit_year = document.getElementById('profit_year_value')
const profit_month = document.getElementById('profit_month_value')

const fetching_data = async () => {
    await fetch(
        URL_pathname, {
        method: 'UPDATE',
        headers: { "Content-type": "application/json; charset=UTF-8" }
    })
        .then(response => response.json())
        .then(json => update_chart(json))
}

const update_chart = json => {
    profit_month.innerHTML = json['profit_month'].toFixed(2)
    profit_year.innerHTML = json['profit_year'].toFixed(2)
    Object.values(json['monthly_profit_12']).forEach(element => {
        values.push(parseFloat(element))
    });
    setTimeout(() => {myLineChart.update()}, 100)
}

document.addEventListener('load', fetching_data())