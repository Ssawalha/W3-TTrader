const api_keyField = document.getElementById("api_key")
const balanceOutput = document.getElementById("balanceOutput")
const balanceButton = document.getElementById("balanceButton")

balanceButton.addEventListener("click", (e)=> {
    event.preventDefault()
    const url = `http://127.0.0.1:5000/api/${api_keyField.value}/balance`
    const promise = fetch(url)  
    promise.then(response => response.json()).then(json => {
        balanceOutput.innerHTML = `Your balance is $${json['balance']}`
    })
})