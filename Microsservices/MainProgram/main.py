import sys
sys.path.append('../../')

from Microsservices.NewsOrigin import source_checking as Source_Checking
from Microsservices.Linguistic import linguistic as Linguistic

def main():
	i = 0
	while(i is not '5'):
		print('\n')
		print(60*'#')
		print(24*'#'+' Bem-vindo '+25*'#')
		print(60*'#')
		print('\n')
		print('O que você deseja fazer? [ESCOLHA COM O NÚMERO + ENTER]')
		print('1) Checar link pelo navegador')
		print('2) Checar link pelo WhatsApp')
		print('3) Checar fonte jornalística')
		print('4) Ver estatísticas de fontes jornalísticas')
		print('5) Sair')
		print('\n')
		print(60*'#')
		print('\n')
		i = input('Escolha uma opção: ')
		print('\n')

		if (i == '1'):
			print('Navegador!')
		elif (i == '2'):
			print('WhatsApp')
		elif (i == '3'):
			switch = True
			while(switch):
				b = input('Nome do jornal: ')
				print('\n')
				jornal = Source_Checking.Source()
				jornal.get_source_id(b)
				try:
					jornal.load_source()
					switch = False
					print(40*'-')
					print(18*' ' + jornal.source_name + 18*' ')
					print(40*'-')
					print('|-> URL:            '+jornal.versions[0]["source_url"])
					print('|-> Twitter:        '+jornal.versions[0]["source_twitter_handler"])
					print('|-> Wikipedia:      '+jornal.versions[0]["source_wikipedia_page"])
					print('|-> Political bias: '+ Source_Checking.POLITICAL_BIAS[jornal.political_bias])
					print('|-> Factuality:     '+ Source_Checking.FACTUALITY[jornal.factuality])
					print(40*'-')
					print('\n')
				except:
					print('Jornal não encontrado, tente novamente')
					print('\n')

		elif (i == '4'):
			jornal = Source_Checking.Source()
			political_bias, factuality = jornal.get_stats()
			
			print(40*'-')
			print(13*' ' + 'POLITICAL BIAS' + 13*' ')
			print(40*'-')
			print ('|-> Extreme-left: '+ str(political_bias[0]['0']))
			print ('|-> Left:         '+ str(political_bias[0]['1']))
			print ('|-> Center-left:  '+ str(political_bias[0]['2']))
			print ('|-> Center:       '+ str(political_bias[0]['3']))
			print ('|-> Center-right: '+ str(political_bias[0]['4']))
			print ('|-> Right:        '+ str(political_bias[0]['5']))
			print ('|-> Extreme-right '+ str(political_bias[0]['6']))
			print(40*'-')
			print('\n')

			print(40*'-')
			print(13*' ' + 'FACTUALITY' + 13*' ')
			print(40*'-')
			print ('|-> Low:       '+ str(factuality[0]['0']))
			print ('|-> Mixed:     '+ str(factuality[0]['1']))
			print ('|-> High:      '+ str(factuality[0]['2']))
			print ('|-> Very High: '+ str(factuality[0]['3']))
			print(40*'-')
			print('\n')

		elif (i == '5'):
			print('Tchau')
		else:
			print('Inválido!')


main()

def test():
	jornal = Source_Checking.Source()
	jornal.get_stats()

#test()