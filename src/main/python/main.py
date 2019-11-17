from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QComboBox, QRadioButton, QLabel, QAction, QFormLayout, QHBoxLayout, QVBoxLayout, QTableWidget, QTableView, QTableWidgetItem, QPushButton, QLineEdit
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QPalette
from Course import *
from Period import *
from Trie import *

import numpy as np
import pickle
import sys

class NumericTableWidgetItem(QTableWidgetItem):
    def __init__(self, number):
        QTableWidgetItem.__init__(self, number, QTableWidgetItem.UserType)
        self.__number = number

    def __lt__(self, other):
        return int(self.__number) < int(other.__number)

class mainGUI(QWidget):
    def __init__(self, root, courses, periods):
        super().__init__()
        self.title = 'Course Viewer'
        self.left = 50
        self.top = 50
        self.width = 1280
        self.height = 720
        self.root = root
        self.courses = courses
        self.periods = periods
        self.filtered = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.vbLayout = QVBoxLayout()
        self.createSearchBar()
        self.createView()

        # Define o layout da tela
        self.setLayout(self.vbLayout)

        # e mostra a janela
        self.show()

    def createTable(self):
        """ Cria a tabela com as colunas """
        self.tbData = QTableWidget()
        self.tbData.setColumnCount(9)
        self.tbData.verticalHeader().hide()
        self.tbData.setSelectionBehavior(QTableView.SelectRows)
        # CodCurso;NomeCurso;Ano;Periodo;Vinculados;Matriculados;Ingressantes;Diplomados;Evadidos
        colNames = ["Cód", "Nome", "Vinculados", "Matriculados", "Ingressantes", "Diplomados", "Evadidos", "Ano", "Semestre"]
        colWidths = [20, 250, 80, 80, 80, 80, 80, 20, 80]
        for width, id in zip(colWidths, range(len(colWidths))):
            self.tbData.setColumnWidth(id,width)

        self.tbData.setHorizontalHeaderLabels(colNames) 
        self.tbData.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tbData.setAlternatingRowColors(True)        

        self.tbData.setMaximumWidth(900)

        # coloca na tela
        self.hbView.addWidget(self.tbData)

    def createSearchBar(self):
        """ Cria o hbox superior da tela """
        self.hbSearch = QHBoxLayout()
        self.txtBox = QLineEdit(self)
        self.btnSearch = QPushButton('Pesquisar', self)
        self.btnSearch.clicked.connect(self.on_search)

        self.hbSearch.addWidget(QLabel('Procure um curso: '))
        self.hbSearch.addWidget(self.txtBox)
        self.hbSearch.addWidget(self.btnSearch)
        
        # coloca na tela
        self.vbLayout.addLayout(self.hbSearch)

    def createView(self):
        self.hbView = QHBoxLayout()
        # coloca a barra lateral
        self.vbOptions = QVBoxLayout()
        self.vbOptions.setSpacing(False)
        # coloca a tabela
        self.createTable()

        # inclui a área de ordenar
        vbTemp = QVBoxLayout()        
        hbTemp0 = QHBoxLayout()
        hbTemp = QHBoxLayout()

        # inclui o seletor de ano
        hbTemp1 = QHBoxLayout()
        hbTemp2 = QHBoxLayout()

        self.cbOrder = QComboBox(self)
        self.cbOrder.setEditable(False)        
        self.cbOrder.setAutoFillBackground(True)
        self.cbOrder.addItems(['Nome','Vinculados', 'Matriculados', 'Ingressantes', 'Diplomados', 'Evadidos'])
        self.cbOrder.currentIndexChanged.connect(self.on_order)
        
        self.cbOrderDir = QComboBox(self)
        self.cbOrderDir.setEditable(False)        
        self.cbOrderDir.setAutoFillBackground(True)
        self.cbOrderDir.addItems(['Asc', 'Desc'])
        self.cbOrderDir.move(0, 50)
        self.cbOrderDir.currentIndexChanged.connect(self.on_order)

        self.cbAno = QComboBox(self)
        self.cbAno.setEditable(False)        
        self.cbAno.setAutoFillBackground(True)
        self.cbAno.currentIndexChanged.connect(self.on_update_year)

        self.cbAnoTo = QComboBox(self)
        self.cbAnoTo.setEditable(False)        
        self.cbAnoTo.setAutoFillBackground(True)

        lbOrder = QLabel('Ordenar por', self)
        lbOrder.move(0, 0)
        lbOrder.setMaximumHeight(60)
        lbOrder.setMaximumWidth(60)

        lbTempAno = QLabel('De', self)
        lbTempAno.move(0, 0)
        lbTempAno.setMaximumHeight(10)
        lbTempAno.setMaximumWidth(30)

        lbTempAno2 = QLabel('Até', self)
        lbTempAno2.move(0, 0)
        lbTempAno2.setMaximumHeight(10)
        lbTempAno2.setMaximumWidth(30)

        # coloca as caixas no lugar
        hbTemp0.addWidget(lbOrder)
        hbTemp0.addWidget(self.cbOrder)
        hbTemp.addWidget(self.cbOrderDir)
        
        vbTemp.addLayout(hbTemp0)
        vbTemp.addLayout(hbTemp)
        vbTemp.addWidget(self.cbOrderDir)
        
        hbTemp1.addWidget(lbTempAno)
        hbTemp1.addWidget(self.cbAno)
        
        hbTemp2.addWidget(lbTempAno2)
        hbTemp2.addWidget(self.cbAnoTo)
        #self.vbOptions.addLayout(hbTemp0)
        self.vbOptions.addLayout(vbTemp)
        self.vbOptions.addLayout(hbTemp1)
        self.vbOptions.addLayout(hbTemp2)

        # inclui o seletor de semestre
        hbTemp2 = QHBoxLayout()
        self.rbSemestreAll = QRadioButton('Ambos semestres', self)
        self.rbSemestre1 = QRadioButton('Semestre 1', self)
        self.rbSemestre2 = QRadioButton('Semestre 2', self)
        self.rbSemestreAll.setChecked(True)
        hbTemp2.addWidget(self.rbSemestreAll)
        hbTemp2.addWidget(self.rbSemestre1)
        hbTemp2.addWidget(self.rbSemestre2)
        self.vbOptions.addLayout(hbTemp2)

        # inclui botão de filtrar
        self.btnFilter = QPushButton('Filtrar', self)
        self.btnFilter.setMinimumHeight(40)
        self.btnFilter.clicked.connect(self.on_filter)
        self.vbOptions.addWidget(self.btnFilter)

        # inclui botão de plotar
        self.btnPlot = QPushButton('Plotar selecionados', self)
        self.btnPlot.setMinimumHeight(40)
        self.btnPlot.setDisabled(True)
        self.btnPlot.clicked.connect(self.on_plot)
        self.vbOptions.addWidget(self.btnPlot)

        self.hbView.addLayout(self.vbOptions)
        self.vbLayout.addLayout(self.hbView)

    def clearTable(self):
        """ Limpa a tabela """
        for i in reversed(range(self.tbData.rowCount())):
            self.tbData.removeRow(i)

    def makePeriods(self, dateFrom, dateTo, semestre):
        """ Cria um intervalo de períodos válidos """
        f, t = int(dateFrom), int(dateTo)
        valid = []
        while f <= t:
            # se forem ambos os semestres
            if ( semestre == '0' ):
                valid.append( str(f) + '/1' )
                valid.append( str(f) + '/2' )
            else:
                valid.append( str(f) + '/' + semestre )

            f += 1

        return valid
        
    def updateSearch(self, courses):
        """ Atualiza a tabela com a lista de cursos fornecida """
        self.btnPlot.setDisabled(True)
        self.clearTable()

        # e inclui os resultados da busca
        self.tbData.setRowCount(len(courses))
        for x, course in zip(range(len(courses)), courses):
            properties = course.__dict__.values()
            for y, prop in zip(range(len(properties)), properties):
                # trata diferente os dicts
                if ( isinstance(prop, dict) ):
                    vals = np.array(list(prop.values()))
                    #self.tbData.setItem(x, y, QTableWidgetItem(str(np.sum(vals))))
                    self.tbData.setItem(x, y, NumericTableWidgetItem(str(np.sum(vals))))
                    self.tbData.setItem(x, 7, QTableWidgetItem('-'))
                    self.tbData.setItem(x, 8, QTableWidgetItem('-'))
                else:
                    self.tbData.setItem(x, y, QTableWidgetItem(str(prop)))
        
        self.on_order()

    @pyqtSlot()
    def on_update_year(self):
        self.cbAnoTo.clear()

        for date in periods:
            ano, semestre = date.split('/')
            if ( semestre == '1' and ano >= self.cbAno.currentText() ):
                self.cbAnoTo.addItem(ano)

    @pyqtSlot()
    def on_search(self):
        prefix = self.txtBox.text()

        if ( prefix == "" ):
            # busca todos
            self.updateSearch(list(self.courses.values()))
            self.filtered = []
        else:
            prefix = prefix.upper()
            self.filtered = get_all(self.root, prefix)
            found = [self.courses[id] for id in self.filtered]
            self.updateSearch(found)

    @pyqtSlot()
    def on_filter(self):
        self.btnPlot.setDisabled(False)
        self.clearTable()        
        dateFrom = self.cbAno.currentText()        
        dateTo = self.cbAnoTo.currentText()
        semestre = '0' if self.rbSemestreAll.isChecked() else ('1' if self.rbSemestre1.isChecked() else '2')
        validPeriods = self.makePeriods(dateFrom, dateTo, semestre)

        qtdCourses = len(self.courses) if len(self.filtered) == 0 else len(self.filtered)
        qtdPeriods = len(validPeriods)
        rowCount = qtdCourses * qtdPeriods
        self.tbData.setRowCount( rowCount )

        # filtra os dados dos períodos específicos
        x = 0
        for period in validPeriods:
            data = self.periods[period]
            # pra cada código de curso
            for cod in data.ingressantes.keys():
                # se já tem dados filtrados, busca só os cod definidos
                if ( len(self.filtered) > 0 and cod not in self.filtered ):
                    continue

                # cod, nome, vinc, mat, ing, dip, eva, ano, sem
                self.tbData.setItem(x, 0, QTableWidgetItem(str(cod)))
                self.tbData.setItem(x, 1, QTableWidgetItem(self.courses[cod].nome))
                self.tbData.setItem(x, 2, NumericTableWidgetItem(str(data.vinculados[cod])))
                self.tbData.setItem(x, 3, NumericTableWidgetItem(str(data.matriculados[cod])))
                self.tbData.setItem(x, 4, NumericTableWidgetItem(str(data.ingressantes[cod])))
                self.tbData.setItem(x, 5, NumericTableWidgetItem(str(data.diplomados[cod])))
                self.tbData.setItem(x, 6, NumericTableWidgetItem(str(data.evadidos[cod])))
                self.tbData.setItem(x, 7, QTableWidgetItem(str(data.ano)))
                self.tbData.setItem(x, 8, QTableWidgetItem(str(data.period)))
                x += 1
        self.on_order()

    @pyqtSlot()
    def on_order(self):
        map = {'Nome': 1, 'Vinculados': 2, 'Matriculados': 3, 'Ingressantes': 4, 'Diplomados': 5, 'Evadidos': 6}
        dir = Qt.AscendingOrder if self.cbOrderDir.currentText() == 'Asc' else Qt.DescendingOrder
        self.tbData.sortByColumn(map[self.cbOrder.currentText()], dir)

    @pyqtSlot()
    def on_plot(self):
        ids = []
        years = []
        semestre = '0' if self.rbSemestreAll.isChecked() else ('1' if self.rbSemestre1.isChecked() else '2')
        selIndexes = self.tbData.selectedIndexes()

        min = 0
        i = 9
        max = int((len(selIndexes)))

        # busca os dados das linhas selecionadas.
        while i <= max:
            row = selIndexes[min:i]
            min += 9
            i += 9
            # vinc, mat , ing, dipl, evad, ano, semestre
            id = self.tbData.model().data(row[0])
            nome = self.tbData.model().data(row[1])
            vinc = self.tbData.model().data(row[2])
            mat = self.tbData.model().data(row[3])
            ing = self.tbData.model().data(row[4])
            dip = self.tbData.model().data(row[5])
            evad = self.tbData.model().data(row[6])
            ano = self.tbData.model().data(row[7])
            semestre = self.tbData.model().data(row[8])
            ids.append(id)
            years.append(ano)
            
        print(ids)
        print(years)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    palette = QPalette()
    palette.setColor(QPalette.Background, Qt.darkGray)
    app.setPalette(palette)

    # carrega o nodo da lista
    with open('trie.p', 'rb') as t:
        root = pickle.load(t)

    with open('periods.p', 'rb') as p:
        periods = pickle.load(p)

    with open('courses.p', 'rb') as f:
        courses = pickle.load(f)

    ex = mainGUI(root, courses, periods)

    ### Inicializa a visualização ###
    insertedPeriods = []
    # configura os anos obtidos do csv
    for date, info in periods.items():
        ano, semestre = date.split('/')

        if ano not in insertedPeriods:
            ex.cbAno.addItem(ano)
            insertedPeriods.append(ano)

    ex.tbData.setRowCount(len(courses))
    for x, course in zip(range(len(courses)), courses.values()):
        properties = course.__dict__.values()

        for y, prop in zip(range(len(properties)), properties):
            # trata os dicts diferente
            if ( isinstance(prop, dict) ):
                v = np.array(list(prop.values()))
                ex.tbData.setItem(x, y, NumericTableWidgetItem(str(np.sum(v))))
            else:
                ex.tbData.setItem(x, y, QTableWidgetItem(str(prop)))
    
    ex.tbData.sortByColumn(1, Qt.AscendingOrder)
    sys.exit(app.exec_()) 

    #window.resize(250, 150)
    #exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    #sys.exit(exit_code)