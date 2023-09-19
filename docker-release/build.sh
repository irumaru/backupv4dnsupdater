#/bin/bash

# Delete old file.
rm -r ../release/dist

# Build
docker compose build
docker compose up

# Copy config file.
cp ../src/config.sample.yaml ../release/dist

# Create priority file.
touch ../release/dist/priority
echo "AUTO" > ../release/dist/priority

# Update owner.
chown -R 1000:1000 ../release
