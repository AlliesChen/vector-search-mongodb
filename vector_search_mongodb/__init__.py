import sys
import os
import argparse
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def connect_to_mongo(url: str) -> MongoClient | None:
    try:
        # Create a new client and connect to the server
        client = MongoClient(url, server_api=ServerApi('1'))
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(f"Error while connecting to MongoDB: {e}")
        return None


def main(query: str):
    client = connect_to_mongo(MONGODB_URL)
    if client is None:
        print("Failed to connect to MongoDB. Exiting...")
        sys.exit(1)

    # Assuming you want to interact with the sample_mflix database and movies collection
    db = client.sample_mflix
    movies = db.embedded_movies

    try:
        embedding = generate_embedding(text=query, api_key=OPENAI_API_KEY)

        results = movies.aggregate([
            {
                "$vectorSearch": {
                    "index": "PlotSemanticSearch",
                    "path": "plot_embedding",
                    "queryVector": embedding,
                    "numCandidates": 100,
                    "limit": 4
                }
            }])

        for movie in results:
            print(f"Movie Name: {movie["title"]
                                 },\nMovie Plot: {movie['plot']}\n")
    except Exception as e:
        print(f"Error while accessing the movies collection: {e}")
    finally:
        # Ensure to close the MongoDB client before exiting
        client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Your query string')
    parser.add_argument('--query', type=str, help='Your query')
    args = parser.parse_args()

    main(query=args.query,)
