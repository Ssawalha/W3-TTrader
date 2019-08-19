# echo 'get_ticker_price'
# curl 127.0.0.1:5000/api/get_ticker_price/aapl

# echo 'get_api_key'
# curl 127.0.0.1:5000/api/12345678912345678902

# echo 'get_balance'
# curl 127.0.0.1:5000/api/12345678912345678902/balance

# echo 'get_positions'
# curl 127.0.0.1:5000/api/12345678912345678902/positions

# echo 'get_trades'
# curl 127.0.0.1:5000/api/12345678912345678902/trades

# echo 'put_deposit $100'
# curl -X PUT -H 'content-type: application/json' -d '{"deposit":100}' 127.0.0.1:5000/api/12345678912345678902/deposit

# echo 'sell_stock {"tsla":1}'
# curl -X POST -H 'content-type: application/json' -d '{"ticker":"tsla","shares":1}' 127.0.0.1:5000/api/12345678912345678902/sell

# echo 'buy_stock {"tsla":1}'
# curl -X POST -H 'content-type: application/json' -d '{"ticker":"tsla","shares":3}' 127.0.0.1:5000/api/12345678912345678902/buy

# echo 'create_account'
# curl -X POST -H 'content-type: application/json' -d '{"username":"h", "password":"1234", "first_name":"h", "last_name":"h"}' 127.0.0.1:5000/api/create_account

echo 'api_key'
curl -X POST -H 'content-type: application/json' -d '{"username":"sami", "password":"1234"}' 127.0.0.1:5000/api/get_api_key

echo 'get_checking_account_number'
curl 127.0.0.1:5000/api/12345678912345678902/checking_account_number

echo 'get_routing_number'
curl 127.0.0.1:5000/api/12345678912345678902/routing_number

# echo 'set_checking_account_number'
# curl -X PUT -H 'content-type: application/json' -d '{"set_checking_account_number":"123412341234"}' 127.0.0.1:5000/api/12345678912345678902/settings/checking_account_number

# echo 'set_routing_number'
# curl -X PUT -H 'content-type: application/json' -d '{"set_routing_number":"123456123456"}' 127.0.0.1:5000/api/12345678912345678902/settings/routing_number