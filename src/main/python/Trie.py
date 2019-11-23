from typing import Tuple
from Course import *

class TrieNode(object):
   """ Nodo de árvore TRIE. """
   def __init__(self, char: str, data):
      self.char = char
      self.children = []
      # Indica se é uma palavra completa
      self.word = False
      # Quantas palavras passaram por esse caractere
      self.counter = 0
      self.data = data
    

def add_node(root: TrieNode, item: Course):
   """ Adiciona uma palavra na árvore. """
   node = root
   # incrementa o contador da raiz pra saber quantos elementos tem
   node.counter += 1
   nome = item.nome

   # pra cada caractere na palavra
   for char in nome:
      found_in_child = False

      # busca nas childs do nodo atual
      for child in node.children:
         # se alguma tem esse caractere
         if child.char == char:
            # incrementa o contador de palavras
            child.counter += 1

            # e recomeça buscando a partir da child
            node = child
            found_in_child = True
            break

      # se não encontrou em nenhuma child, cria uma nova
      if not found_in_child:
         new_node = TrieNode(char, None)
         node.children.append(new_node)
         
         # e começa a partir dela
         node = new_node

   # define como palavra completa no último caractere.
   node.word = True
   node.data = item.codCurso


def find_prefix(root: TrieNode, prefix: str):
   """ Busca um prefixo na árvore. """
   """ Retorna uma tupla [Bool se encontrou, qtd. nodos com esse prefixo] """
   node = root

   # Se a raíz não tem filhos, a árvore é vazia
   if not root.children:
      return False, 0

   # se não, busca cada caractere do prefixo   
   for char in prefix:
      char_not_found = True

      # busca nas childs do nodo atual
      for child in node.children:
         if child.char == char:
            # se encontrar, atualiza a flag
            char_not_found = False
            # e recomeça do nodo que encontrou
            node = child
            break

      # se não encontrou algum caractere
      if char_not_found:
         return False, 0

   # se não, se encontrou todos, retorna
   return True, node.counter

def get_all(root: TrieNode, prefix: str):
   """ Busca todos os nodos com determinado prefixo """
   """ Retorna uma lista IDs de cursos com o prefixo """
   node = root
   found = []
   prefix = prefix.upper()

   # Se a raíz não tem filhos, a árvore é vazia
   if not root.children:
      return found

   # se não, busca cada caractere do prefixo   
   for char in prefix:
      char_not_found = True

      # se o usuário colocar um asterisco, sinaliza qualquer palavra com o prefixo
      if char == '*': 
         break
      else:
         # busca nas childs do nodo atual
         for child in node.children:
            if child.char == char:
               # se encontrar, atualiza a flag
               char_not_found = False
               # e recomeça do nodo que encontrou
               node = child
               break

      # se não encontrou algum caractere
      if char_not_found:
         return found

   # se encontrou todas as letras ou um *, pega todas as palavras
   return find_words(node)

def find_words(root: TrieNode):
   """ Busca todas as palavras abaixo de um nodo utilizando DFS"""
   found = []

   if root.word:
      found.append(root.data)

   for child in root.children:
      for el in find_words(child):                
         found.append(el)

   return found