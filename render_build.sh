#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Ensure static directory exists and copy favicon
mkdir -p static
if [ ! -f static/favicon.ico ]; then
    echo "favicon.ico not found in static directory"
else
    echo "favicon.ico found in static directory"
fi

# Run database migrations
python manage.py migrate

# Collect static files for WhiteNoise
python manage.py collectstatic --noinput

# Verify favicon was collected
if [ -f staticfiles/favicon.ico ]; then
    echo "favicon.ico successfully collected to staticfiles"
else
    echo "favicon.ico not found in staticfiles - copying manually"
    mkdir -p staticfiles
    cp static/favicon.ico staticfiles/ 2>/dev/null || echo "Failed to copy favicon"
fi
