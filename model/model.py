import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMapSquadre = {}
        self._squadre = []
        self._idMapSalari = {}

    @staticmethod
    def getAnni():
        return DAO.getAnni()

    def getSquadre(self, anno):
        self._graph.clear()
        self._idMapSquadre.clear()
        self._squadre.clear()
        squadre = DAO.getSquadre(anno)
        self._squadre.extend(squadre)
        for squadra in squadre:
            self._idMapSquadre[squadra.ID] = squadra
        return squadre

    def buildGraph(self, anno):
        self._graph.add_nodes_from(self._squadre)
        salari = DAO.getSalari(anno)
        for salario in salari:
            self._idMapSalari[salario["ID"]] = salario["tot"]
        for squadra in self._squadre:
            for squadra2 in self._squadre:
                if squadra != squadra2:
                    self._graph.add_edge(squadra, squadra2, weight = self._idMapSalari[squadra.ID] + self._idMapSalari[squadra2.ID])

    def getNumNodi(self):
        return len(self._graph.nodes)

    def getNumArchi(self):
        return len(self._graph.edges)

    def getNodi(self):
        return self._graph.nodes
