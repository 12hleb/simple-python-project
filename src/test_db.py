from sqlalchemy import create_engine, text

# Database connection
DATABASE_URL = "postgresql://postgres:65JobApp!@db.wpxrwqojndtkxdrcqrmu.supabase.co:5432/postgres"

def test_connection():
    try:
        # Create engine
        engine = create_engine(DATABASE_URL)
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text('SELECT 1'))
            print("Database connection successful!")
            return True
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection() 