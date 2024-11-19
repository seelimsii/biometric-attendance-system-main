#!/bin/bash

echo "========================="
echo "   Changing Directory    "
echo "========================="
cd ./deploy/local/

echo "========================="
echo "Changing file permissions"
echo "========================="
sudo chown -R 10001:1000 mssql/data mssql/data
sudo chown -R 10001:1000 mssql/data mssql/log
sudo chmod -R +x mssql/scripts/*

echo "========================="
echo "  Set VM overcommit mem  "
echo "========================="
sudo sysctl vm.overcommit_memory=1

echo "========================="
echo "  Starting mssql setup   "
echo "========================="
chmod +x ./scripts/mssql-setup.sh
sh ./scripts/mssql-setup.sh > ./mssql-setup.log 2>&1 &

echo "========================="
echo " Starting docker compose "
echo "========================="
docker compose -f docker-compose.yml up \
       --remove-orphans

echo "========================="
echo "       Move back         "
echo "========================="
cd -