<%
Session("genericFilters") = "{""sortBy"": """", ""offset"": """", ""limit"": """"}"

public function apiRequest( sessionId, methodNameIn, paramsIn )

Response.AppendToLog "apiRequest " + sessionId + " AND "+ dataIn
'Response.Write(dataIn + "<br><br>") 

Dim http: Set http = Server.CreateObject("WinHttp.WinHttpRequest.5.1")
Dim url: url = Session("myUrl")
Dim data: data = "{""jsonrpc"": ""2.0"", ""method"": """+methodNameIn+""", ""token"":"""++Session("token")+""", ""params"":"+paramsIn+", ""filter"":"+Session("genericFilters")+"}"

'Response.Write(data + "<br>")

With http
  Call .Open("POST", url, False)
  Call .SetRequestHeader("Content-Type", "application/json")
  
  Call .Send(data)
End With

If Left(http.Status, 1) = 2 Then
  'Request succeeded with a HTTP 2xx response, do something...
  apiRequest = http.ResponseText
Else
  'Output error
  apiRequest = "Server returned: " & http.Status & " " & http.StatusText
End If

End function

'----------- login ----------
public Function apiLogin( urlIn, token )
	Session("myUrl") = urlIn
	Session("token") = token


end function

'-----------get_system_info -------------
public Function apiget_system_info( )
	apiget_system_info = apiRequest(Session("mySessionId"), "get_system_info", "{ }")
end function
'-----------get_status -------------
public Function apiget_status( )
	apiget_status = apiRequest(Session("mySessionId"), "get_status", "{ }")
end function
'-----------set_status -------------
public Function apiset_status( status, moo )
	apiset_status = apiRequest(Session("mySessionId"), "set_status", "{ ""status"":"""+status""",""mood"":"""+mood"""}")
end function
'-----------make_payment -------------
public Function apimake_payment( from_wallet, to_wallet, amount, commen )
	apimake_payment = apiRequest(Session("mySessionId"), "make_payment", "{ ""from_wallet"":"""+from_wallet""",""to_wallet"":"""+to_wallet""",""amount"":"""+amount""",""comment"":"""+comment"""}")
end function


%>
