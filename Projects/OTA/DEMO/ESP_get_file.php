<?php
#Setting up the website end of things in order to authenticate access and download update files.
#Create a directory to which your ESPs can connect to download update files. Ideally this folder should not be publicly
#accessable and have meta tags to deny web robots.
#Access this script with a web address and query string, which must contain version number, mac address, and password.
#for example http://my_website/Downloads/ESP_get_data.php?ver=V1&mac=abcdefgh&file=file&password=my-password&file=

if (isset($_GET['password'])) {  $pwd = $_GET['password'];} 
if (isset($_GET['mac'])) {  $mac = $_GET['mac'];} 
if (isset($_GET['ver'])) {  $version = $_GET['ver'];} 
if (isset($_GET['file'])) {  $file = $_GET['file'];} 
$id = 0;

if (isset($version) && isset($mac))
{  $file = $version.$mac.$file;}
else
{ $file = 'no_file';
   exit('incorrect query string');}

#create a password for all your ESPs in the project and code into your program password = 'xxxxxx'
#create a SHA1 hash of this password.
#To create a password hash save the following script on your server and access with a browser, and copy the hash
       #  <?php echo sha1('enter your password here').'<p>';

#create the following PHP script and place it in a folder of your website without public access, usually the 
#folder up from the root folder of your domain.  The filename can be anything you want, here I call it 'hash.php'

#the script has just one line. Put the hash of your password in it.
#    <?php   $hash = 'the hash you copied from your browser';

 #The next line is the path to your database hash script.
include('../../hash.php');
echo 'Hash from file:  '.$hash.'<p>';
#echo SHA1($pwd).'<p>';
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
