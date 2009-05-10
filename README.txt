Orphereus - Installation and Setup
======================

At first, you should configure your installation by creating a copy of 
'development.ini.template' (i.e., to 'prod.ini') and modifying it.   

Deployment is automatical and should run smoothly. To start it, run:

  $ paster setup-app prod.ini  
  
After that, start the server process like that:
 
  $ paster serve --reload prod.ini  
  
  
  
Orphereus - Configuration
=====================

Almost all configuration options are self-explanatory.
There are two basic server modes: SCGI and atand-alone HTTP server. 

For the first mode (recommended), in [server:main] section:

      use = egg:PasteScript#flup_scgi_thread

and for the second one,

      use = egg:Paste#http 