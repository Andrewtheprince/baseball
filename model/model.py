import copy
import warnings
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMapSquadre = {}
        self._squadre = []
        self._idMapSalari = {}
        self._bestPath = []
        self._bestScore = 0

    def getBestPath(self, start):
        self._bestPath = []
        self._bestScore = 0
        parziale = [start]
        vicini = self._graph.neighbors(start)
        for v in vicini:
            parziale.append(v)
            self._ricorsione(parziale)
            parziale.pop()
        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale):
        if self.score(parziale) > self._bestScore:
            self._bestScore = self.score(parziale)
            self._bestPath = copy.deepcopy(parziale)
        for v in self._graph.neighbors(parziale[-1]):
            if v not in parziale and self._graph[parziale[-2]][parziale[-1]]["weight"] > self._graph[parziale[-1]][v]["weight"]:
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()

    def score(self, listOfNodes):
        if len(listOfNodes) < 2:
            warnings.warn("Errore in score, attesa lista lunga almeno 2")
        totPeso = 0
        for i in range(len(listOfNodes) - 1):
            totPeso += self._graph[listOfNodes[i]][listOfNodes[i+1]]["weight"]
        return totPeso

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
            self._idMapSalari[salario["teamID"]] = salario["totale"]
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

    def getAdiacenti(self, nodo):
        result = []
        archi_ordinati = sorted(self._graph.edges(nodo, data = True), key = lambda x: x[2].get("weight", 0), reverse=True)
        for u,v, data in archi_ordinati:
            peso = data["weight"]
            lunghezza_iniziale = 70-len(str(peso))
            testo_formattato = str(v)[:lunghezza_iniziale].ljust(lunghezza_iniziale)
            stringa_finale = testo_formattato + str(peso)
            result.append(f"{stringa_finale}")
        return result

    def getVicini(self, nodo):
        vicini = nx.neighbors(self._graph, nodo)
        viciniTuple = []
        for v in vicini:
            viciniTuple.append((v, self._graph[nodo][v]["weight"]))
        viciniTuple.sort(key=lambda x: x[1], reverse = True)
        return viciniTuple