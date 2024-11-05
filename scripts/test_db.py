import pandas as pd
from src.data.database import get_db

       
async def load_data_2():
    """
    """
    try:
        async with get_db() as cursor:
            query = "SELECT * FROM my_table"
            df = pd.read_sql_query(query, cursor.connection)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

async def pipeline():
    try:
        df = await load_data_2()
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

if __name__ == "__main__":
    import asyncio
    asyncio.run(pipeline())