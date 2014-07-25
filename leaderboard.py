import pygame, sys, os, time, glob

class Leaderboard:

		def __init__(self):
	
			self.black    = (   0,   0,   0)
			self.white    = ( 255, 255, 255)
			self.green    = (   0, 255,   0)
			self.red      = ( 255,   0,   0)
			self.blue     = (   0,   0, 255)
			self.yellow   = ( 255, 255,   0)
			self.lightblue = (176, 226, 255)
			self.maize = (238, 238, 0)


			#This will be the color of the leaderboard lines
			self.linecolor = self.black	
			#This will be the title of the leaderboard
			self.headerLine = "Discussion Leaderboard"
			#This will be the caption of the leaderboard window
			self.caption = "Discussion Leaderboard"
	
			self.theme = 0
	
			self.pokeImages = {}
			self.pokeNames = []
			self.pokeImageBoardLocs = []
			self.pokeNameBoardLocs = []
			self.correctBoardLocs = []
			self.timeBoardLocs = []
			self.memBoardLocs = []

			self.picDir = "./PokePics/"

			for i in range(0, 10):
				self.pokeImageBoardLocs.append((55, 200 + i * 50))
				self.pokeNameBoardLocs.append((150, 220 + i * 50))
				self.correctBoardLocs.append((360, 220 + i * 50))
				self.timeBoardLocs.append((530, 220 + i * 50))
				self.memBoardLocs.append((680, 220 + i * 50))

			pygame.init()
			self.clock = pygame.time.Clock()
			self.screenSize = [800,700]
			self.screen = pygame.display.set_mode(self.screenSize)
			pygame.display.set_caption(self.caption)
			self.font = pygame.font.Font(None, 44)
			self.labelFont = pygame.font.Font(None, 24)

			self.nameLabel = self.labelFont.render("Submitter", 1, (10, 10, 10))
			self.correctLabel = self.labelFont.render("Status", 1, (10, 10, 10))
			self.timeLabel = self.labelFont.render("Time Usage", 1, (10, 10, 10))
			self.memoryLabel = self.labelFont.render("Mem Usage", 1, (10, 10, 10))
			self.headerSurface = self.font.render(self.headerLine, 1, (10, 10, 10))
		
			self.screen.fill(self.white)

			#self.loadImages()
	
			#self.printHeader()
			#self.printBackground()
			#self.printLabels()
			#self.printTestPokemon()

			#pygame.display.flip()

		def selectTheme(self, choice, folder):
			if choice == 1:
				self.theme = 0
				self.linecolor = self.lightblue
			elif choice == 2:
				self.linecolor = self.white
				self.theme = 1
				self.picDir = folder
			self.loadImages()

		def printBlankBoard(self):
			self.printHeader()
			self.printBackground()
			self.printLabels()
			pygame.display.flip()

		def updateBoard(self, listOfInfo, numSubmissions):
			print "Updating Leaderboard..."
			num = 10

			if len(listOfInfo) < 10:
				num = len(listOfInfo)

			self.printHeader()
			self.printBackground()
			self.printLabels()
	
			for i in range(0, num):
				name = listOfInfo[i][0]
				img = self.pokeImages[name]
				isCorrect = listOfInfo[i][1]
				correct = "True"
				if not isCorrect:
					correct = "False"
				if isCorrect == -1:
					correct = "Did Not Compile"
				if isCorrect == -2:
					correct = "Unsafe"
				runtime = str(listOfInfo[i][2])
				memoryusage = str(listOfInfo[i][3])
				
				nameSurface = self.labelFont.render(name, 1, (10, 10, 10))
				correctSurface = self.labelFont.render(correct, 1, (10, 10, 10))
				runtimeSurface = self.labelFont.render(runtime, 1, (10, 10, 10))
				memoryusageSurface = self.labelFont.render(memoryusage, 1, (10, 10, 10))

				self.screen.blit(img, self.pokeImageBoardLocs[i])
				self.screen.blit(nameSurface, self.pokeNameBoardLocs[i])
				self.screen.blit(correctSurface, self.correctBoardLocs[i])
				self.screen.blit(runtimeSurface, self.timeBoardLocs[i])
				self.screen.blit(memoryusageSurface, self.memBoardLocs[i])

				pygame.display.flip()

		def printHeader(self):
			offset = 0
			if self.theme:
				offset = 8

			pygame.draw.rect(self.screen, self.maize, [0, 0, 800, 150])
			pygame.draw.rect(self.screen, self.blue, [0, 0, 800, 150], 8)
			pygame.draw.rect(self.screen, self.maize, [5, 142, 791, 7])
			self.screen.blit(self.headerSurface, [250, 50])
			self.screen.blit(self.leftPokeHeader, [15-offset, 8])
			self.screen.blit(self.rightPokeHeader, [640+offset, 8])

		def printBackground(self):
			for i in range(2, 8):
				pygame.draw.rect(self.screen, self.linecolor, [0, i*100, 800, 50])
				pygame.draw.rect(self.screen, self.white, [0, i*100 + 50, 800, 50])
	
		def printLabels(self):
			self.screen.blit(self.nameLabel, [55, 175])
			self.screen.blit(self.correctLabel, [360, 175])
			self.screen.blit(self.timeLabel, [530, 175])
			self.screen.blit(self.memoryLabel, [680, 175])
			for i in range(0, 10):
				numSurface = self.labelFont.render(str(i+1), 1, (10, 10, 10))
				self.screen.blit(numSurface, [15, 220 + i * 50])

		def loadImages(self):
			pokePNGs = []
			pokeTitles = []
			numPokemon = 0
			imageListing = glob.glob(self.picDir + '*')
			for imageName in imageListing:
				numPokemon += 1
				name = imageName[len(self.picDir):imageName.find(".",len(self.picDir))]
				pokeImg = pygame.image.load(imageName)
				pokeImg.set_colorkey(self.white)
				pokePNGs.append(pokeImg)
				pokeTitles.append(name)
			for i in range (0, numPokemon):
				self.pokeImages[pokeTitles[i]] = pygame.transform.scale(pokePNGs[i], (50, 50))
			for pokeTitle in pokeTitles:
				self.pokeNames.append(self.labelFont.render(pokeTitle, 1, (10, 10, 10)))	

			if not self.theme:
				self.leftPokeImg = pygame.image.load("./PokePics/Bulbasaur.png")
				self.rightPokeImg = pygame.image.load("./PokePics/Pikachu.png")
            		else:
            			self.leftPokeImg = pygame.image.load("./DogPics/Snoopy.png")
            			self.rightPokeImg = pygame.image.load("./DogPics/Snoopy.png")

			self.leftPokeImg.set_colorkey(self.white)
			self.rightPokeImg.set_colorkey(self.white)
	
			self.leftPokeHeader = pygame.transform.scale(self.leftPokeImg, (140, 140))
			self.rightPokeHeader = pygame.transform.scale(self.rightPokeImg, (140, 140))
		


		def printTestPokemon(self):
			realNames = self.pokeImages.keys()
			realNames.sort()
			for i in range(0, 10):
				self.screen.blit(self.pokeImages[realNames[i]], (55, 200 + i * 50))	
				self.screen.blit(self.pokeNames[i], (150, 220 + i * 50))
