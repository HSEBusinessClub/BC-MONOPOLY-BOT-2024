import os
import psycopg2
from psycopg2.extensions import cursor, connection

def ADD_USER(user_chat_id) -> str:
    return f"""
    do $$
    begin
      IF NOT EXISTS (SELECT * FROM users WHERE chat_id='{user_chat_id}') THEN
      INSERT INTO users (chat_id) VALUES ({user_chat_id});
      END IF;
    end
    $$
"""

def ADD_NOTE(user_chat_id, partner_name) -> str:
    return f"""
    do $$
    begin
    IF NOT EXISTS 
      (SELECT * FROM user_visited_partner 
      WHERE user_id=(SELECT user_id FROM users WHERE chat_id='{user_chat_id}') AND
      partner_id=(SELECT partner_id FROM partners WHERE partner_name='{partner_name}')
      ) THEN
    INSERT INTO user_visited_partner (user_id, partner_id)
    VALUES 
    (
      (SELECT user_id FROM users WHERE chat_id='{user_chat_id}'), 
      (SELECT partner_id FROM partners WHERE partner_name='{partner_name}')
    );
    END IF;
    end
    $$
"""

def GET_ALL_USERS() -> str:
    return "SELECT chat_id FROM users" 


def init_db() -> tuple[connection, cursor]:
    user_name = os.environ["POSTGRES_USER"]
    db_password = os.environ["POSTGRES_PASSWORD"]
    db_name = os.environ["POSTGRES_DB_NAME"]

    connection = psycopg2.connect(host="localhost", user=user_name,
                                  password=db_password, database=db_name)
    cursor = connection.cursor()

    connection.commit()
    return connection, cursor