mysqlbackup
===========

A simple utility to get gzipped MySQL dumps with easy connection strings written in python.

Installation
============
Execute the following command as root (sudo).

> make install


Usage
=====
mysqlbackup username[:password]@hostname[:port]/database [-extra-mysqldump-parameters]

Output file will be formatted with timestamp as databasename_YYYYMMDD_HHMMSS.sql.gz.

If password is not specified, it will be prompted via standard input. Original mysqldump parameters can also be passed.


License
=======
Distributed under [GNU/GPL v3](http://www.gnu.org/licenses/gpl.html).


Contact
=======
Maintainer: [Ahmet Alp Balkan](http://github.com/ahmetalpbalkan)
