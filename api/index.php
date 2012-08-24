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
	
	$dbh = new PDO('sqlite:/etc/SmartHome/Databases/APIUsers.sqlite');
	$results = $dbh->Query("SELECT * from Users WHERE PublicKey = '$publickey'");
	while ($row = $results->Fetch(PDO::FETCH_ASSOC)) 
	{
		$key = $row['2'];
	}

	$hash = hash_hmac('SHA1', $_REQUEST['request'].$_REQUEST['key'].$_REQUEST['time'], $key);
	if($hash === $_REQUEST['hash'] && $_REQUEST['time'] > (time() - 60) )
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

private function zones()
{
	if($this->get_request_method() != "GET")
	{
		$this->response('', 406);
	}

	$dir = 'sqlite:/etc/SmartHome/Databases/Security.sqlite';
	$dbh = new PDO($dir) or die ("cannot open the database");
	$query = $dbh->query('SELECT * from Zones');
        while ($entry = $query->fetch(SQLITE_NUM))
        {
                $result[] = $entry;
        }

	$this->response(json_encode($result), 200);
}

private function addtosyslog()
{
	if($this->get_request_method() != "GET")
	{
		$this->response('',406);
	}

	$dir = 'sqlite:/etc/SmartHome/Databases/SysLog.sqlite';
        $dbh  = new PDO($dir) or die("cannot open the database");
        $dbh->exec("INSERT INTO Log (Time, Text) VALUES('".time()."',  '".str_replace("-", " ", $_REQUEST['text'])."' )");

	$this->response('Success', 200);
}

private function getsyslog()
{
	// Cross validation if the request method is GET else it will return "Not Acceptable" status
    if($this->get_request_method() !== "GET")
    {
            $this->response('',406);
    }
    $dir = 'sqlite:/etc/SmartHome/Databases/SysLog.sqlite';
    $dbh  = new PDO($dir) or die("cannot open the database");
    $query = $dbh->query('SELECT * from Log ORDER BY Time DESC LIMIT 30');
    while ($entry = $query->fetch(SQLITE_NUM))
    {
            $result[] = $entry;
    }
    $dir = 'sqlite:/etc/SmartHome/Databases/Security.sqlite';
    $dbh  = new PDO($dir) or die("cannot open the database");
    $query = $dbh->query('SELECT * from Log ORDER BY Time DESC LIMIT 30');
    while ($entry = $query->fetch(SQLITE_NUM))
    {
            $result[] = $entry;
    }


    $this->response(json_encode($result), 200);
}

private function getallresults()
{
	// Cross validation if the request method is GET else it will return "Not Acceptable" status
	if($this->get_request_method() !== "GET")
	{
		$this->response('',406);
	}
	$dir = 'sqlite:/etc/SmartHome/Databases/Security.sqlite';
    $dbh  = new PDO($dir) or die("cannot open the database");
	$query = $dbh->query('SELECT * from Log ORDER BY Time DESC LIMIT 30');
	while ($entry = $query->fetch(SQLITE_NUM))
	{
		$result[] = $entry;
	}

	$this->response($this->json($result), 200);

}

// This method needs to be cleaned up....
private function status()
{
	$namearray = array("Front Door", "Back Door", "Garage Door", "Bedroom Windows", "Upstairs Windows",
                   "Hallway Motion", "Livingroom Motion", "Front Windows", "Garage Windows",
                   "Attic Door", "Livingroom/Kitchen Windows");
	// Cross validation if the request method is GET else it will return "Not Acceptable" status
        if($this->get_request_method() !== "GET")
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
	$this->response(json_encode($result), 200);
}
}

// Initiiate Library
$api = new API;
$api->processApi();
?>
