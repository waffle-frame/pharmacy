
// -------------------------------------------------------------------- Na-Sa
$(document).ready(function() {
    var vaar = []
    var strr = ''
    var temp = 1
    options = [ [],
        ['Дыхательная система', 'Акушерство, гинекология', 'Аллергия', 'Анестезия, реанимация', 'Антибиотики', 'Болезни крови', 'Боль, температура', 'Геморрой', 'Глаза', 'Глисты, вши, чесотка', 'Диабет', 'Желудок, кишечник, печень',
            'Зубы и рот', 'Иммунная система', 'Кожа', 'Мочеполовая система', 'Нарушения обмена веществ', 'Неврология, психиатрия', 'Обеззараживающие средства', 'Онкология', 'Отравления', 'Питательные смеси', 'Противовирусные средства',
            'Противогрибковые средства', 'Сердечно-сосудистые', 'Трихомоноз и малярия', 'Ухо, горло, нос', 'Эндокринология', 'Разные средства', 'Миорелаксант'
        ],  
        ['Витамины и минералы', 'Биологически активные добавки', 'Похудение'],
        ['Травы', 'Чаи', 'Сборы', 'Сиропы', 'Эликсиры'],
        ['Соски,пустышки', 'Товары для мам', 'Детская гигиена', 'Детское питание', 'Детская косметика', 'Детские подгузники', 'Приборы для вскармливания', 'Аксессуары для детского питания', 'Игрушки,предметы ухода за детьми'],
        ['Антисептики', 'Аптечки', 'Перевязка', 'Пластыри'],
        ['Термометры', 'Медтехника', 'Тонометры', 'Сахарный диабет (мед. прибор)', 'Дыхательная система (мед. прибор)', 'Уход за полостью рта (мед. приборы,изделия)'],
        ['Спринцовка', 'Пластыри', 'Иглы и шприцы', 'Рентгеноконтрастное', 'Презервативы и лубриканты', 'Другие медицинские изделия']
    ]

    $("#category").change(function() {
        var val = $(this).val();
        for (let i of options[val]) {
            temp += 1
            strr += "<option value='" + temp + "'>" + i + "</option>"
        }
        $("#subcategory").html(strr);
        // document.querySelector("#subcatecory").innerHTML = strr
        strr = ''
        temp = 0
    });
});
// --------------------------------------------------------------------


// -------------------------------------------------------------------- Na-Sa
$("#transferPharmacy").on('change', e => {
    let _pharmacy = document.getElementById('transferPharmacy').value               // Получение выбранного значения
    let _convertToJSONToSend = { pharmacy: _pharmacy }

    fetch('/transfer/data', {                                                       // Отправляем запрос на обработку
            method: 'POST',
            body: JSON.stringify(_convertToJSONToSend),
            headers: { "Content-type": "application/json; charset=UTF-8" }})

        .then(response => response.json())                                          // Конверт полученных данных от сервера в JSON
        .then(json => {                                                            // Переобразование в данных в HTML-код
            let ChangedListDepartment = json.map(option =>
                `<option value="${option.id}" >${option.name}</option>`)
            document.querySelector("#transferSubcategory").innerHTML = ChangedListDepartment
        })

        .catch(err => console.log('Request Failed', err));
})
// -------------------------------------------------------------------- Na-Sa 


$('#price').on('input', () => {
    let price = document.getElementById('price').value
    let quantity = document.getElementById('quantity').value
    let printSum = document.getElementById('summ')
    
    calculate = +price * +quantity

    printSum.value = calculate
})
$('#quantity').on('input', () => {
    let price = document.getElementById('price').value
    let quantity = document.getElementById('quantity').value
    let printSum = document.getElementById('summ')
    
    calculate = +price * +quantity

    printSum.value = calculate
})