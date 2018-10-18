import random


def hangman(word, definition):
	lenword = len(word)
	wordguess = ['_'] * len(word)
	solved = False
	correct = 0
	incorrect = 0
	guesses = 0


	alphabet = []
	right_list = []
	wrong_list = []
	invalid = False

	for ch in 'abcdefghijklmnopqrstuvwxyz':
		alphabet.append(ch.casefold())

	while not solved:
		if not invalid:
			for i in wordguess:
				print(i, end=' ')

			print()
			print('number of guesses: ', guesses)

			print('number correct; ', correct,end=" ")
			print(right_list)

			print('number incorrect: ', incorrect,end =" ")
			print(wrong_list)
		letter = input('pick a letter ').casefold()
		invalid = False
		if letter not in alphabet:
			print('try again')
			invalid = True
		else:
			guesses += 1
			for i in range(len(alphabet) + 1):

				if alphabet[i] == letter:
					alphabet.pop(i)
					break
			if letter in word:
				correct += 1

				for k in range(lenword):
					if word[k] == letter:
						wordguess[k] = letter.capitalize()
				right_list.append(letter)

			else:

				incorrect += 1
				wrong_list.append(letter)
			if '_' not in wordguess:

				solved = True
			if incorrect > 6:
				print('Sorry, you lose')

				print(word)
				break

	if solved:

		print('Congrats!  You win!')
		print(word.capitalize(), ": ", definition.capitalize())


wordlist = {'abode':'a home','access':'an outburst of an emotion',
            'adieu':'goodbye','afar':'at a distance','apace':'quickly'
            ,'argosy':'a large merchant ship','arrant':'utter',

            'asunder':'into pieces','atrabilious':'melancholy or bad-tempered'
            ,'aurora':'the dawn','bard':'a poet','barque':'a boat'
            ,'bedizen':'dress gaudily','beget':'produce (a child)'
            ,'behold':'see','beseech':'ask urgently and fervently'
            ,'bestrew':'scatter','betake oneself':'go to','betide':'happen'
            ,'betoken':'be a warning of','blade':'sword','blithe':'happy'
            ,'bosky':'covered by trees or bushes','brand':'a sword'
            ,'brume':'mist or fog','celerity':'swiftness',
            'circumvallate':'surround with a rampart or wall'
            ,'clarion':'loud and clear','cleave to':'stick fast to'
            ,'cockcrow':'dawn','coruscate':'flash or sparkle'
            ,'crapulent':'relating to the drinking of alcohol'
            ,'crescent':'growing','darkling':'relating to growing darkness'
            ,'dell':'a small valley','dingle':'a deep wooded valley',
            'divers':'of varying types','Dives':'a rich man'
            ,'dolour':'great sorrow','dome':'a stately building'
            ,'dulcify':'sweeten','effulgent':'shining brightly','eld':'old age'
            ,'eminence':'a piece of rising ground','empyrean':'the sky'
            ,'ere':'before','erne':'a sea eagle','espy':'catch sight of'
            ,'ether':'the clear sky','evanescent':'quickly fading'
            ,'farewell':'goodbye','fervid':'hot or glowing'
            ,'finny':'relating to fish','firmament':'the sky'
            ,'flaxen':'pale yellow','fleer':'jeer or laugh disrespectfully'
            ,'flexuous':'full of bends and curves','fulgent':'shining brightly'
            ,'fulguration':'a flash like lightning','fuliginous':'sooty; dusky'
            ,'fulminate':'explode violently','furbelow':'adorn with trimmings'
            ,'gird':'secure with a belt','glaive':'a sword','gloaming':'dusk'
            ,'greensward':'grassy ground','gyre':'whirl or gyrate'
            ,'hark':'listen','horripilation':'gooseflesh; hair standing on end'
            ,'hymeneal':'relating to marriage'
            ,'ichor':'blood or a fluid likened to it','illude':'trick someone',
            'imbrue':'stain ones hand or sword with blood'
            ,'impuissant':'powerless'
            ,'incarnadine':'colour (something) crimson'
            ,'ingrate':'ungrateful','inhume':'bury','inly':'inwardly'
            ,'ire':'anger','isle':'an island','knell':'the sound of a bell'
            ,'lachrymal':'connected with weeping or tears'
            ,'lacustrine':'associated with lakes'
            ,'lambent':'softly glowing or flickering'
            ,'lave':'wash or wash over','lay':'a song'
            ,'lea':'an area of grassy land','lenity':'kindness or gentleness'
            ,'lightsome':'nimble','limn':'represent in painting or words'
            ,'lucent':'shining','madding':'acting madly; frenzied',
            'mage':'a magician or learned person','malefic':'causing harm'
            ,'manifold':'many and various','marge':'a margin','mead':'a meadow'
            ,'mephitic':'foul-smelling','mere':'a lake or pond'
            ,'moon':'a month','muliebrity':'womanliness'
            ,'nescient':'lacking knowledge; ignorant','nigh':'near'
            ,'niveous':'snowy','nocuous':'noxious harmful or poisonous'
            ,'noisome':'foul-smelling','nymph':'a beautiful young woman',
            'orb':'an eye','orgulous':'proud or haughty'
            ,'pellucid':'translucent','perchance':'by some chance'
            ,'perfervid':'intense and impassioned'
            ,'perfidious':'deceitful and untrustworthy',
            'philippic':'a bitter verbal attack'
            ,'plangent':'loud and mournful'
            ,'plash':'a splashing sound','plenteous':'plentiful'
            ,'plumbless':'extremely deep','poesy':'poetry',
            'prothalamium':'a song or poem celebrating a wedding'
            ,'puissant':'powerful or influential','pulchritude':'beauty'
            ,'purl':'flow with a babbling sound'
            ,'quidnunc':'an inquisitive and gossipy person','realm':'a kingdom'
            ,'refulgent':'shining brightly','rend':'tear to pieces'
            ,'repine':'be discontented'
            ,'Rhadamanthine':'stern and incorruptible in judgement'
            ,'roundelay':'a short, simple song with a refrain'
            ,'rubescent':'reddening'
            ,'rutilant':'glowing or glittering with red or golden light'
            ,'sans':'without','scribe':'write','sea-girt':'surrounded by sea'
            ,'sempiternal':'everlasting','serpent':'a snake',
            'shade':'a ghost','ship of the desert':'a camel','shore':'country by the sea','slay':'kill','slumber':'sleep','star-crossed':'ill-fated','steed':'a horse','stilly':'still and quiet',

            'storied':'celebrated in stories','strand':'a shore','Stygian':'very dark','summer':'a year of a personss age','supernal':'relating to the sky or the heavens','susurration':'a whispering or rustling sound',

            'swain':'a young lover or suitor','sylvan':'wooded','tarry':'delay leaving','temerarious':'rash or reckless','tenebrous':'dark; shadowy','threescore':'sixty',

            'thrice':'three times','tidings':'news; information','toilsome':'involving hard work','tope':'drink alcohol to excess','travail':'painful or laborious effort','troublous':'full of troubles',

            'tryst':'a rendezvous between lovers','unman':'deprive of manly qualities','vestal':'chaste; pure','vesture':'clothing','virescent':'greenish','viridescent':'greenish or becoming green',

            'visage':'a persons face','want':'lack or be short of','wax':'become larger or stronger','wayfarer':'a person who travels on foot','wed':'marry','wind':'blow (a bugle)',

            'without':'outside','wondrous':'inspiring wonder','wont':'accustomed','wonted':'usual','wrathful':'extremely angry','wreathe':'twist or entwine','yon':'yonder; that','yore':'of former ties or long ago',

            'youngling':'a young person or animal','zephyr':'a soft, gentle breeze'}


CONTINUE = True
print("Welcome")
while CONTINUE:
	CONT = input('do you want to play Hangman? [Y]es, [N]o')
	if CONT[0].casefold() == 'y'.casefold():
		word, definition = random.choice(list(wordlist.items()))

		hangman(word, definition)
	else:
		CONTINUE = False
