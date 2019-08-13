const tickerInput = document.getElementById("ticker")
const submitButton = document.getElementById("submit")
const theOutput = document.getElementById("output")

let lookupPrice = null

function submitClick(event) {
    event.preventDefault()
    const promise = fetch(`http://127.0.0.1:5000/api/get_ticker_price/${tickerInput.value}`)
    promise.then(response => response.json()).then(json => {
        theOutput.innerHTML = `The price is $${json["ticker price is "]}!`
    })
}

submitButton.addEventListener("click", submitClick)