import environment

from model import Entry
from model import db
from datetime import datetime


def worker(event, context):
  """Handler for processing batch event to database ingestion"""
  for record in event['Records']:
    timestamp = float(record['attributes']['SentTimestamp']) / 1000
    body = record['body']
    hash_key = record['md5OfBody']
    entry = Entry(created_at=datetime.fromtimestamp(timestamp), content=body, hash_key=hash_key)
    db.session.add(entry)
  else:
    db.session.commit()
  return None