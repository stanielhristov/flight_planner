import psycopg2


def get_connection(): return psycopg2.connect(database="postgres",
                                              host="localhost",
                                              user="admin",
                                              password="admin",
                                              port="5432")
