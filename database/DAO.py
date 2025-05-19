from database.DB_connect import DBConnect
from model.squadra import Squadra

class DAO:

    @staticmethod
    def getAnni():
        conn = DBConnect.get_connection()
        cursor = conn.cursor()
        result = []
        query = """ SELECT t.year
                    FROM teams t
                    WHERE t.year >= 1980
                    group by t.year
                    order by t.year"""
        cursor.execute(query)
        for row in cursor:
            result.append(row[0])
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getSquadre(anno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary = True)
        result = []
        query = """ SELECT *
                    FROM teams t
                    WHERE t.year = %s"""
        cursor.execute(query, (anno,))
        for row in cursor:
            result.append(Squadra(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSalari(anno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """ select s.teamID, sum(s.salary) as totale
                    from salaries s
                    where s.year = %s
                    group by s.teamID 
                    order by totale"""
        cursor.execute(query, (anno,))
        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return result