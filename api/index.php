<?php

require_once("Rest.inc.php");

class API extends REST 
{

public function __construct()
{
	parent::__construct();// Init parent contructor
}

//Public method for access api.
//This method dynmically call the method based on the query string
public function processApi()
{
	$publickey = $_REQUEST['key'];
	$dir = 'sqlite:/etc/SmartHome/Databases/APIUsers.sqlite';
        $dbh  = new PDO($dir) or die("cannot open the database");
        $query =  "SELECT * from Users WHERE PublicKey = '$publickey'";
	foreach ($dbh->query($query) as $row)
        {
		$key = $row['2'];
	}

	$hash = hash_hmac('SHA1',$_REQUEST['request'].$_REQUEST['key'].$_REQUEST['timestamp'], $key);
	if($hash === $_REQUEST['hash'])
	{
		$func = $_REQUEST['request'];
		if((int)method_exists($this,$func) > 0)
			$this->$func();
		else
			$this->response('',404);
	}
	else
	{
    		$this->response('Unauthorized',401);
	}
}

private function json($data)
{
	if(is_array($data))
	{
		return json_encode(array_values($data));
	}
}

private function getallresults()
{
	// Cross validation if the request method is GET else it will return "Not Acceptable" status
	if($this->get_request_method() != "GET")
	{
		$this->response('',406);
	}
	$result = array();
	$dir = 'sqlite:/etc/SmartHome/Databases/Security.sqlite';
        $dbh  = new PDO($dir) or die("cannot open the database");
	$query = $dbh->query('SELECT * from Log ORDER BY Time DESC');
	while ($entry = $query->fetch(SQLITE_NUM))
	{
		$result[] = $entry;
	}

	// If success everythig is good send header as "OK" and return list of users in JSON format
	$this->response($this->json($result), 200);
}


private function status()
{
	$namearray = array("Front Door", "Back Door", "Garage Door", "Bedroom Windows", "Upstairs Windows",
                   "Hallway Motion", "Livingroom Motion", "Front Windows", "Garage Windows",
                   "Attic Door", "Livingroom/Kitchen Windows");
	// Cross validation if the request method is GET else it will return "Not Acceptable" status
        if($this->get_request_method() != "GET")
        {
                $this->response('',406);
        }

        $result = array();
	foreach($namearray as $name)
	{
	        $dir = 'sqlite:/etc/SmartHome/Databases/Security.sqlite';
        	$dbh  = new PDO($dir) or die("cannot open the database");
        	$query = $dbh->query("SELECT * from Log WHERE Zone = '$name' ORDER BY Time DESC");
        	while ($entry = $query->fetch(SQLITE_NUM))
        	{
                	$result[] = $entry;
			break;
        	}
	}

	// If success everythig is good send header as "OK" and return list of users in JSON format
	$this->response($this->json($result), 200);
}
}

// Initiiate Library
$api = new API;
$api->processApi();
?>
