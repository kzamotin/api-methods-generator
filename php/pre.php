<?php
class Sample{
    private $URL;
    private $TOKEN;
    private $SESSIONID;
	private $GENERICFILTER;
    private $DELAY;
    
    function __construct($url, $token, $delay=500000) {
        $this->URL=$url;
        $this->TOKEN=$token;
		$this->DELAY=$delay;
		$this->GENERICFILTER=array(
            'sortBy' => '',
            'offset' => '',
            'limit' => '' );
		$this->EXTRAINFO='';
             
    }

    //====================
    private function make_json($method, $params) {
        $data = array('jsonrpc' => '2.0', 
        'method' => $method, 
		'token'  => $this->TOKEN,
        'params' => $params,
		'filter' => $this->GENERICFILTER
        );
        $js = json_encode($data);
        return $js;
    }

    //====================
    private function parseHeaders( $headers )
    {
        $head = array();
        foreach( $headers as $k=>$v )
        {
            $t = explode( ':', $v, 2 );
            if( isset( $t[1] ) )
                $head[ trim($t[0]) ] = trim( $t[1] );
            else
            {
                $head[] = $v;
                if( preg_match( "#HTTP/[0-9\.]+\s+([0-9]+)#",$v, $out ) )
                    $head['response_code'] = intval($out[1]);
            }
        }
        return $head;
    }
    //====================
    public function request($js, &$data) {
		usleep($this->DELAY);
		$this->EXTRAINFO='';
        $options = array(
            'http' => array(
                'header'  => "Content-type: application/json\r\n",
                'method'  => 'POST',
                'content' => $js
            )
        );
        $context  = stream_context_create($options);
        $result = @file_get_contents($this->URL, true, $context) or die("Unable to connect Sample client");
        $response = $this->parseHeaders($http_response_header);
        if ($response['response_code'] != 200){
            $data= '';
            return false;
        }
        else{
            
        $response = json_decode($result);
            if (isset ($response->{'error'})) {
                $data = $response->{'error'};
                return false;
            }
            else {
                $data = $response->{'result'};
                if ($data === false)
                    return false;
				$this->EXTRAINFO = $response->{'resultExtraInfo'};
                return true;

            }
        }
    }
    //====================

	function genericFilter($sortBy, $offset, $limit){
		$this->GENERICFILTER = array(
		'sortBy' => $sortBy,
		'offset' => $offset,
		'limit' => $limit );
        }
    //====================
   
    function genericFilterClear(){
        $this->GENERICFILTER = array(
        'sortBy' => '',
        'offset' => '',
        'limit' => '' );
        } 
    //====================
	
	 function getExtraInfo(){
        return $this->EXTRAINFO;
        } 
    //====================
 
