Orphereus - Installation and Setup
======================

0. Orphereus requires Python 2.5+.

1. Configure your installation by creating a copy of
'development.ini.template' (i.e., to 'prod.ini') and modifying it
(see 'Orphereus - Configuration' section.).   

2. Deployment is automatical. To start it, run:

  $ python setup.py install 
 
Any problematic modules can be installed manually with a packet manager or with 
`easy_install`.

2.1 Development environment
This command will made paster commands available without installation:

  $ python setup.py egg_info 
 
Example command processors can be found in example.py

  $paster --plugin=Orphereus mycommand --goodbye lol

3. Initial database structure is created with 

  $ paster setup-app prod.ini  

4. Create a user and make him the owner of Orphereus' directory.

5. Customize included startup script 'orphie-initscript' to match your paths and 
server process username and place it in a directory with init scripts.   
  
6. Start the server process like that:
 
  $ /etc/init.d/orphie start                   
  

Orphereus - Configuration
=====================

Almost all configuration options are self-explanatory.
There are two basic server modes: SCGI and stand-alone HTTP server. 

For the first mode (recommended), in [server:main] section:

      use = egg:PasteScript#flup_scgi_thread

For the second one:

      use = egg:Paste#http
      

Orphereus - Automatic Maintenance
=====================
Add this into crontab:

  $ paster maintenance --config=development.ini --path=. RunAllObligatory

--path is obligatory parameter, it's equals '.' by default.

If you experience problems with this command, you may add "--plugin=Orphereus" 
option to command line:
  
  $ paster --plugin=Orphereus maintenance --config=development.ini --path=. RunAllObligatory
  
Also you can replace "RunAllObligatory" with set of maintenance actions.
Run this command get additional information:

  $ paster --plugin=Orphereus maintenance -h

-- TEXT BELOW IS DEPRECATED --
To implement automatic unbans, integrity checks and clean-ups, there is an 
example script for scheduling these tasks via cron - 'mtn.sh'. 