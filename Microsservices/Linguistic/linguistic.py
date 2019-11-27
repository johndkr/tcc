#linguistic
# -*- coding: utf-8 -*-
import os, sys
sys.path.append('..\\..\\')

import string
import json

import spacy
import re
import unicodedata

from spellchecker import SpellChecker
from collections import Counter 
from pyUFbr.baseuf import ufbr

import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

from Microsservices.CommonUtil.Log import log_util

KNOWN_WORDS = ".\\data\\known_words.txt"

## consult this before defining which word split will be used: https://machinelearningmastery.com/clean-text-machine-learning-python/

class LinguisticAnalyses():
  log_manager = log_util.Log_Util(False)
  nlp = spacy.load('pt_core_news_sm')

  def __init__(self):
    self.spellchecker = SpellChecker(language='pt')
    self.__load_known_words()
  
  def __ponctuation_remover(self, txt):
    ### this method removes all accents from a string
    # return unicodedata.normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
    text_cleanned = txt.replace('\t','').replace('\r\n', ' ').replace('  ', ' ')
    text_cleanned = text_cleanned.replace(u"\u201C", '').replace(u"\u201D",'').replace('"','').replace(u"\u2018",'').replace(u"\u2019",'').replace('…','')

    return text_cleanned.translate(str.maketrans('', '', string.punctuation))

  def __remove_them_all(self, txt):
    # This method returns a string only containg numbers, letters and space
    text_cleanned = txt.replace('  ', ' ').replace('\t','').replace('\r\n\r\n', ' ')
    nfkd = unicodedata.normalize('NFKD', text_cleanned)
    palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    return re.sub('[^a-zA-Z0-9 \\\]', '', palavraSemAcento)

  def __load_known_words(self):
    known_words = []
    siglas_partidarias = ['MDB', 'PT', 'PSDB', 'PP', 'PDT', 'PTB', 'DEM', 'PL', 'PSB', 'PSC', 'PCdoB', 'PV', 'PSD',
                          'PSL', 'PMN', 'PTC', 'DC', 'PODE', 'Avante', 'Solidariedade', 'PSOL', 'PRTB', 'PROS', 'Patriota'
                          'PMB', 'NOVO', 'REDE', 'PSTU', 'PCB', 'PCO', 'PMDB']
    try:
      path = os.path.join(os.path.dirname(os.path.abspath(__file__)), KNOWN_WORDS)
      known_words = open(path, encoding='utf-8').read().split()
      self.log_manager.info('Found file for known words at: ' + path)
    except Exception as err:
      self.log_manager.exception(err)
      known_words = []
    finally:
      
      known_words += ufbr.list_uf #learn BR UFs
      known_words += siglas_partidarias
      known_words += [partido + regiao for partido in siglas_partidarias for regiao in ufbr.list_uf] # learn partido regiao PT-SP = PTSP after removing ponctuation
      
      for uf in ufbr.list_uf: #Learn BR cities with name titled and without "-"
        known_words += [self.__ponctuation_remover(city.title()) for city in ufbr.list_cidades(uf)]

      self.spellchecker.word_frequency.load_words(known_words)

  def __kill_gremlins(self, text):
    cp1252 = {
      # from http://www.microsoft.com/typography/unicode/1252.htm
      u"\x80": u"\u20AC", # EURO SIGN
      u"\x82": u"\u201A", # SINGLE LOW-9 QUOTATION MARK
      u"\x83": u"\u0192", # LATIN SMALL LETTER F WITH HOOK
      u"\x84": u"\u201E", # DOUBLE LOW-9 QUOTATION MARK
      u"\x85": u"\u2026", # HORIZONTAL ELLIPSIS
      u"\x86": u"\u2020", # DAGGER
      u"\x87": u"\u2021", # DOUBLE DAGGER
      u"\x88": u"\u02C6", # MODIFIER LETTER CIRCUMFLEX ACCENT
      u"\x89": u"\u2030", # PER MILLE SIGN
      u"\x8A": u"\u0160", # LATIN CAPITAL LETTER S WITH CARON
      u"\x8B": u"\u2039", # SINGLE LEFT-POINTING ANGLE QUOTATION MARK
      u"\x8C": u"\u0152", # LATIN CAPITAL LIGATURE OE
      u"\x8E": u"\u017D", # LATIN CAPITAL LETTER Z WITH CARON
      u"\x91": u"\u2018", # LEFT SINGLE QUOTATION MARK
      u"\x92": u"\u2019", # RIGHT SINGLE QUOTATION MARK
      u"\x93": u"\u201C", # LEFT DOUBLE QUOTATION MARK
      u"\x94": u"\u201D", # RIGHT DOUBLE QUOTATION MARK
      u"\x95": u"\u2022", # BULLET
      u"\x96": u"\u2013", # EN DASH
      u"\x97": u"\u2014", # EM DASH
      u"\x98": u"\u02DC", # SMALL TILDE
      u"\x99": u"\u2122", # TRADE MARK SIGN
      u"\x9A": u"\u0161", # LATIN SMALL LETTER S WITH CARON
      u"\x9B": u"\u203A", # SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
      u"\x9C": u"\u0153", # LATIN SMALL LIGATURE OE
      u"\x9E": u"\u017E", # LATIN SMALL LETTER Z WITH CARON
      u"\x9F": u"\u0178", # LATIN CAPITAL LETTER Y WITH DIAERESIS
    }
    # map cp1252 gremlins to real unicode characters
    if re.search(u"[\x80-\x9f]", text):
      def fixup(m):
        s = m.group(0)
        return cp1252.get(s, s)
      
      if isinstance(text, str):
        # make sure we have a unicode string
        text = text
        text = re.sub(u"[\x80-\x9f]", fixup, text)
    return text

  def wrong_proportion(self, text):
    text_cleanned = self.__ponctuation_remover(text)
    #removing double and single quotes
    split_it = text_cleanned.split()
    return len(self.spellchecker.unknown(split_it))/(len(split_it))
  
  def get_wrong_words(self, text):
    text_cleanned = self.__ponctuation_remover(text)

    split_it = text_cleanned.split()
    return self.spellchecker.unknown(split_it)

  def get_words_types(self, txt):
    self.log_manager.debbug("Getting words types...")
    
    doc = self.nlp(txt)
    return [(token.orth_, token.pos_) for token in doc]

  def count_words_types(self, txt):
    # this method reveices a text and returns all its words types counted in touples
    # IT IS SENSITIVE to grammar mistakes in portuguese.
    self.log_manager.info("Counting words types")
    types_count = {}
    types_tag_tuples = self.get_words_types(txt)

    for tutuple in types_tag_tuples:
      if tutuple[1] not in types_count:
        types_count[tutuple[1]] = 1
      else:
        types_count[tutuple[1]] += 1

    return types_count

  def count_interjeicao(self, txt):
    interjeicao_list = ['Cuidado!', 'Olhe!', 'Atenção!', 'Fogo!', 'Olha lá!', 'Alto lá!', 'Calma!', 'Devagar!', 'Sentido!', 'Alerta!', 'Vê bem!', 
                        'Volta aqui!', 'Fora!', 'Toca!', 'Xô!', 'Xô pra lá!', 'Passa!', 'Sai!', 'Roda!', 'Arreda!', 'Rua!', 'Cai fora!', 'Vaza!', 
                        'Graças a Deus!', 'Obrigado!', 'Agradecido!', 'Muito obrigada!', 'Valeu!', 'Valeu a pena!', 'Ah!', 'Ah,' 'Eh!', 'Oh!', 'Oba!', 
                        'Eba!', 'Viva!', 'Olá!', 'Olé!', 'Eta!', 'Eita!', 'Eia!', 'Uhu!', 'Que bom!', 'Ufa!', 'Uf!', 'Arre!', 'Puxa!', 'Ainda bem!', 
                        'Nossa senhora!', 'Coragem!', 'Força!', 'Ânimo!', 'Avante!', 'Vamos!', 'Firme!', 'Inteirinho!', 'Bora!', 'Socorro!', 'Ei!', 
                        'Ô!', 'Alô!', 'Psiu!', 'Psit!', 'Misericórdia!', 'Muito bem!', 'Bem!', 'Bravo!', 'Bis!', 'É isso aí!', 'Isso!', 'Parabéns!', 
                        'Boa!', 'Apoiado!', 'Ótimo!', 'Fiufiu!', 'Hup!', 'Hurra!', 'Hei!', 'Oi!', 'Ó!', 'Claro!', 'Certo!', 'Sem dúvida!', 'Então!', 
                        'Sim!', 'Pois não!', 'Tá!', 'Hã-hã!', 'Droga!', 'Porcaria!', 'Credo!', 'Perdão!', 'Opa!', 'Desculpa!', 'Desculpe!', 'Foi mal!', 
                        'Oxalá!', 'Tomara!', 'Quisera!', 'Queira', 'Deus!', 'Quem me dera!', 'Adeus!', 'Até logo!', 'Tchau!', 'Até amanhã!', 'Ai!', 
                        'Ui!', 'Meu', 'Ai de mim!', 'Hum?', 'Hem?', 'Hã?', 'Ué!', 'Epa!', 'Quê!', 'Nossa!', 'Nossa mãe!', 'Virgem!', 'Caramba!', 'Xi!',
                        'Meu Deus!', 'Senhor Jesus!', 'Crê em Deus pai!', 'Adiante!', 'Upa!', 'Vai nessa!', 'Cruzes!', 'Uh!', 'Barbaridade!',
                        'Francamente!', 'Que medo!', 'Jesus!', 'Jesus', 'Maria e José!', 'Bom!', 'Salve!', 'Ave!', 'Shh!', 'Silêncio!', 'Basta!',
                        'Chega!', 'Calado!', 'Quieto!', 'Bico fechado!']

    interjeicao_list_lower = [w.lower() for w in interjeicao_list]
    text_clean = [word.lower() for word in self.__ponctuation_remover(txt).split()]

    return sum(1 for word in text_clean if word in interjeicao_list_lower)

  def get_defined_word_types(self, txt):
    word_types = self.get_words_types(txt)

    result_json = {
      "verbos": sum('VERB' in type_tuple for type_tuple in word_types),
      "substantivos": sum('NOUN' in type_tuple for type_tuple in word_types) + sum('PROPN' in type_tuple for type_tuple in word_types),
      "adverbios": sum('ADV' in type_tuple for type_tuple in word_types),
      "pronomes": sum('PRON' in type_tuple for type_tuple in word_types),
      "artigos": sum('DET' in type_tuple for type_tuple in word_types),
      "adjetivo": sum('ADJ' in type_tuple for type_tuple in word_types),
      "numerais": sum('NUM' in type_tuple for type_tuple in word_types),
      "preposicoes": sum('ADP' in type_tuple for type_tuple in word_types),
      "conjuncoes": sum('CCONJ' in type_tuple for type_tuple in word_types) + sum ('SCONJ' in type_tuple for type_tuple in word_types),
      "pontuacao": sum('PUNCT' in type_tuple for type_tuple in word_types),
      "interjeicoes": self.count_interjeicao(txt),
      "verbos_modais": self.count_modal_verbs(txt)
    }

    return result_json
 
  def count_words(self, txt):
    txt_sem_pontuacao = self.__remove_them_all(txt)
    return len(txt_sem_pontuacao.split())

  def get_entities(self, txt):
    # this method gets all entities within a given text.
    # IT IS SENSITIVE to grammar mistakes
    #self.log_manager.debbug("Getting text entities...")

    doc = self.nlp(txt)
    return doc.ents

  def get_all_entities_vector(self, txt):
    # this method receives a text and counts its entities
    # IT IS SENSITIVE to grammar mistakes on the text

    #self.log_manager.debbug("Counting entities mentioned on text")

    entities = self.get_entities(txt)
    entities = list(dict.fromkeys([str(ent) for ent in entities]))

    entities_type = [(entitie, txt.upper().count(str(entitie).upper())) for entitie in entities]

    return entities_type

  def count_entities(self, txt):
    # this method gets all entities within a given text.
    # IT IS SENSITIVE to grammar mistakes
    self.log_manager.debbug("Counting text entities...")
    return len(self.nlp(txt).ents)

  def count_upper_case_words(self, txt):
    clean_text = self.__remove_them_all(txt)
    return sum(map(str.isupper, clean_text.split()))

  def count_pronome_pessoal_eu_tu_voce(self, txt):
    clean_text = self.__remove_them_all(txt)

    count_pronomes = 0
    count_pronomes += clean_text.lower().split().count("eu")
    count_pronomes += clean_text.lower().split().count("tu")
    count_pronomes += clean_text.lower().split().count("voce")

    return count_pronomes

  def count_pronome_pessoal_nos(self, txt):
    clean_text = self.__remove_them_all(txt)

    count_pronomes = 0
    count_pronomes += clean_text.lower().split().count("nos")

    return count_pronomes

  def count_pronome_pessoal_elxs(self, txt):
    clean_text = self.__remove_them_all(txt)

    count_pronomes = 0
    count_pronomes += clean_text.lower().split().count("ele")
    count_pronomes += clean_text.lower().split().count("eles")
    count_pronomes += clean_text.lower().split().count("ela")
    count_pronomes += clean_text.lower().split().count("elas")

    return count_pronomes

  def count_modal_verbs(self, txt):
    doc = self.nlp(txt)
    verbs = [token.lemma_ for token in doc if token.pos_ == 'VERB']
    result = verbs.count('dever') + verbs.count('ter') + verbs.count('poder')

    return result

  def count_caracteres(self, txt):
    return len(txt)

  def count_sentence_average_size(self, txt):
    sentences_set = sent_tokenize(txt)
    return sum(len(sentence.split()) for sentence in sentences_set) / len(sentences_set)

  def count_word_average_size(self, txt):
    clean_text = self.__remove_them_all(txt)
    words = clean_text.split()
    return sum(len(word) for word in words) / len(words)
  
  def make_linguistic_analyses(self, txt):
    """ this method run all analysis for this module and return them within a json """

    txt = self.__kill_gremlins(txt)

    word_types = self.get_defined_word_types(txt)

    other_tags = {
      "n_palvaras": self.count_words(txt),
      "prop_palavras_erradas": self.wrong_proportion(txt),
      "n_camel_case": self.count_entities(txt),
      "n_upper_case": self.count_upper_case_words(txt),
      "n_pronome_1": self.count_pronome_pessoal_eu_tu_voce(txt),
      "n_pronome_1_plural": self.count_pronome_pessoal_nos(txt),
      "n_pronome_2": self.count_pronome_pessoal_elxs(txt),
      "n_characteres": self.count_caracteres(txt),
      "avg_sentence": self.count_sentence_average_size(txt),
      "avg_word_length": self.count_word_average_size(txt)
    }

    result = dict(word_types.items(), **other_tags)

    return result

if __name__ == "__main__":
    txt = open('E:\\Documentos Local\\GitHub\\tcc\\Microsservices\\MainProgram\\db\\fake\\' + str(2) + '.txt', encoding='utf-8').read()
    print(txt)

    analisator = LinguisticAnalyses()
    print(analisator.make_linguistic_analyses(txt))
