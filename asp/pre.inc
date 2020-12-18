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

