var jwt = null
//initialize the page to show login
$('#loginForm').show();
$('div:not(#loginForm)').hide();

//book genre-bar logic
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
 * @param {string} method
 * @param {JSON}	data_to_send
 * @param {function} on_success_callback 
 * @param {function} on_fail_callback 
 */
function secure_call_with_token(endpoint, method, data_to_send, on_success_callback, on_fail_callback) {
	console.log("Secure Call: " + method)
	console.log(data_to_send)
	xhr = new XMLHttpRequest();
	function setHeader(xhr) {
		xhr.setRequestHeader('Authorization', 'Bearer:' + jwt);
	}
	function get_and_set_new_jwt(data) {
		console.log(data);
		jwt = data.token
		on_success_callback(data)
	}
	$.ajax({
		url: endpoint,
		data: data_to_send,
		type: method,
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
			console.log(jwt)
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
 * Reloading the page takes you back to the login screen. Clear JWT data
 */
function signout() {
	jwt = null
	window.location.reload(true);
}

/**
 * Verifies the token then loads and shows book data.
 */
function get_books() {
	//make secure call with the jwt
	secure_call_with_token("/secure_api/get_books", 'GET', {}, function (data) {
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
 * Shows books only of specific genre
 * @param {string} genre 
 */
function showOnly(genre) {
	if (genre == "all") {
		$('div.book').show();
	}
	else {
		$('div.book').not('.' + genre).hide();
		$('div.book.' + genre).show();
	}
}

/**
 * Goes back to main page
 */
function backToMain() {
	$('div').not('#book-page').hide();
	$('#book-page').show().find('*').show();
}
/**
 * hides bookstore and gets redlepanka page
 */
function getRedLepankaPage() {
	$('#book-page').hide();
	$('#red_lepanka_page').show().find('*').show();
	getBookData(1);
}

/**
 * hides bookstore and gets becometaco page
 */
function getBecomeTacoPage() {
	$('#book-page').hide();
	$('#become_taco_page').show().find('*').show();
	getBookData(2);
}

/**
 * hides bookstore and gets carjack page
 */
function getCarjackerPage() {
	$('#book-page').hide();
	$('#car_jack_page').show().find('*').show();
	getBookData(3);
}

/**
 * hides bookstore and gets egobias page
 */
function getEgoBiasPage() {
	$('#book-page').hide();
	$('#ego_bias_page').show().find('*').show();
	getBookData(4);
}

/**
 * Takes an int corresponding to the book you want to fetch. Gets and sets book name, price, and calls getReviews
 * @param {int} book_id 
 */
function getBookData(book_id) {
	secure_call_with_token("/secure_api/get_book_data", 'GET', { "book_id": book_id }, function (data) {
		console.log("got book data");

		//initialize html div ID strings
		var name = "#name" + book_id;
		var price = "#price" + book_id;
		var hideName = "#bookname" + book_id;
		var hidePrice = "#bookprice" + book_id;

		//set HTML and hidden attributes
		$(name).html(data.info['bookname'])
		$(price).html(data.info['price'])
		$(hideName).val(data.info['bookname'])
		$(hidePrice).val(data.info['price'])

		//fetch the reviews
		getReviews(book_id)
	}, function (err) {
		console.log(err);
	});
}

/**
 * Gets the reviews and calculates avg rating
 * @param {int} book 
 */
function getReviews(book) {
	secure_call_with_token("/secure_api/get_book_data", 'GET', { "book_id": book }, function (data) {
		console.log("got reviews");

		//initialize avgRate, html ID strings, and reviews array
		var avgRate = 0;
		var userR = "#user-review" + book;
		var rate = "#avg-rate" + book;
		var reviews = data.info['reviews']

		//append all reviews in reviews array
		for (let i = 0; i < reviews.length; i++) {
			$(userR).append(reviews[i][3] + " rated: " + reviews[i][2] + "/5 - " + reviews[i][1])
			avgRate += reviews[i][2]
			$(userR).append("<br><br>")
		}

		//calc and set the avg rating
		avgRate = avgRate / reviews.length
		$(rate).html("Rating: " + avgRate.toFixed(1) + "/5")
	}, function (err) {
		console.log(err);
	});
}

/**
 * Posts a new review for a given book based on what book_id is
 * @param {int} book_id 
 */
function postReview(book_id) {
	//init html IDs and get avg rate html
	var reviewText = "#book-review" + book_id;
	var rating = "#rate" + book_id;
	var userR = "#user-review" + book_id;
	var rate = "#avg-rate" + book_id;
	var avgRate = $(rate).html();
	//clearing to just get the avg rate
	avgRate = avgRate.replace("Rating: ", "");
	avgRate = avgRate.replace("/5", "");
	secure_call_with_token("/secure_api/post_book_review", 'POST', { "book_id": book_id, "review": $(reviewText).val(), "rate": $(rating).val() },
		function (data) {
			//add new review
			$(userR).append(data.review['user'] + " rated: " + data.review['rate'] + "/5 - " + data.review['review']);
			$(userR).append("<br><br>");

			//calc new avg rating
			var numReviews = ($(userR + " br").length) / 2; //there are 2 line breaks after each review; getting num of reviews based on line breaks
			console.log(numReviews)
			console.log(avgRate)
			console.log(avgRate * numReviews)
			console.log($(rating).val())
			//get rough sum of all the previous ratings, add the current rating, then div by num of previous reviews plus this new one
			avgRate = ((avgRate * numReviews) + $(rating).val()) / (numReviews);
			$(rate).html("Rating: " + avgRate.toFixed(1) + "/5")
		}, function (err) {
			console.log(err)
		});
	return false;
}
