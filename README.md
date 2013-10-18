# gridiot.py

Rev 1, oct 18, 2013

* you will need automatic login via ssh-keys
* on remote machines, your will need some RC file that sets your path for non-interactive shells
* * *

##class Computing\_Node()
* ***fields***
    * username
    * ip
    * port
    * workdir
    * freeslots
    * mode
###\_\_init\_\_( username, ip, port, workdir, maxslots, mode)

###get_command( befehl )


##class Job\_Object()
### __init__(self, befehl)
### start( self, node)
### def check( self):


##process_list(joblist,nodelist):

