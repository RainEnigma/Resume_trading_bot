from contextlib import closing

import psycopg2

from config import config


def func_creating_tables():
    creating_tables_in_DB(tab_name='USERS',
                          numb='SERIAL PRIMARY KEY',
                          user_id='integer',
                          name='varchar',
                          user_name='varchar',
                          last_name='varchar',
                          date_add='varchar',
                          additional='integer')


# Функция для создания всех таблиц в базе данных
def creating_tables_in_DB(tab_name, **kwargs):
    forming_string = ''
    for item in kwargs.items():
        forming_string += f'{item[0]} {item[1]},'
    forming_string = forming_string.rstrip(',')

    with closing(psycopg2.connect(dbname=config.name_DB,
                                  user=config.user_DB,
                                  password=config.password_DB,
                                  host=config.host_DB)) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(f"""create table if not exists {tab_name} ({forming_string})""")
