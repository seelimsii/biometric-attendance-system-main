#!/bin/bash

echo "========================="
echo "Run script inside docker "
echo "========================="
while [ $? -ne 1 ]; do
    container_id=$(docker ps -qf "ancestor=mcr.microsoft.com/mssql/server")
    echo "container_id=$container_id"

    if [ -z "$container_id" ]; then
        echo "Container is not running"
        echo "Sleeping for 5 seconds"
        sleep 1
    else
        echo "Container is running"
        docker exec "$container_id" /scripts/setup-db.sh
        break
    fi
done
echo "========================="
echo "Script executed          "
echo "========================="