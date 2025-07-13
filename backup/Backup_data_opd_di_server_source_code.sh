#!/bin/bash

# Gabung ke source code django_opd_release

# Jalankan di folder Backup
# 1. Backup Folder Media
#sudo rsync -avz -e "ssh -p 5627" webopd@vpn.lombokbaratkab.go.id:/home/webopd/media/crop/2024 . --progress

# sebelum jalankan backup database
# jalankan perintah di bawah ini di komputer source code

# jalankan di folder /var/www

sudo rsync -avz dbopdweb@192.168.13.26:/home/dbopdweb/daily backupdb --progress --ignore-existing 
sudo rsync -avz dbopdweb@192.168.13.26:/home/dbopdweb/weekly backupdb --progress --ignore-existing 
sudo rsync -avz dbopdweb@192.168.13.26:/home/dbopdweb/monthly backupdb --progress --ignore-existing 

# kemudian jalankan chown 
sudo chown -R webopd:webopd backupdb

# 2. Backup Database
# sudo rsync -avz -e "ssh -p 5627" webopd@vpn.lombokbaratkab.go.id:/var/www/backupdb . --progress

