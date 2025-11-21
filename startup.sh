#!/usr/bin/env sh

set -e #exit on error

pip install -r requirements.txt 
alembic upgrade head 
cd frontend
npm install
npm run build