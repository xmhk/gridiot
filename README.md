# gridiot.py

Rev 4, oct 23, 2013

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

###clear\_workdir

* remove the working directory on the remote machine

### print\_df(extracommand)
* execute "df" on the remote machine
* extracommand can be '' or for example " |grep sda" to pass to df

##class Job\_Object()
### \_\_init\_\_(self, befehl)
### start( self, node)
### def check( self):


##process\_list(joblist,nodelist)

##push\_to\_nodes( nodelist, pushfilelist)
* a list of files (or wildcards) in pushfilelist are transferred to the workdir on the remote machine

##pull\_from\_nodes(nodelist)
* be careful with this!!! remote files will overwrite files that were pushed and that changed in the meantime!!!

##clear\_node\_workdirs(nodelist)
* clear the workdirs on the nodes in nodelist

##print_df(nodelist):
* exectute df on all nodes to get the free disk space