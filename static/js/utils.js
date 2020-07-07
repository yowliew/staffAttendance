var toStop = false;

function callAjax(method, value) {
	var params = {
		method: method,
		value: value,
	};

	$.ajax({
		type: 'POST',
		url: '/validate_field',
		data: params,
		success: function (data, textStatus, jqXHR) {
			if (!data.message) {
				showMsg(data.error);
				method = '#' + method;
				$(method).focus();
				toStop = true;
			} else toStop = false;
		},
		error: function (jqHXR, textStatus, errorThrown) {
			showMsg(jqXHR.status + ' ' + errorThrown);
			method = '#' + method;
			$(method).focus();
			toStop = true;
		},
	});
}

function CallAjextWithReturn(method, value, handleresult) {
	var params = {
		method: method,
		value: value,
	};

	$.ajax({
		type: 'POST',
		url: '/validate_field',
		data: params,
		success: function (result, textStatus, jqXHR) {
			handleresult(result);
		},
		error: function (jqHXR, textStatus, errorThrown) {
			showMsg(jqXHR.status + ' ' + errorThrown);
			method = '#' + method;
			$(method).focus();
		},
	});
}

function showMsg(msg) {
	$('.modal-body').text(msg);
	$('#staticBackdrop').modal();
}

var searchString = []; //Global variable for autocomplete field

function autoCompleteField(theField) {
	ajexAutoComplete(theField, function (result) {
		for (i in result[theField]) {
			searchString[theField][searchString[theField].length] = result[theField][i][theField];
		}
	});
}

function ajexAutoComplete(theField, handleResult) {
	$.ajax({
		type: 'POST',
		url: '/autocomplete',
		data: { field: theField },
		dataType: 'json',
		success: function (result, textStatus, jqXHR) {
			handleResult(result);
		},
		error: function (jqHXR, textStatus, errorThrown) {
			showMsg(jqHXR.status + ' 	' + errorThrown);
		},
	});
}

// function to verify float
function isFloat(evt) {
	var charCode = event.which ? event.which : event.keyCode;
	if (charCode != 46 && charCode > 31 && (charCode < 48 || charCode > 57)) {
		showMsg('Please enter only a valid number');
		return false;
	} else {
		//if dot sign entered more than once then don't allow to enter dot sign again. 46 is the code for dot sign
		var parts = evt.srcElement.value.split('.');
		if (parts.length > 1 && charCode == 46) {
			return false;
		}
		return true;
	}
}

//function to verify numbers
function isNumb(theField) {
	let numbers = /^[0-9]+$/;
	if (!theField.match(numbers)) return false;
	else return true;
}

//to convert date format
function convertDate(theDate, saperator, inFormat, outFormat) {
	var parts = theDate.split(saperator);
	if (inFormat == 'DD/MM/YYYY') {
		var doneDate = new Date(parts[2], parts[1] - 1, parts[0]);
	} else if (inFormat == 'YYYY-MM-DD') {
		var doneDate = new Date(parts[0], parts[1] - 1, parts[2]);
	}

	var dd = doneDate.getDate();
	var mm = doneDate.getMonth() + 1;
	var yyyy = doneDate.getFullYear();

	if (dd < 10) {
		dd = '0' + dd;
	}

	if (mm < 10) {
		mm = '0' + mm;
	}
	//			convertDate = mm + '-' + dd + '-' + yyyy;
	//			convertDate = mm + '/' + dd + '/' + yyyy;
	//			convertDate = dd + '-' + mm + '-' + yyyy;
	//          convertDate = dd + '/' + mm + '/' + yyyy;
	if (outFormat == 'YYYY-MM-DD') {
		doneDate = yyyy + '-' + mm + '-' + dd;
	} else if (outFormat == 'DD/MM/YYYY') {
		doneDate = dd + '/' + mm + '/' + yyyy;
	}
	return doneDate;
}

//to fix 2 decimal place for "Input" type -> number
function setTwoNumberDecimal(el) {
	el.value = parseFloat(el.value).toFixed(2);
}

//to populate DrowDown input
function populateDropDown(theField, emptyMessage) {
	var theSelector = '#' + theField;

	$.ajax({
		type: 'POST',
		data: { field: theField },
		url: '/populate_dropdown',
		success: function (data) {
			var len = data.length;

			$(theSelector).empty();
			$(theSelector).append('<option value="">' + emptyMessage + '</option>');

			for (var i = 0; i < len; i++) {
				var id = data[i]['id'];
				var name = data[i]['name'];

				$(theSelector).append("<option value='" + name + "'>" + name + '</option>');
			}
		},
	});
}
