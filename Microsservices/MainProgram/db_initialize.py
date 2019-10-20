import pandas as pd
import os
import sys

headline = ['fake_or_true','author','link','category','publication_date','nr_tokens','nr_words_wo_ponctuation','nr_types','nr_links','nr_upper','nr_verbs','nr_sub_and_imperative','nr_nouns','nr_adjectives','nr_adverbs','nr_modal_verbs','nr_sing_first_second_personal_pronoums','nr_plural_first_personal_pronoums','nr_pronoums','pausality','nr_characters','avg_sentence_length','avg_word_length','percentage_w_spelling_errors','emotiveness','diversity']
dataset_fake = []
dataset_true = []

#Fake meta database
for number in range(1,3602,1):
	try:
		fp = open(str(os.getcwd()) + '\\db\\meta_fake\\' + str(number) + '-meta.txt')
		arq = fp.readlines()
		one_set = [line.replace('\n','') for line in arq]
		one_set.insert(0,'Fake')
		dataset_fake.append(one_set)
	except:
		print(str(number) + ' not found')

#True meta database
for number in range(1,3602,1):
	try:
		fp = open(str(os.getcwd()) + '\\db\\meta_true\\' + str(number) + '-meta.txt')
		arq = fp.readlines()
		one_set = [line.replace('\n','') for line in arq]
		one_set.insert(0,'True')
		dataset_true.append(one_set)
	except:
		print(str(number) + ' not found')

#Exporta base
df_fake = pd.DataFrame(dataset_fake,columns = headline)
df_true = pd.DataFrame(dataset_true,columns = headline)
df = pd.concat([df_fake,df_true])
df.to_excel(str(os.getcwd()) + '\\db\\database.xls')