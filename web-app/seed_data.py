"""Fill the database with fake recordings for development"""

import random
from datetime import datetime, timedelta, timezone

from database import COLLECTION, get_db

TRANSCRIPTS = [
    "hello? hello hello?",
    "the quick brown fox jumps over the lazy dog",
    "sphinx of black quartz judge my vow",
    "can you hear me? can you see me?",
    "5",
]


def build_fake_recordings(count=20):
    """Build fake finished recordings spread over the last two weeks. Uses random picks of integers within ranges to ensure variety"""
    now = datetime.now(timezone.utc)
    docs = []
    for i in range(count):
        avg = random.randint(-45, -20)
        docs.append(
            {
                "seeded": True,  # So we can directly see what entries are from the seeding vs. actual testing/data, and nothing real gets overwritten when re-running this program
                "created_at": now - timedelta(days=random.randint(0, 14)),
                "status": "done",
                "audio_path": f"/data/audio/seed_{i}.webm",
                "mode": "free",
                "transcript": random.choice(TRANSCRIPTS),
                "stats": {
                    "duration_sec": random.randint(3, 45),
                    "avg_loudness_db": random.randint(-20, 120),
                    "max_loudness_db": random.randint(0, 200),
                    "min_loudness_db": random.randint(-40, 40),
                },
            }
        )
    return docs


def main():
    """Remove old seed data, then insert a fresh batch"""
    collection = get_db()[COLLECTION]
    collection.delete_many({"seeded": True})
    docs = build_fake_recordings()
    collection.insert_many(docs)
    print(f"Inserted {len(docs)} fake recordings.")


if __name__ == "__main__":
    main()