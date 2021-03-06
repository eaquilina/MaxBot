from datetime import date 
from datetime import datetime
from datetime import timedelta
import pymongo


class DB:
    
    def __init__(self, db_name):
        if not hasattr(self, 'db'):
            self.db = self.connect(db_name)

    def connect(self, db_name, hostname='localhost', port=27017):
        client = pymongo.MongoClient(f'mongodb://{hostname}:{port}/')
        return client[db_name]

    def insert_event(self, collection, event):
        result = self.db[collection].update(
            {'category': event.category, 'event_date': event.event_date, 'source': event.source},
            {
                '$setOnInsert': vars(event),
            },
            upsert=True
        )
        return result

    def get_events_for_date(self, collection, date):

        # current_date = datetime.combine(date.today(), datetime.min.time())
        current_date = datetime.combine(date, datetime.min.time())
        next_date = current_date + timedelta(days=1)

        return self.db[collection].find(
        { '$and': [ 
                {
                    'event_date': {
                        '$gte': current_date
                    }
                }, 
                {
                    "event_date": {
                        '$lt': next_date
                    }
                } 
            ] 
        })

    def create_financial_event(self, collection, event_to_update, new_field, new_info):
        result = self.db[collection].update_one(
            {'_id': event_to_update['_id']},
            {
                '$set':
                {
                    new_field: new_info
                },
                '$currentDate':
                {
                    'modified_date': True
                },
            },
            upsert=True
        )

        return result.raw_result