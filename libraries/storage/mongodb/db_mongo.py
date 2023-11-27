# from .connect import connect_mongodb
# from libraries.config import HISTORICAL_DATA_DB_NAME


# def insert_data(data):
#     db = connect_mongodb()
    
#     collection = db[HISTORICAL_DATA_DB_NAME]
    
#     # Convert DataFrame to a dictionary and insert into MongoDB
#     records = data.to_dict(orient='records')
#     collection.insert_many(records)
    
#     print(f'DataFrame saved to MongoDB.')
    
    