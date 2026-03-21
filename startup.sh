#!/bin/bash
# GovRAG V3 — Azure App Service Startup
pip install -r requirements.txt
uvicorn app.api.main:app --host 0.0.0.0 --port 8000
