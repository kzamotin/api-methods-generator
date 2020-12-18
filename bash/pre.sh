#!/bin/bash
# note: use correct path for qj
apiurl="http://127.0.0.1:10010/api/1.0/"
token="F95EBFEC86F968D80A5D40CAD1BCD520"
jqcommand="jq"
#======================
function makejson(){
#echo "$1"
#echo "$2"
echo $($jqcommand  -n "{jsonrpc: "2.0", method: \"$1\", token: \"$token\"} + {params: $2}")
}
#======================
function makerequest(){
#echo $1
response=$(curl -c cookiefile -b cookiefile --silent  -H "Content-Type: application/json" -d "$1"   $apiurl )

echo $(echo $response | $jqcommand '.result')
}
#======================
function login () {

param=$($jqcommand -n "{accessToken: \"$1\"}") 
jsondata=$(makejson "login" "$param")

makerequest "$jsondata"
}
