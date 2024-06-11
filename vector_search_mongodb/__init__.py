import sys
import os
import argparse
import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

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


def generate_embedding(url: str, token: str, text: str) -> list[float]:
    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {token}"},
        json={"inputs": text},
    )

    if response.status_code != 200:
        raise ValueError(
            f"Request failed with status {response.status_code}: {response.text}")

    return response.json()


def main(db_url: str, embedding_url: str, huggingface_token: str):
    client = connect_to_mongo(db_url)
    if client is None:
        print("Failed to connect to MongoDB. Exiting...")
        sys.exit(1)

    # Assuming you want to interact with the sample_mflix database and movies collection
    db = client.sample_mflix
    movies = db.movies

    try:
        generate_embedding(embedding_url, huggingface_token, "I love MongoDB!")
        # for movie in movies.find({"plot": {"$exists": True}}).limit(50):
        #     movie["plot_embedding_hf"] = generate_embedding(
        #         embedding_url, huggingface_token, movie["plot"])
        #     movies.replace_one({"_id": movie["_id"]}, movie)
    except Exception as e:
        print(f"Error while accessing the movies collection: {e}")
    finally:
        # Ensure to close the MongoDB client before exiting
        client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='MongoDB URL, Embedding URL and Huggingface token')
    parser.add_argument('--url', type=str, help='MongoDB URL',
                        default=os.getenv("MONGODB_URL"))
    parser.add_argument('--embedding-url', type=str, help='Embedding URL',
                        default=os.getenv("EMBEDDING_URL"))
    parser.add_argument('--huggingface-token', type=str, help='huggingface token',
                        default=os.getenv("HUGGINGFACE_TOKEN"))
    args = parser.parse_args()

    main(args.url, args.embedding_url, args.huggingface_token)
