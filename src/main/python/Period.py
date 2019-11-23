class Period():
   """ Classe representando um ano/semestre. """
   def __init__(self, ano, semestre):
      self.ano = ano
      self.period = semestre
      self.vinculados = {}
      self.matriculados = {}
      self.ingressantes = {}
      self.diplomados = {}
      self.evadidos = {}

   def addData(self, codCurso, vinculados=0, matriculados=0, ingressantes=0, diplomados=0, evadidos=0):
      """ Adiciona propriedades a uma instância de período. """
      if vinculados >= 0:
         self.vinculados[codCurso] = vinculados
      if matriculados >= 0:
         self.matriculados[codCurso] = matriculados
      if ingressantes >= 0:
         self.ingressantes[codCurso] = ingressantes
      if diplomados >= 0:
         self.diplomados[codCurso] = diplomados
      if evadidos >= 0:
         self.evadidos[codCurso] = evadidos
