#!/usr/bin/python
from sys import argv
from sys import exit
from getpass import getpass
from os import popen
from os import unlink
from datetime import datetime
import tempfile


# Author: ahmet alp balkan <ahmetalpbalkan at gmail.com>
# Distributed under GNU/GPL v3 License
# see http://www.gnu.org/licenses/gpl.html for more.

usage = """usage:\tmysqlbackup username[:password]@hostname[:port]/database [-extra-mysqldump-parameters]
\tget gzipped dump of given database."""

mysqldump_path = '/usr/bin/mysqldump'
gzip_path = '/usr/bin/gzip'

def error(msg, exitcode=1):
    print msg
    exit(exitcode)


if __name__ == '__main__':
    if len(argv) < 2:
        error(usage)
    else:
        username, password, hostname, port, database, extras = None, None, None, None, None, None

        conn_string = argv[1]

        parts = conn_string.split('@')
        if len(parts) != 2:
            error("Invalid connection string")
        
        auth = parts[0].split(':')
        target = parts[1].split('/')
        
        # get authentication data
        if len(auth)<1 :
            error("Invalid authentication string")
        elif len(auth) >= 1:
            username = auth[0]
            if len(username)<1 : error("Username not specified")
            if len(auth) > 1:
                password = auth[1]
            else:
                password = getpass("Password: ")

        # get target host data
        if len(target) < 2:
            error("Invalid hostname string")
        else:
            host = target[0].split(':')
            database = target[1]
            if len(database)<1: error("No database specified")
            
            if len(host) < 1:
                error("Invalid hostname target string")
            else:
                hostname = host[0]
                if len(hostname) < 1: error("Hostname not specified")

                if len(host) > 1:
                    port = int(host[1])
        
        if len(argv)>2:
           extras = [] 
           for i in range(2, len(argv)):
                   extras.append(argv[i])

        # execute mysqldump
        arguments = []
        arguments.append(mysqldump_path)
        if(extras): arguments.append(' '.join(extras))
        arguments.append('-u ' + username)
        if (password): arguments.append('-p' + password)
        arguments.append('-h ' + hostname)
        if (port): arguments.append('-P ' + str(port))
        arguments.append(database)
       
        m_pipe = popen(' '.join(arguments))
        tmp = tempfile.NamedTemporaryFile(delete = False)
        tmp.write(m_pipe.read())
        m_pipe.close()

        # execute gzip
        arguments = []
        outfile =database + '_' + datetime.now().strftime('%Y%m%d_%H%M%S') +'.sql.gz'
        arguments.append(gzip_path)
        arguments.append('-c')
        arguments.append(tmp.name)
        arguments.append(' > ' + outfile)
        print(' '.join(arguments))
        g_pipe = popen(' '.join(arguments))
        g_pipe.close()

        unlink(tmp.name)
        tmp.close()
