import sqlite3
from config import DATABASE

skills = [ (_,) for _ in (['Python', 'SQL', 'API', 'Telegram'])]
statuses = [ (_,) for _ in (['На этапе проектирования', 'В процессе разработки', 'Разработан. Готов к использованию.', 'Обновлен', 'Завершен. Не поддерживается'])]

class DB_Manager:
    def __init__(self, database):
        self.database = database

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE projects (
                            project_id INTEGER PRIMARY KEY,
                            user_id INTEGER,
                            project_name TEXT NOT NULL,
                            project_coord TEXT NOT NULL
                        )''')
            conn.commit()
        print("База данных успешно создана.")

    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()

    def __select_data(self, sql, data = tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()
        
    def insert_project(self, data):
        sql = 'INSERT OR IGNORE INTO projects (user_id, project_name, project_coord) values(?, ?, ?, ?)'
        self.__executemany(sql, data)

    def insert_skill(self, user_id, project_name, skill):
        sql = 'SELECT project_id FROM projects WHERE project_name = ? AND user_id = ?'
        project_id = self.__select_data(sql, (project_name, user_id))[0][0]
        skill_id = self.__select_data('SELECT skill_id FROM skills WHERE skill_name = ?', (skill,))[0][0]
        data = [(project_id,skill_id)]
        sql = 'INSERT OR IGNORE INTO project_skills VALUES (?, ?)'
        self.__executemany(sql, data)

    def get_projects(self, user_id):
        return self.__select_data(sql='SELECT * FROM projects WHERE user_id = ?', data = (user_id,))

    def get_project_id(self, project_name, user_id):
        return self.__select_data(sql='SELECT project_id FROM projects WHERE project_name = ? AND user_id = ?  ', data = (project_name, user_id,))[0][0]

    def get_project_info(self, user_id, project_name):
        sql = """
SELECT project_name, project_coord FROM projects 
WHERE project_name=? AND user_id=?
"""
        return self.__select_data(sql=sql, data = (project_name, user_id))
    

    def update_projects(self, param, data):
        self.__executemany(f"UPDATE projects SET {param} = ? WHERE project_name = ? AND user_id = ?", [data]) # data ('atr', 'mew', 'name', 'user_id')


    def delete_project(self, user_id, project_id):
        sql = "DELETE FROM projects WHERE user_id = ? AND project_id = ? "
        self.__executemany(sql, [(user_id, project_id)])

if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    manager.create_tables()
    manager.default_insert()
