#!/usr/bin/env sh

pip install -r requirements.txt 
alembic upgrade head 
cd frontend
npm install
npm run build