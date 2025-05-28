<?php
/*
Setting up the website end of things in order to authenticate access and download update files.
Create a directory to which your ESPs can connect to and download update files. Ideally this folder should not be publicly
accessable and have meta tags to deny web robots.
Access this script with a web address and query string, which must contain version number, mac address, password and filename
for example http://my_website/Downloads/ESP_get_data.php?ver=V1&mac=abcdefgh&password=my-password&file=my_filename

For security there is the password feature, but this is optional. If you do not require it, skip this part, and remove password from the query string
and the password checking in the php script.
Create a password for all your ESPs in the project and add as a variable to your program code:    password = 'my_password' 
and then create a SHA1 hash of this password.
To create a password hash, save the following line to a script on your server and access it with a browser.
The browser will display a hash code for the password. Copy it for the next step
       <?php echo sha1('my_password').'<p>';

create the following PHP script and place it in a folder of your website without public access, usually the 
folder up from the root folder of your domain.  The filename can be anything you want, here I call it 'hash.php'
the script has just one line. Put the hash of your password in it.
    <?php   $hash = 'the hash you copied from your browser';

*/
#here is the main php script

if (isset($_GET['password'])) {  $pwd = $_GET['password'];}  #remove if not using passwords
if (isset($_GET['mac'])) {  $mac = $_GET['mac'];} 
if (isset($_GET['ver'])) {  $version = $_GET['ver'];} 
if (isset($_GET['file'])) {  $file = $_GET['file'];} 
$id = 0;

if (isset($version) && isset($mac))
{  $file = $version.$mac.$file;}
else
{ $file = 'no_file';
   exit('incorrect query string');}
   
 #The next line is the path to your hash script, if you opted to use a password
 #otherwise you can skip this bit.
include('../../hash.php');
if ($hash != SHA1($pwd)) {  exit('hash file error');}
#if script gets this far, we have received a valid password.
	
#finally, after authentication is done, read the file
$fail = 'File not found';
$dir = getcwd();
$file = $dir.'/'.$file;
$myfile = fopen($file, "r") or die($fail);
echo file_get_contents($file);
fclose($myfile);

?>
