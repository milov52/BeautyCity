#!/bin/bash
set -e


cd /opt/beauty_city
git fetch
git pull

cd /opt/beauty_city/infra
docker compose -f docker-compose.prod.yml --build up -d

echo beauty_city was updated and it will work soon!
