import sqlite3 as sq

class DB:
    @staticmethod
    def TryGetOptionsFromDataBase():
        prevRecord = None
        
        with sq.connect('OptionsAPI.db') as con:
            cur = con.cursor()

            cur.execute(f"""CREATE TABLE IF NOT EXISTS options (
                            token text, 
                            secretToken text, 
                            language text);
            """)

            cur.execute(f"""SELECT * FROM options;
            """)
            prevRecord = cur.fetchone()

        if prevRecord != None:
            return (prevRecord[0], prevRecord[1], prevRecord[2])
        
        return ('', '', '')
            
    @staticmethod
    def SaveOptionsDataBase(token, secretToken, language):
        with sq.connect('OptionsAPI.db') as con:
            cur = con.cursor()

            cur.execute(f"""CREATE TABLE IF NOT EXISTS options (
                            token text, 
                            secretToken text, 
                            language text);
            """)

            cur.execute(f"""DELETE FROM options;
            """)

            cur.execute(f"""INSERT INTO options (token, secretToken, language) VALUES (?, ?, ?);
                """, (token, secretToken, language))

            con.commit()