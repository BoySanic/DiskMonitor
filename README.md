# DiskMonitor

The goal of this program is to pull smart data for disks (SSDs) on a TrueNAS Scale machine to track writes over time in a database.
I use this for a grafana dashboard mainly.

This program runs on 2-3 nodes.

1. TrueNAS Scale
2. MariaDB/MySQL Server
3. Optional intermediary server (can run directly on the MariaDB server if desired)

Each portion of the program is in its specified folder, including database schema.


getdisks.sh runs on TrueNAS Scale and runs smartctl for desired disks, placing them in a desired path.
I recommend using a real dataset on your zpool to prevent your data from disappearing unexpectedly.
I also recommend placing this in /root/ somewhere. I used /root/scripts. 
There is a small problem where after updating TrueNAS Scale it will remove cron jobs added via command line, so you may have to do it via the web gui.

diskmon.sh and insertDatabase.py run on either the intermediary server or on the MariaDB server, depending on your setup.
diskmon.sh pulls files from the dataset on TrueNAS for parsing, and executes insertDatabase.py.
Preferably add the public key for the user running this script to the admin user on TrueNAS Scale to prevent the need for passwords or anything like that.
insertDatabase.py parses the files and adds the data to the database. If data ends up missing, other than modelfamily (weird TrueNAS change I've not substantiated yet), the script will not insert and instead will put the failed file in /diskmonitor_path/failed for analysis. Feel free to include these in issues.


CreateTables.sql will create the necessary tables in the database.
DiskInfo contains the information about each disk
DiskEntries contains the data we care about pulled each interval.