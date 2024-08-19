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
CSV_FOLDER="data/raw"
CSV_FOLDER_MODIFY="$CSV_FOLDER/tmp"

# Check if the container exists
CONTAINER_EXISTS=$(docker ps -a --filter name="$CONTAINER_NAME" --quiet)

if [ -z "$CONTAINER_EXISTS" ]; then
    # Container doesn't exist, create a new one
    echo "PostgreSQL container doesn't exist. Creating a new one..."
    docker run -d --name "$CONTAINER_NAME" -e POSTGRES_PASSWORD=funky -p 5432:5432 postgres
    echo "PostgreSQL container created successfully."
else
    # Container exists, check if it's running
    CONTAINER_STATUS=$(docker inspect --format='{{.State.Running}}' "$CONTAINER_NAME")

    if [ "$CONTAINER_STATUS" == "true" ]; then
        echo "PostgreSQL container is already running."
    else
        echo "PostgreSQL container exists but is not running. Starting the container..."
        docker start "$CONTAINER_NAME"
        echo "PostgreSQL container started successfully."
    fi
fi

# Check if the database exists
DB_EXISTS=$(docker exec "$CONTAINER_NAME" psql -lqt | cut -d \| -f 1 | grep -w "$DB_NAME" | wc -l)

if [ "$DB_EXISTS" -eq 0 ]; then
    # Database doesn't exist, create a new one
    echo "Database '$DB_NAME' doesn't exist. Creating a new one..."
    docker exec -it "$CONTAINER_NAME" psql -U postgres -c "CREATE DATABASE $DB_NAME;"
    echo "Database '$DB_NAME' created successfully."
else

    echo "Database '$DB_NAME' already exists."
fi


# =====
# table : DATA
# =====

# Check if the table data exists
TABLE_DATA_EXISTS=$(docker exec "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -c "
    SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_name = '$TBL_DATA'
    );" -tAX)

if [ "$TABLE_DATA_EXISTS" = "t" ]; then
    # Table exists, try to delete it
    echo "Deleting table '$TBL_DATA'..."
    docker exec "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -c "DROP TABLE $TBL_DATA;" || true
fi


# Create the table
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

echo "Table '$TBL_DATA' created successfully."

# =====
# table : USER
# =====

# Check if the table data exists
TABLE_USER_EXISTS=$(docker exec "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -c "
    SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_name = '$TBL_USER'
    );" -tAX)

if [ "$TABLE_USER_EXISTS" = "t" ]; then
    # Table exists, try to delete it
    echo "Deleting table '$TBL_USER'..."
    docker exec "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -c "DROP TABLE $TBL_USER;" || true
fi

# Create the table
docker exec -i $CONTAINER_NAME psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME <<EOF
CREATE TABLE IF NOT EXISTS $TBL_USER (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user'
);
EOF

echo "Table '$TBL_USER' created successfully."
# =====
# POPULATE TABLES
# =====

# OHCVLT DATA
# ===========

# Check if the folder exists
if [ ! -d "$CSV_FOLDER" ]; then
    echo "Error: The specified folder '$CSV_FOLDER' does not exist."
    exit 1
else
    echo "folder "$CSV_FOLDER" checked"
fi

# Create a temporary folder to store modified CSV files
if [ -d "$CSV_FOLDER_MODIFY" ]; then
  rm -rf "$CSV_FOLDER_MODIFY"
fi
mkdir -p "$CSV_FOLDER_MODIFY"

# Process each CSV file
for file in $CSV_FOLDER/*.csv; do
    echo "process file: $file"
    # Extract pair from the file name
    pair=$(basename "$file" | cut -d'_' -f1)
    filename=$(basename "$file")
    # Add a new column with the prefix value at the beginning of each line
    awk -v prefix="$pair" 'BEGIN {FS=OFS=","} NR==1 {print "new_column",$0} NR>1 {print prefix,$0}' "$file" > "$CSV_FOLDER_MODIFY/$filename"
done

# Combine all CSV files into one*
echo "combine all csv from $CSV_FOLDER_MODIFY ..."
cat $CSV_FOLDER_MODIFY/*.csv > combined.csv
# Copy the combined CSV file into the Docker container
echo "copy combined csv file from $CSV_FOLDER_MODIFY to Container ..."
docker cp combined.csv $CONTAINER_NAME:/combined.csv

# Access the PostgreSQL container and run the COPY command
echo "Create table $DB_NAME and bulk import data"
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

echo "Data OHCVLT import completed."


# USER DATA
# ===========

# Copy the JSON file into the Docker container
docker cp "$JSON_FILE_PATH" "$CONTAINER_NAME":/tmp/file.json

docker exec -i "$CONTAINER_NAME" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "
    COPY $TABLE_NAME FROM '/tmp/file.json'
    WITH (
        FORMAT 'json',
        FREEZE 'true'
    );
"