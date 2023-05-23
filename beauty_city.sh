#!/bin/bash
set -e


cd /opt/BeautyCity
git fetch
git pull

cd /opt/BeautyCity/infra
docker compose -f docker-compose.prod.yml --build up -d

echo beauty_city was updated and it will work soon!
