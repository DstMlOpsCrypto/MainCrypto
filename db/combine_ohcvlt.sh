#!/bin/bash

# Process each CSV file
for file in /ohcvlt/raw/*.csv; do
    echo "...process file: $file"
    # Extract pair from the file name
    pair=$(basename "$file" | cut -d'_' -f1)
    filename=$(basename "$file")
    # Add a new column with the prefix value at the beginning of each line
    awk -v prefix="$pair" 'BEGIN {FS=OFS=","} NR==1 {print "new_column",$0} NR>1 {print prefix,$0}' "$file" > "/ohcvlt/combine.csv"
done

# Access the PostgreSQL container and copy user data to table

cat << EOF > "TMP_SQL_FILE"
DO \$\$
BEGIN

    BEGIN
        COPY mytable (asset, epoch, open, high, low, close, volume, trades)
        FROM '/ohcvlt/combine.csv' DELIMITER ',' CSV HEADER;
    EXCEPTION WHEN OTHERS THEN
        RAISE NOTICE 'Skipping problematic line: %', SQLERRM;
    END;
END \$\$;
EOF

# Execute the SQL commands using psql
PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DB" -U "$POSTGRES_USER" -f /sql/create_tables.sql

# Remove the temporary SQL file
rm "$TMP_SQL_FILE"