README

Author:
Qi Wang

Class:
EC500

Instruction:
After download MySQL, use command line: mysql -u root -p, and enter password to start MySQL server. 
First, create a database called airports. Use command line: CREATE DATABASE airports;
Second, switch to airports database, using command line: USE airports. Then create a table in airports database, using data structure provided in airports_Mysql.sql. 
Third, switch airports.json file to airports.csv file, using the service provided by http://www.danmandle.com/blog/json-to-csv-conversion-utility/.
Fourth, import airports.csv file into airports table. Use command line: LOAD DATA INFILE  '/$PATH/airports.CSV' INTO TABLE airports;
Fifth, run desired instructions to select specific data. Listed in airports_Mysql.sql file.

Comparison Between MySQL and MongoDB:
Similarity:
1. MySQL and MongoDB both use constant time to do inserting one record.

Difference:
1. 
MySQL needs more restrict data definition before import data file.
MongoDB can import data directly without designing tables and defining data type.

2. 
MySQL's search function could more complicated for a programmer if tables aren't designed great. A programmer could do complexity revise on search query.
MongoDB's search query is more straightforward for a programmer. A programmer doesn't need to think the logic/relationship behind data fields to do search query.

3.
In MySQL, records can be divided into different tables. A table could be relatively small, which means that querying could be more efficient inside one table.
MongoDB stores every records into one database. Querying needs to scan every records.
