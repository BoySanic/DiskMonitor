#!/bin/bash

diskspassed=0
attempts=0
failure=0
max_attempts=5
log_file=
PYTHON3_PATH=
Identity_Path=
SSH_User=
TrueNAS_Host=
TrueNAS_Path=
Local_DiskMonitor_Path=
Scripts_Location=


while [ $diskspassed = 0 ]
do
  current_time=$(date +"%Y-%m-%d %H:%M:%S")
  echo "$current_time - Attempt $attempts: Copying files from remote host..." >> "$log_file"
  /bin/scp -i $(echo $Identity_Path) $(echo $SSH_User)@$(echo $TrueNAS_Host):$(echo $TrueNAS_Path) $(echo $Local_DiskMonitor_Path)
  $(echo $PYTHON3_PATH) $(echo $Scripts_Location)/insertDatabase.py

  if [ $? = 0 ]
  then
      echo "$current_time - Attempt $attempts: Successfully processed files." >> "$log_file"
      diskspassed=1
  else
      attempts=$((attempts+1))
      echo "$current_time - Attempt $attempts: Failed to process files." >> "$log_file"
  fi

  if [ $attempts = $max_attempts ]
  then
      diskspassed=1
      failure=1
      echo "$current_time - Maximum attempts reached. Exiting." >> "$log_file"
  fi
done

echo "Attempts: $attempts"
echo "Failure: $failure"
