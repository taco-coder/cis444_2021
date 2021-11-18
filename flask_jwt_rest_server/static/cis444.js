var jwt = null
//initialize the page to show login
$('#loginForm').show();
$('div:not(#loginForm)').hide();

//book genre logic
var header = document.getElementById("genre-bar");
var btns = header.getElementsByClassName("genrebtn");
for (var i = 0; i < btns.length; i++) {
	btns[i].addEventListener("click", function () {
		var current = document.getElementsByClassName("active");
		current[0].className = current[0].className.replace(" active", "");
		this.className += " active";
	});
}

/**
 * swaps login and signup form
 */
function swaplogin() {
	$('#loginForm').toggle();
	$('#signupForm').toggle();
}
/**
 * Gets get_books endpoint and assigns global JWT
 * @param {string} endpoint 
 * @param {function} on_success_callback 
 * @param {function} on_fail_callback 
 */
function secure_get_with_token(endpoint, on_success_callback, on_fail_callback) {
	xhr = new XMLHttpRequest();
	function setHeader(xhr) {
		xhr.setRequestHeader('Authorization', 'Bearer:' + jwt);
	}
	function get_and_set_new_jwt(data) {
		console.log("success callback")
		console.log(data);
		jwt = data.token
		on_success_callback(data)
	}
	$.ajax({
		url: endpoint,
		type: 'GET',
		datatype: 'json',
		success: on_success_callback,
		error: on_fail_callback,
		beforeSend: setHeader
	});
}

/**
 * Sends form data to signup endpoint and displays create status based on success/failure
 * @returns false
 */
function send_signup() {
	$.post("/open_api/signup", { "username": $('#new_user').val(), "password": $('#new_pwd').val() },
		function (textStatus) {
			//this gets called when browser receives response from server
			$('#create_status').html(textStatus.message)
		}, "json").fail(function (response) {
			//this gets called if the server throws an error
			console.log("error");
			console.log(response);
		});
	return false;
}

/**
 * Sends form to login. If fails, prompts user. If success, get_books.
 * @returns false
 */
function send_login() {
	$.post("/open_api/login", { "username": $('#user').val(), "password": $('#pwd').val() },
		function (data, textStatus) {
			//this gets called when browser receives response from server
			if (data.authenticated == false) {
				$('#login_status').html(data.message)
				return false
			}

			//Set global JWT
			jwt = data.token;

			//make secure call with the jwt
			get_books();
		}, "json").fail(function (response) {
			//this gets called if the server throws an error
			console.log("error");
			console.log(response);
		});
	return false;
}

/**
 * Verifies the token then loads and shows book data.
 */
function get_books() {
	//make secure call with the jwt
	secure_get_with_token("/secure_api/get_books", function (data) {
		load_books(data.books);
		show_books();
	}, function (err) {
		console.log(err)
	});
}

/**
 * goes through books array, populating bookname and bookprice fields respectively
 * @param {array} books 
 */
function load_books(books) {
	//go through books array
	for (let i = 0; i < books.length; i++) {
		//load names and prices
		$('#book_name' + (i + 1)).html(books[i][1]);
		$('#book_price' + (i + 1)).html(books[i][2]);
		//hidden attr          
		$('#book' + (i + 1) + 'name').val(books[i][1]);
		$('#book' + (i + 1) + 'price').val(books[i][2]);
	}
}
/**
 * hide everything and show only books page
 */
function show_books() {
	$('#book-page').show().find('*').show();
	$('#loginForm').hide();
}

/**
 * show only thriller books
 */
function onlyThriller() {
	$('#book_row_one_column_one').show();
	$('#book_row_one_column_two').hide();
	$('#book_row_two_column_two').hide();
	$('#book_row_two_column_one').hide();
}
/**
 * show only romance books
 */
function onlyRomance() {
	$('#book_row_two_column_two').show();
	$('#book_row_one_column_one').hide();
	$('#book_row_one_column_two').hide();
	$('#book_row_two_column_one').hide();
}

/**
 * show only scifi books
 */
function onlyScifi() {
	$('#book_row_one_column_two').show();
	$('#book_row_one_column_one').hide();
	$('#book_row_two_column_two').hide();
	$('#book_row_two_column_one').hide();
}
/**
 * show only selfhelp books
 */
function onlySelfhelp() {
	$('#book_row_two_column_one').show();
	$('#book_row_one_column_two').hide();
	$('#book_row_two_column_two').hide();
	$('#book_row_one_column_one').hide();
}

/**
 * show all books regardless of genre
 */
function showAll() {
	$('#book_row_one_column_one').show();
	$('#book_row_one_column_two').show();
	$('#book_row_two_column_two').show();
	$('#book_row_two_column_one').show();
}