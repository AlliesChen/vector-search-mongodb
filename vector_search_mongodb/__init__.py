import sys
import os
import argparse
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import openai

load_dotenv()


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


def generate_embedding(text: str, api_key: str) -> list[float]:
    openai.api_key = api_key
    response = openai.embeddings.create(
        model="text-embedding-ada-002",
        input=[text],
    )
    return response.data[0].embedding

def main(query: str, db_url: str, openai_api_key: str):
    client = connect_to_mongo(db_url)
    if client is None:
        print("Failed to connect to MongoDB. Exiting...")
        sys.exit(1)

    # Assuming you want to interact with the sample_mflix database and movies collection
    db = client.sample_mflix
    movies = db.embedded_movies

    try:
        embedding = generate_embedding(text=query, api_key=openai_api_key)

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
            print(f"Movie Name: {movie["title"]},\nMovie Plot: {movie['plot']}\n")
    except Exception as e:
        print(f"Error while accessing the movies collection: {e}")
    finally:
        # Ensure to close the MongoDB client before exiting
        client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Your query,MongoDB URL, Embedding URL and Huggingface token')
    parser.add_argument('--query', type=str, help='Your query')
    parser.add_argument('--url', type=str, help='MongoDB URL',
                        default=os.getenv("MONGODB_URL"))
    parser.add_argument('--openai-api-key', type=str, help='openai api key',
                        default=os.getenv("OPENAI_API_KEY"))
    args = parser.parse_args()

    main(
        query=args.query,
        db_url=args.url,
        openai_api_key=args.openai_api_key
        )
