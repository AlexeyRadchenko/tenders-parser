//
// Custom JS
//

var firstSearch = true;
var monthsRu = new Array('Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря');
var monthsEn = new Array('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December');

function cleanSearch(obj)
{
	if (firstSearch)
	{
		firstSearch = false;
		obj.value = '';
		obj.style.color = '#000000';
		obj.style.background = '#FFFFFF';
		obj.style.border = '2px solid #F8B411';
	}
}

