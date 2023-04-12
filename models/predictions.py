from models.sql import *
import json
import random


class Prediction:
    table_name = 'predictions'
    query = \
        '''
            id INTEGER PRIMARY KEY,
            prediction varchar(350) NOT NULL
        '''
    create_table(table_name, query, remove_previous=False)

    @classmethod
    def get_random_prediction(cls):
        count = select_one(cls.table_name, columns=['COUNT(*)'])[0]
        random_num = random.randint(1, count)
        return select_one(table_name=cls.table_name, columns=['prediction'], condition=f'id = {random_num}')

    @classmethod
    def add_prediction(cls, prediction: str) -> None:
        insert_into(table_name=cls.table_name, columns=['prediction'], values=[prediction])

    @classmethod
    def add_all_predictions_from_json(cls) -> None:
        with open(f'{cls.table_name}.json', 'r', encoding='utf-8') as file:
            parsed_predictions = json.load(file)
            for prediction in parsed_predictions:
                cls.add_prediction(prediction=prediction['prediction'])
