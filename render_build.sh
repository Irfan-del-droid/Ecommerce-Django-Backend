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

# Ensure favicon is in staticfiles
if [ -f static/favicon.ico ] && [ ! -f staticfiles/favicon.ico ]; then
    echo "Copying favicon.ico to staticfiles directory"
    cp static/favicon.ico staticfiles/
fi

# Verify favicon was collected
if [ -f staticfiles/favicon.ico ]; then
    echo "favicon.ico successfully available in staticfiles"
else
    echo "Warning: favicon.ico not found in staticfiles"
fi
