from subprocess import Popen
from time import sleep


from os import system as ossystem
from sys import argv as sysargv



class Computing_Node():
    def __init__(self,
                 username,
                 ip,
                 port,
                 workdir,
                 maxslots,
                 mode):
        self.username = username
        self.ip = ip
        self.port = port
        self.workdir = workdir
        self.freeslots = maxslots
        self.mode = mode

    def get_command(self, ccommand):
        sshpart = "ssh %s@%s -p %d"%(self.username, self.ip,self.port)
        return "%s 'cd %s && %s'"%(sshpart,self.workdir,ccommand)


class Job_Object():
    def __init__(self, ccommand):
        self.ccommand = ccommand
        self.done = False
        self.active = False
        self.started = False
        self.node = None
        self.process = None
        self.exitmsg = None

    def start( self, node):
        self.node = node
        self.started = True
        self.active = True
        self.process = Popen( self.node.get_command(self.ccommand),shell=True,stdout=None)
        self.node.freeslots-=1
#        print "starting job on %s@%s"%(self.node.username,self.node.ip)

    def check( self):
        if self.done==False and self.started == True:
            signal = self.process.poll()
            if signal != None:
                self.exitmsg = signal
                self.active = False
                self.done = True
                self.node.freeslots+=1
#                print "finished job on %s@%s"%(self.node.username,self.node.ip)


def process_list(joblist,nodelist):
    #determine maximum processors
    maxpro = 0    
    for n in nodelist:
        maxpro += n.freeslots
    #make a list of jobobjects
    jobobjlist=[ Job_Object( jj ) for jj in joblist]
    alldone = False or len(jobobjlist)==0    
    counter = 0
    while not alldone:

        for n in nodelist:
#            print n.ip, n.freeslots
            for j in jobobjlist:
                if j.started == False:
                    if n.freeslots>0:                
                        j.start(n)        
        alldone = True
        donenumber = 0
        activelist = []
        for j in jobobjlist:
            j.check()
            if j.active:
                activelist.append(j)
            if j.done:
                donenumber +=1

            alldone = alldone and j.done

        print "\n\n ----- %d / %d done ... step %d-----"%(donenumber,len(jobobjlist),counter)
        for j in activelist:
            print "active : %s@%s - %s"%(j.node.username, j.node.ip, j.ccommand)
        counter += 1
        sleep(7)


def push_to_nodes( nodelist, pushfilelist):
    for node in nodelist:
        ccommand = 'rsync -azvhc --progress --exclude=%s '%(sysargv[0]) #you don't want to push your control file

        # withou compression    ccommand = 'rsync -avh '
        for pd in pushfilelist:
            ccommand+=pd+' '
        ccommand += ' -e "ssh -p %s"  %s@%s:%s'%(node.port,node.username,node.ip,node.workdir)
        print "++ rsynccommand = ",ccommand
        ossystem(ccommand)



def pull_from_nodes(nodelist):
    for node in nodelist:
        ccommand = 'rsync -avhc --progress %s@%s:%s/ ./ -e "ssh -p %s" --exclude=%s  '%(node.username,node.ip,node.workdir,node.port,sysargv[0])
# without compression    ccommand = 'rsync -avh --progress %s@%s:%s ./ -e "ssh -p %s "  '%(node.username,node.ip,node.workdir,node.port)
        print "++ rsynccommand = ",ccommand
        ossystem(ccommand)

