import mariadb
import sys
import shutil
from datetime import datetime
import configparser
import os

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user=config.get('Database', 'user'),
        password=config.get('Database', 'password'),
        host=config.get('Database', 'host'),
        port=int(config.get('Database', 'port')),
        database=config.get('Database', 'database')
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

disks_tracked = config.get('Disks', 'tracked_disks').split(',')
timestamp = datetime.utcnow()

for disk in disks_tracked:
    lbas = -1
    drive_health = -1
    serial = ''
    model = ''
    modelfamily = ''
    capacity = ''
    capacitybytes = -1
    sectorsize = -1
    diskid = -1
    file_path = os.path.join(config.get('Paths', 'diskmonitor_path'), f"{disk}.txt")

    if(os.path.isfile(file_path)):
      with open(file_path) as f:
          lines = f.readlines()

          for line in lines:
              if "Model Family" in line:
                  modelfamily = line.split(':')[-1].strip()

              if "Device Model" in line:
                  model = line.split(':')[-1].strip()

              if "Serial Number" in line:
                  serial = line.split(':')[-1].strip()

              if "User Capacity" in line:
                  capacitybytesstr = line.split('b')[0].split(':')[-1].strip()
                  capacitybytes = int(capacitybytesstr.replace(',', ''))
                  capacity = line.split('[')[-1].split(']')[0].strip()

              if "Total_LBAs_Written" in line:
                  lbas = int(line.split()[-1])

              if "Percent_Lifetime_Remain" in line or "Wear_Leveling_Count" in line:
                  drive_health = int(line.split()[3])

              if "Sector Size" in line:
                  sectorsize = int(line.split(':')[-1].split('b')[0].strip())

      strtimestamp = timestamp.strftime('%G-%m-%dT%H%M')
      if lbas == -1 or drive_health == -1 or capacity == '' or serial == '' or model == '' or sectorsize == -1:
          dest_path = os.path.join(config.get('Paths', 'failed_path'), f"{disk}-{strtimestamp}.txt")
          shutil.copyfile(file_path, dest_path)
          f1 = open(dest_path, 'a')
          f1.write("Error! LBAS: {} drive_health {}, capacity {} serial {} model {} modelfamily {} sectorsize {}".format(lbas, drive_health, capacity, serial, model, modelfamily, sectorsize))
      else:
          try:
              cur.execute("SELECT id FROM DiskInfo WHERE serial=?", (serial,))
          except mariadb.Error as e:
              print(f"Error: {e}")

          if cur.rowcount > 0:
              diskid = cur.fetchone()[0]
          else:
              try:
                  cur.execute("INSERT INTO DiskInfo (Serial, Model, ModelFamily, Capacity, CapacityBytes, SectorSize) VALUES (?, ?, ?, ?, ?, ?)", 
                              (serial, model, modelfamily, capacity, capacitybytes, sectorsize))
                  conn.commit()
                  diskid = cur.lastrowid
              except mariadb.Error as e:
                  print(f"Error: {e}")

          try:
             cur.execute("INSERT INTO DiskEntries (DiskID, Percent_Life_Remain, DiskTBW, timestamp) VALUES (?, ?, ?, ?)", 
             (diskid, drive_health, float((lbas * sectorsize) / 1000000000000), timestamp))
             conn.commit()
          except mariadb.Error as e:
             print(f"Error: {e}")

conn.close()