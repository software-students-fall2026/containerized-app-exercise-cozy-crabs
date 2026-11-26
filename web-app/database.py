"""Database helpers for the web app"""

import os
from datetime import datetime, timezone
from functools import lru_cache

from bson import ObjectId
from bson.errors import InvalidId
from pymongo import MongoClient

COLLECTION = "recordings"


@lru_cache(maxsize=1)  # Prevents the application from creating new clients when requesting the same URI
def get_client(uri):
    """Create the MongoDB client once and reuse it"""
    return MongoClient(uri)


def get_db():
    """Return the database named in MONGO_URI (defaults to local Mongo)"""
    uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/voiceproject")
    return get_client(uri).get_default_database("voiceproject")


def _serialize(doc):
    """Turn the ObjectId into a string so JSON and templates work"""
    if doc is not None:
        doc["_id"] = str(doc["_id"])
    return doc


def insert_recording(audio_path, mode="free"):  # "free" is a placeholder, can be replaced at any time once options are specified
    """Insert a new pending recording and return its id as a string"""
    doc = {
        "created_at": datetime.now(timezone.utc),
        "status": "pending",
        "audio_path": audio_path,
        "mode": mode,
    }
    result = get_db()[COLLECTION].insert_one(doc)
    return str(result.inserted_id)


def get_recording(recording_id):
    """Return one recording, or None if it's missing or the id is invalid"""
    try:
        object_id = ObjectId(recording_id)
    except (InvalidId, TypeError):
        return None
    return _serialize(get_db()[COLLECTION].find_one({"_id": object_id}))


def list_recordings(limit=50):
    """Return recordings, newest first"""
    cursor = get_db()[COLLECTION].find().sort("created_at", -1).limit(limit)
    return [_serialize(doc) for doc in cursor]