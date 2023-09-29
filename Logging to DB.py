class connection_db:

    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self._conn = ps.connect(host=self.host, database=self.database, user=self.user, password=self.password,
                                port=self.port)
        self._cursor = self._conn.cursor()

    def distinct_links(self, table, column):
        query = f"select {column} from {table}"
        sql_table = pd.read_sql(query, self._conn)

        return list(sql_table[column].unique())

    def distinct_cat(self, table, column, message):
        link = "'" + str(message.text) + "'"
        query = f"select distinct {column} from {table} where link = {link}"
        sql_table = pd.read_sql(query, self._conn)

        return list(sql_table['link_user_description'].unique())

    def distinct_links_cat(self, table, column, cat):
        query = f"select date_add,{column} from {table} where link_user_description = '{cat}'"
        sql_table = pd.read_sql(query, self._conn)

        return list(sql_table[column].unique())

    def user_distinct_links(self, table, message):
        user_id = "'" + str(message.from_user.id) + "'"
        query = f"select link from {table} where user_id = {user_id}"
        sql_table = pd.read_sql(query, self._conn)

        return list(sql_table['link'].unique())

    def distinct_user_id(self, table):
        query = f"select user_id from {table} "
        sql_table = pd.read_sql(query, self._conn)
        return list(sql_table['user_id'].unique())

    def distinct_user_id_count(self, table):
        query = f"select  user_id from {table} where dt = (select max(dt) from {table})"
        sql_table = pd.read_sql(query, self._conn)
        return sql_table['user_id'].nunique()

    def write_to_db(self, table, message, word):
        today_date = "'" + str(dt.datetime.strftime(dt.datetime.today(), "%d.%m.%Y")) + "'"
        user_id = "'" + str(message.from_user.id) + "'"
        user_name = "'" + str(message.from_user.first_name) + "'"
        status = "'" + 'New' + "'"
        # category_of = "'" + str(cat) + "'"
        link_user_description = "'" + str(message.text) + "'"
        # cursor = self._conn.cursor()
        self._cursor.execute(f'INSERT INTO {table}\
            (date_add,user_id,user_name,status,link,link_user_description) \
            VALUES ({today_date},{user_id},{user_name},{status},{word},{link_user_description})')
        self._conn.commit()

    def logging(self, table, message,message_data):
        today_date = "'" + str(dt.datetime.strftime(dt.datetime.today(), "%d.%m.%Y")) + "'"
        user_id = "'" + str(message.from_user.id) + "'"
        user_name = "'" + str(message.from_user.first_name) + "'"
        message = "'" + str(message_data) + "'"
        self._cursor.execute(f'INSERT INTO {table}\
                    (dt,user_id,user_name,message) \
                    VALUES ({today_date},{user_id},{user_name},{message})')
        self._conn.commit()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._conn.commit()
        self._conn.close()
