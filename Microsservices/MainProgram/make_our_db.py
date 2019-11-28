# set our database using our classifier
import os, sys
import string
import json
import csv
import re

sys.path.append('..\\..\\')

from Microsservices.Linguistic import linguistic
from Microsservices.Message import message
from Microsservices.NewsOrigin import source

def kill_gremlins(text):
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

def get_files():
    path_fake = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".\\db\\fake\\")
    fake_files = [os.path.join(path_fake, f) for f in os.listdir(path_fake)]

    path_true = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".\\db\\true\\")
    true_files = [os.path.join(path_true, f) for f in os.listdir(path_true)]

    result = fake_files + true_files

    return result

def get_analysis():
    ling_analysator = linguistic.LinguisticAnalyses()
    mes_analysator = message.MessageAnalyses()
    source_analysator = source.SourceAnalyses()

    files = get_files()
    result = []

    chunk_size = 500
    control = 500

    while control < (len(files) + 1):
        counter = 0
        for f in files[control:control+chunk_size-1]:
            txt = kill_gremlins(open(f, 'r', encoding='utf-8', newline='').read())

            ling = ling_analysator.make_linguistic_analyses(txt)
            
            res1 = {
                'file_name': str(f),
                'index': os.path.basename(f).split('.')[0],
                'fake_or_true': 'Fake' if 'fake' in f.split('\\') else 'True',
                # 'feeling': mes_analysator.get_txt_feeling(txt),
                'feeling': -1,
                'nr_links': source_analysator.count_links(txt),
                'nr_locations': mes_analysator.count_location_mentions(txt)
            }
            result.append(dict(res1.items(), **ling))
            counter += 1
            print("{0:.2f}% Completed".format(100*counter/len(files[control:control+chunk_size-1])))

        print("A analise terminou, com {} resultados para chunk {}-{}".format(len(result), control, control+chunk_size-1))
        print("\nA meta é atingir {} arquivos".format(len(files)))
        create_csv_file(result, control, control+chunk_size-1)
        control = control+chunk_size

def get_wrong_words_list():
    ling_analysator = linguistic.LinguisticAnalyses()
    files = get_files()
    result = []
    counter = 0
    sum_words = 0

    for f in files:
        txt = open(f, 'r', encoding='utf-8', newline='').read()
        txt = kill_gremlins(txt)

        wrong_words = ling_analysator.get_wrong_words(txt)
        result.append(wrong_words)
        sum_words += len(wrong_words)

        counter += 1
        print("{0:.2f}% Completed".format(100*counter/len(files)))

    print("Lista de palavras erradas pegas com sucesso! {} conjuntos encontrados\nCom {} palavras erradas".format(len(result), sum_words))

    with open("wrong_words_found.csv","w",newline='',encoding='utf-8') as f:
        print("Escrevendo resultado num csv..\n")
        wr = csv.writer(f)
        wr.writerows(result)

    print("Prontinho :)\n")

def create_csv_file(list_of_analysis, inicio, fim):
    print("Colocando resultados em CSV...\n")
    with open("our_db_chunk_{}-{}.csv".format(str(inicio), str(fim)),"w",newline="") as f:
        header = list_of_analysis[0].keys()
        cw = csv.DictWriter(f,header,delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        cw.writeheader()
        cw.writerows(list_of_analysis)
    print("Prontinho :)\n")

if __name__ == "__main__":
    get_analysis()
    # get_wrong_words_list()
