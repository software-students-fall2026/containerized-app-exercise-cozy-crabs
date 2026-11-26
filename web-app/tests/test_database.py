"""Tests for the web database helpers"""

from datetime import datetime, timedelta, timezone

import database


def test_insert_recording_creates_pending_doc(test_db):
    """New recordings start as pending with the right fields"""
    recording_id = database.insert_recording("/data/audio/a.webm")

    doc = test_db[database.COLLECTION].find_one()

    assert str(doc["_id"]) == recording_id
    assert doc["status"] == "pending"
    assert doc["mode"] == "free"
    assert doc["audio_path"] == "/data/audio/a.webm"


def test_get_recording_returns_string_id():
    """The returned id is a string, not an ObjectId"""
    recording_id = database.insert_recording("/data/audio/a.webm")

    doc = database.get_recording(recording_id)

    assert doc["_id"] == recording_id
    assert doc["audio_path"] == "/data/audio/a.webm"


def test_get_recording_missing_or_invalid():
    """Unknown or malformed ids give None instead of crashing"""
    assert database.get_recording("not-an-id") is None
    assert database.get_recording("0" * 24) is None
    assert database.get_recording(None) is None


def test_list_recordings_newest_first(test_db):
    """Newest recordings come first, and the limit is respected"""
    now = datetime.now(timezone.utc)

    for minutes in (30, 10, 20):
        test_db[database.COLLECTION].insert_one(
            {
                "created_at": now - timedelta(minutes=minutes),
                "status": "done",
            }
        )

    docs = database.list_recordings()

    times = [doc["created_at"] for doc in docs]

    assert times == sorted(times, reverse=True)
    assert len(database.list_recordings(limit=2)) == 2


def test_list_recordings_empty(test_db):
    """An empty database gives an empty list"""
    assert database.list_recordings() == []


def test_get_db_uses_mongo_uri(test_db):
    """get_db picks the database name from MONGO_URI"""
    assert test_db.name == "voiceproject_web_test"
