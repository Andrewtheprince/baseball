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
        self._view.update_page()

    def handleCreaGrafo(self, e):
        pass

    def handleDettagli(self, e):
        pass

    def handlePercorso(self, e):
        pass