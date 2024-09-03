from fastapi import FastAPI, Request
from pydantic import BaseModel
import motor.motor_asyncio
import urllib.parse
import uvicorn

app = FastAPI()

username = urllib.parse.quote_plus("hsundar2004")
password = urllib.parse.quote_plus("Hsundar@2004")

uri = f"mongodb+srv://{username}:{password}@mycluster.oilvp.mongodb.net/?retryWrites=true&w=majority&appName=MyCluster"
client = motor.motor_asyncio.AsyncIOMotorClient(uri)

db = client.smartaid  # Replace with your database name
collection = db.box  # Replace with your collection name

# Pydantic model for data validation
class NameModel(BaseModel):
    name: str

@app.get("/")
def hello_world():
    return {"message": "Hello World"}

@app.post("/hello")
async def reply(request: Request):
    data = await request.json()  # Extract the JSON body from the request
    box_id = data.get("box_id")  # Get the 'name' from the JSON, or use 'Guest' as default
    tablet_name = data.get("tablet_name")  # Get the 'name' from the JSON, or use 'Guest' as default
    expiry_date = data.get("expiry_date") # Get the 'name' from the JSON, or use 'Guest' as default
    
    # Save data to MongoDB
    document = {"box_id": box_id, "tablet_name": tablet_name, "expiry_date": expiry_date}
    result = await collection.insert_one(document)

    return {"message": f"Saved", "id": str(result.inserted_id)}  # Return a JSON response with MongoDB ID

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
