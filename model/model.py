from database.DAO import DAO

class Model:
    def __init__(self):
        pass

    @staticmethod
    def getAnni():
        return DAO.getAnni()

    @staticmethod
    def getSquadre(anno):
        return DAO.getSquadre(anno)