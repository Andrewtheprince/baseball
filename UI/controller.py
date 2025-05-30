import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def fillDDAnno(self):
        anni = self._model.getAnni()
        for anno in anni:
            self._view._ddAnno.options.append(ft.dropdown.Option(anno))


    def squadreAnno(self, e):
        anno = self._view._ddAnno.value
        squadre = self._model.getSquadre(anno)
        self._view._txtOutSquadre.controls.clear()
        self._view._txtOutSquadre.controls.append(ft.Text(f"Squadre presenti nell'anno {anno}: {len(squadre)}"))
        for squadra in squadre:
            self._view._txtOutSquadre.controls.append(ft.Text(squadra))
        self._view._btnCreaGrafo.disabled = False
        self._view.update_page()

    def handleCreaGrafo(self, e):
        self._model.buildGraph(int(self._view._ddAnno.value))
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Grafo creato con {self._model.getNumNodi()} vertici e {self._model.getNumArchi()} archi."))
        nodi = self._model.getNodi()
        for nodo in nodi:
            self._view._ddSquadra.options.append(ft.dropdown.Option(key = str(nodo), data = nodo, on_click=self.choiceSquadra))
        self._view.update_page()

    def choiceSquadra(self, e):
        self._squadraScelta = e.control.data
        self._view._btnDettagli.disabled = False
        self._view._btnPercorso.disabled = False
        self._view.update_page()

    def handleDettagli(self, e):
        adiacenti = self._model.getAdiacenti(self._squadraScelta)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Adiacenti per la squadra {self._squadraScelta}"))
        for stringa in adiacenti:
            self._view._txt_result.controls.append(ft.Text(stringa))
        self._view.update_page()

    def handlePercorso(self, e):
        self._view._txt_result.controls.clear()
        path, score = self._model.getBestPath(self._squadraScelta)
        self._view._txt_result.controls.append(ft.Text(f"Trovato un cammino che parte da {self._squadraScelta} con score uguale a {score}"))
        for v in path:
            self._view._txt_result.controls.append(ft.Text(v))
        self._view.update_page()