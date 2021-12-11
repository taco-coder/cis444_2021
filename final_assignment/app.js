//connect to websocket
socket = new WebSocket('wss://g7ftl241bb.execute-api.us-east-1.amazonaws.com/dev');

//on successful connect
socket.onopen = function (event) {
  console.log("connected")
}

//get response from gateway
socket.onmessage = function (event) {
  //parse JSON style string
  data = JSON.parse(event.data)
  //post message
  post(data['message'])
}

socket.onclose = function (event) {
  console.log("connection closed")
}


/**
 * Keeps count of how many characters are currently in the text field
 * @param {var} val 
 */
function countChar(val) {
  var len = val.value.length;
  if (len >= 500) {
    val.value = val.value.substring(0, 240);
  } else {
    $('#charNum').text(240 - len);
  }
};




/**
 * takes the textarea submission and creates a new post for all following users and self
 */
function make_post() {
  d = new Date()

  payload = {
    'action': 'makePost',
    'message': {
      'time': Date.now().toString(),
      'text': $('#post-text-area').val(),
      'date': d.toUTCString()
    }
  }
  socket.send(JSON.stringify(payload));
}

function post(data) {
  text = data['text']
  date = data['date']

  $('#main-page-area-stage').hide()
  $('#main-page-area-post').prepend('<div id="post-item">\
                                                <div id="post-time" style="margin-left: 15px; margin-bottom: 10px; margin-top: 0px">' + date + '</div>\
                                                <div id="user-post" style="margin-left: 15px; margin-bottom: 10px;">' + text + '</div>\
                                            </div>')

}