class Course():
    """ Class que define um curso. """
    def __init__(self, codCurso, nome):
        self.codCurso = codCurso
        self.nome = nome
        self.vinculados = {}
        self.matriculados = {}
        self.ingressantes = {}
        self.diplomados = {}
        self.evadidos = {}

    def addData(self, period, vinculados=0, matriculados=0, ingressantes=0, diplomados=0, evadidos=0):        
        """ Adiciona propriedades a uma instância de curso. """
        if vinculados > 0:
            self.vinculados[period] = vinculados
        if matriculados > 0:
            self.matriculados[period] = matriculados
        if ingressantes > 0:
            self.ingressantes[period] = ingressantes
        if diplomados > 0:
            self.diplomados[period] = diplomados
        if evadidos > 0:
            self.evadidos[period] = evadidos