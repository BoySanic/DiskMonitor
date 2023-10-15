#!/bin/bash

disks=("sda" "sdb" "sdc" "sdd" "sde" "sdf")
TrueNAS_Diskmon_out=
# Define ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

for disk in "${disks[@]}"
do
    echo -e "${GREEN}Processing $disk...${NC}"
    /usr/sbin/smartctl -a "/dev/$disk" > "$(echo $TrueNAS_Diskmon_out)/$disk.txt"
    echo -e "${GREEN}Completed processing $disk.${NC}"
done

echo -e "${RED}Changing ownership of files...${NC}"
chown -R admin $(echo $TrueNAS_Diskmon_out)
echo -e "${RED}Ownership changed.${NC}"

echo -e "${GREEN}Script execution completed.${NC}"