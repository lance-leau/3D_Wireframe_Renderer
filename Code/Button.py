from math import sqrt
import pygame

#button class
class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == True and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

class Check():
	def __init__(self, x, y, image1, image2, scale, state = False):
		width = image1.get_width()
		height = image1.get_height()
		self.unchecked = image1 # pygame.transform.scale(image1, (int(width * scale), int(height * scale)))
		self.checked = image2 # pygame.transform.scale(image2, (int(width * scale), int(height * scale)))
		self.rect = self.unchecked.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
		self.state = state

	def draw(self, surface):
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == True and self.clicked == False:
				self.clicked = True
				self.state = not self.state

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		if self.state:
			surface.blit(self.checked, (self.rect.x, self.rect.y))
		else:
			surface.blit(self.unchecked, (self.rect.x, self.rect.y))

		return self.state

class RadioCheck():
	def __init__(self, x, y, image1, image2, scale, state = False):
		width = image1.get_width()
		height = image1.get_height()
		self.unchecked = image1 # pygame.transform.scale(image1, (int(width * scale), int(height * scale)))
		self.checked = image2 # pygame.transform.scale(image2, (int(width * scale), int(height * scale)))
		self.rect = self.unchecked.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
		self.state = state

	def draw(self, surface):
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == True and self.clicked == False:
				self.clicked = True
				self.state = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		if self.state:
			surface.blit(self.checked, (self.rect.x, self.rect.y))
		else:
			surface.blit(self.unchecked, (self.rect.x, self.rect.y))

		return self.state

class Slider():
    def __init__(self, x, y, BarImage, NobImage):
        NobWidth = NobImage.get_width()
        self.BarImage = BarImage
        self.NobImage = NobImage
        self.nob = self.NobImage.get_rect()
        self.bar = self.BarImage.get_rect()
        self.bar.midleft = (x, y)
        self.nob.center = self.bar.center
        self.nobOffset = NobWidth/2
        self.value = 0.5
        self.action = False
    
    def getXpos(self):
        if self.action:
            pos = pygame.mouse.get_pos()[0]
            if pos > self.bar.bottomleft[0] + self.nobOffset:
                if pos < self.bar.bottomright[0] - self.nobOffset:
                    self.nob.centerx = pos
                    self.value = (self.nob.centerx - self.bar.bottomleft[0]) / (self.bar.bottomright[0] - self.bar.bottomleft[0])
                else:
                    self.nob.centerx = self.bar.bottomright[0] - self.nobOffset - 1
                    self.value = (self.nob.centerx - self.bar.bottomleft[0]) / (self.bar.bottomright[0] - self.bar.bottomleft[0])
            else:
                self.nob.centerx = self.bar.bottomleft[0] + self.nobOffset + 1
                self.value = (self.nob.centerx - self.bar.bottomleft[0]) / (self.bar.bottomright[0] - self.bar.bottomleft[0])
        
    
    def draw(self, surface):
        #get mouse position
        pos = pygame.mouse.get_pos()
        
        #check mouseover and clicked conditions
        if self.nob.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            self.action = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.action = False
        
        self.getXpos()
            
        #draw button on screen
        surface.blit(self.BarImage, (self.bar.x, self.bar.y))
        surface.blit(self.NobImage, (self.nob.x, self.nob.y))
        
        return self.action
    
class Tactile():
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect((x, y), (width, height))
        self.shape = (float(width), float(height))
        self.valueX = 0
        self.valueY = 0
        self.posAtClick = (float(0), float(0))
        self.action = False
    
    def getXval(self):
        if self.action:
            pos = pygame.mouse.get_pos()[0]
            if self.rect.left < pos and pos < self.rect.right:
                self.valueX = (self.posAtClick[0] - pos)/self.shape[0]
    
    def getYval(self):
        if self.action:
            pos = pygame.mouse.get_pos()[1]
            if self.rect.top < pos and pos < self.rect.bottom:
                self.valueY = float(pos-self.posAtClick[1])/float(self.shape[1])
        
    
    def updatePad(self):
        #get mouse position
        pos = pygame.mouse.get_pos()
        
        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            if not self.action:
                self.posAtClick = pos
            self.action = True
            self.getXval()
            self.getYval()
        else:
            self.action = False
        
        
        return self.action
