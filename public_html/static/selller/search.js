const search_input = document.getElementById('search')
const search_box = document.getElementById('searchBox')
const filtred_items_paste = document.getElementById('filtred-items-paste')
let prodd

/* functions */
const fetch_search = () => {
	fetch(URL_pathname, {
		method: 'PUT',
		body: JSON.stringify({ type_search: search_status, value: search_input.value }),
		headers: {
			"Content-type": "application/json; charset=UTF-8"
		}
	})
		.then(res => res.json())
		.then(json => { search_drug(json); prodd = json })
}

const search_drug = filtred_array => {
	let out = '<div class="card-body-search scrollbar" id="ss">'

	if (filtred_array.length !== undefined && filtred_array.length > 0) {
		filtred_array.forEach(function (value, i) {
			if (i == 0)  {active_class = 'active' }   else active_class = ''
			
			out += `
				<a class="list-group-item list-group-item-action align-items-start border-0 ${active_class}" id='${i}'>
					<div class="d-flex justify-content-between">
						<h5 class="mb-1">${value.barcode}</h5>
						<small>${value.shelf_life}</small>
					</div>
					<p class="mb-1">${value.name}</p>
					<small>${value.price}</small>
				</a>`
		})
	}
	else {
		out += `
				<a class="list-group-item list-group-item-action flex-column align-items-start active">
					<div class="d-flex w-100 justify-content-between">
						<h5 class="mb-1">Препарат не найден</h5>
						<small></small>
					</div>
					<p class="mb-1"></p>
					<small>0.0 сом.</small>
				</a>`
	}
	out += '</div>'

	filtred_items_paste.classList.add('searchList-show')
	filtred_items_paste.classList.remove('searchList-hide')
	filtred_items_paste.innerHTML = out
}

search_input.addEventListener('input', () => {
	fetch_search()
})

filtred_items_paste.addEventListener('click',  event => {
	convert = {'by_name': 'name', 'by_barcode': 'barcode'}
	convertt = convert[search_status]

	console.log(event)

	if (event.srcElement.tagName == 'A'){
		changeBarcode(prodd[event.srcElement.id][convertt])
		fetchProduct()
	}

	else if (event.srcElement.id == '') {
		changeBarcode(prodd[event.srcElement.offsetParent.id][convertt])
		fetchProduct()
	}
	
	filtred_items_paste.classList.remove('searchList-show')
	filtred_items_paste.classList.add('searchList-hide')
})