from fastapi import FastAPI, Request
from pydantic import BaseModel
import pymongo
import urllib.parse
import uvicorn

app = FastAPI()

# URL encode the username and password
username = urllib.parse.quote_plus("hsundar2004")
password = urllib.parse.quote_plus("Hsundar@2004")

# MongoDB URI connection string
uri = f"mongodb+srv://{username}:{password}@mycluster.oilvp.mongodb.net/?retryWrites=true&w=majority&appName=MyCluster"

# Create a MongoDB client
client = pymongo.MongoClient(uri)

# Define the database and collection
db = client.smartaid  # Replace with your database name
collection = db.box  # Replace with your collection name

# Pydantic model for data validation
class NameModel(BaseModel):
    box_id: str
    tablet_name: str
    expiry_date: str

@app.get("/")
def hello_world():
    return {"message": "Hello World"}

@app.post("/hello")
async def reply(request: Request):
    data = await request.json()  # Extract the JSON body from the request
    box_id = data.get("box_id")  # Get 'box_id' from the JSON
    tablet_name = data.get("tablet_name")  # Get 'tablet_name' from the JSON
    expiry_date = data.get("expiry_date")  # Get 'expiry_date' from the JSON
    
    # Save data to MongoDB
    document = {"box_id": box_id, "tablet_name": tablet_name, "expiry_date": expiry_date}
    result = collection.insert_one(document)

    return {"message": f"Saved", "id": str(result.inserted_id)}  # Return a JSON response with MongoDB ID

# Uvicorn entry point for local development
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
