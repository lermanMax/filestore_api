#!/bin/bash
gunicorn -b localhost:8000 filestore_api:app --daemon