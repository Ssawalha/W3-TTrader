const usernameField = document.getElementById("username")
const passwordField = document.getElementById("password")
const loginButton = document.getElementById("loginButton")
const outputArea = document.getElementById("output")
const autoInputAPIkey = document.getElementById("api_key")

// install flask-cors
// in the python file where your Flask app object is created add the following line:
// from flask_cors import CORS
// app = Flask(__name__)
// cors = CORS(app)

loginButton.addEventListener("click", (event) => {
    event.preventDefault()
    const url = "http://127.0.0.1:5000/api/get_api_key"
    const promise = fetch(url, {
        method: "post",
        mode: "cors",
        headers: {"content-type": "application/json"},
        body: JSON.stringify({
            username: usernameField.value,
            password: passwordField.value
        })
    })
    promise.then(response => response.json()).then(json => {
        console.log(json)
        if (json.error !== undefined) {
            outputArea.innerHTML = "<b>Bad username or password</b>"
        } else {
            window.sessionStorage.setItem("api_key", json.api_key)
        }
    })
})