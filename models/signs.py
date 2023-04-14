import json
from models.sql import *


class Sign:
    table_name = 'signs'
    query = \
        '''
            id INTEGER PRIMARY KEY,
            sign_num INTEGER,
            name varchar(50) NOT NULL,
            translated_name varchar(50) NOT NULL,
            horoscope_type varchar(10) NOT NULL,
            start_date varchar(10),
            end_date varchar(10)
        '''
    create_table(table_name, query, remove_previous=False)

    @classmethod
    def add_sign(cls, sign_id: int, name: str, translated_name: str, horoscope_type: str, start_date: str | None,
                 end_date: str | None):
        insert_into(cls.table_name, ['sign_num', 'name', 'translated_name', 'horoscope_type', 'start_date', 'end_date'],
                    [sign_id, name, translated_name, horoscope_type, start_date, end_date])

    @classmethod
    def add_all_signs_from_json(cls) -> None:
        with open(f'{cls.table_name}.json', 'r', encoding='utf-8') as file:
            parsed_signs = json.load(file)
            for sign in parsed_signs:
                cls.add_sign(sign['sign_num'], sign['name'], sign['translated_name'], sign['horoscope_type'],
                             sign.get('start_date'), sign.get('end_date'))

    @classmethod
    def get_all_signs(cls, horoscope_type: str | None) -> list:
        condition = f'horoscope_type LIKE "{horoscope_type}"' if horoscope_type else None
        all_signs = select_all(table_name=cls.table_name, columns=['*'], condition=condition)
        return all_signs

    @classmethod
    def get_sign_by_translated_name(cls, translated_name: str, horoscope_type: str):
        sign = select_one(table_name=cls.table_name, columns=['id', 'sign_num', 'name', 'translated_name', 'horoscope_type'],
                          condition=f'translated_name LIKE "%{translated_name.capitalize()}%" AND horoscope_type LIKE "{horoscope_type}"')
        return sign

    @classmethod
    def get_cl_sign_by_date(cls, date: str):
        all_signs = select_all(table_name=cls.table_name, columns=['*'], condition=f'horoscope_type LIKE "cl"')
        day, month = list(map(int, date.split('-')))
        for sign in all_signs:
            start_date, end_date = sign[-2].split('-'), sign[-1].split('-')
            if (day >= int(start_date[0]) and month == int(start_date[1])) or \
                    (day <= int(end_date[0]) and month == int(end_date[1])):
                return sign[:-2]
