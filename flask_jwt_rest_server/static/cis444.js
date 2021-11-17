var jwt = null
//initialize the page to show login
$('#loginForm').show();
$('div:not(#loginForm)').hide();

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