#!/bin/bash

# Set the database connection details
DB_HOST="localhost"
DB_PORT="5432"
CONTAINER_NAME="cpostgres"
DB_NAME="ohlcvt"
TBL_DATA="historical"
TBL_USER="user"
DB_USER="postgres"
DB_PASSWORD="funky"

# Set the folder path containing the CSV files
JSON_USER_FILE="users.csv"
JSON_USER_FILE_FOLDER="data/"
JSON_USER_FILE_PATH="$JSON_USER_FILE_FOLDER$JSON_USER_FILE"
CSV_FOLDER="data/raw"
CSV_FOLDER_MODIFY="$CSV_FOLDER/tmp"

# Check if the container exists
echo "=====Docker Container====="
CONTAINER_EXISTS=$(docker ps -a --filter name="$CONTAINER_NAME" --quiet)
echo ">Container name: $CONTAINER_NAME exist, drop it ..."
if [ -z "$CONTAINER_EXISTS" ]; then
    # Stop the container first
    docker stop "$CONTAINER_NAME"
    docker rm "$CONTAINER_NAME"
fi

echo "=====PostgrSQL Container====="
echo "> Creating PostgreSQL container ..."
docker run -d --name "$CONTAINER_NAME" -e POSTGRES_PASSWORD=funky -p 5432:5432 postgres
echo "> ...done"

echo "> Creating Database '$DB_NAME' ..."
docker run --name DB_NAME -e POSTGRES_PASSWORD=DB_PASSWORD -d postgres
echo "> ...done"

# =====
# table : DATA & USER
# =====

echo "=====Create table : $TBL_DATA, $TBL_USER====="

# Create the historical data 
echo "> Creating Table '$TBL_DATA' ..."
docker exec -i $CONTAINER_NAME psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME <<EOF
CREATE TABLE IF NOT EXISTS $TBL_DATA (
    asset TEXT,
    epoch BIGINT,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume NUMERIC,
    trades NUMERIC
);
EOF

echo "> ...done"

# Create the user table
echo "> Creating Table '$TBL_USER' ..."
docker exec -i $CONTAINER_NAME psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME <<EOF
CREATE TABLE IF NOT EXISTS "$TBL_USER" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user'
);
EOF

echo "> ...done"


# =====
# POPULATE TABLES
# =====

echo "=====Upload data into table : $TBL_DATA====="

# Check if the folder exists
if [ ! -d "$CSV_FOLDER" ]; then
    echo ">Error: The specified folder '$CSV_FOLDER' does not exist."
    exit 1
else
    echo ">folder "$CSV_FOLDER" checked"
fi

# Create a temporary folder to store modified CSV files
if [ -d "$CSV_FOLDER_MODIFY" ]; then
  rm -rf "$CSV_FOLDER_MODIFY"
fi
mkdir -p "$CSV_FOLDER_MODIFY"

# Process each CSV file
for file in $CSV_FOLDER/*.csv; do
    echo "----- process file: $file"
    # Extract pair from the file name
    pair=$(basename "$file" | cut -d'_' -f1)
    filename=$(basename "$file")
    # Add a new column with the prefix value at the beginning of each line
    awk -v prefix="$pair" 'BEGIN {FS=OFS=","} NR==1 {print "new_column",$0} NR>1 {print prefix,$0}' "$file" > "$CSV_FOLDER_MODIFY/$filename"
done

# Combine all CSV files into one*
echo ">combine all csv from $CSV_FOLDER_MODIFY ..."
cat $CSV_FOLDER_MODIFY/*.csv > combined.csv
# Copy the combined CSV file into the Docker container
echo ">copy combined csv file from $CSV_FOLDER_MODIFY to Container ..."
docker cp combined.csv $CONTAINER_NAME:/combined.csv

# Access the PostgreSQL container and copy user data to table
echo ">Create table $TBL_DATA and bulk import data"
docker exec -i $CONTAINER_NAME psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME <<EOF
DO \$\$
BEGIN
    BEGIN
        COPY $TBL_DATA (asset, epoch, open, high, low, close, volume, trades)
        FROM '/combined.csv' DELIMITER ',' CSV HEADER;
    EXCEPTION WHEN OTHERS THEN
        RAISE NOTICE 'Skipping problematic line: %', SQLERRM;
            END;
END \$\$;
EOF
rm /combined.csv
echo ">Data OHCVLT import completed."


echo "=====Upload data into table : $TBL_USER====="

# Copy the JSON file into the Docker container
docker cp $JSON_USER_FILE_PATH $CONTAINER_NAME:/
echo "$JSON_USER_FILE_PATH"
echo "---"
# Connect to the PostgreSQL container and load the data
docker exec -i $CONTAINER_NAME psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME <<EOF
DO \$\$
BEGIN
    BEGIN
        COPY $TBL_USER (id,username,email,hashed_password,role)
        FROM '/"$JSON_USER_FILE_PATH"' DELIMITER ',' CSV HEADER;
    EXCEPTION WHEN OTHERS THEN
        RAISE NOTICE 'Skipping problematic line: %', SQLERRM;
            END;
END \$\$;
EOF
rm "/$JSON_USER_FILE_PATH"

echo "Users import completed."

echo "..... └[°=°]┘ ....  waiting order master !"