# phantom-webserver

This is a web server for fetch web page. It is implemented with PhantomJS2, 
selenium.

How it works:
It is an API, send form-data by post to it's root url, it will return an html 
resource, encoded in UTF-8.
Example request:

    POST / HTTP/1.1
    Content-Type: application/x-www-form-urlencoded
    
    url=http%3A%2F%2Fdetail.tmall.com%2Fitem.htm%3Fid%3D521585783755           
    
Requirements:

* phantomjs2  
  Install from github because there are some bugs the author has fixed, but not submitted to the NPM yet.
   
    `     npm install -g https://github.com/pocketjoso/phantomjs2.git              
    ` 
  
* python packages in requirements.txt.
  
How to run it:
After all requirements are installed, in the project root, in terminal:

    gunicorn -w 4 app:app
    
Then Gunicorn will start it with four workers.
