##
# \file kmeans.py
# \author Icaro Marcelino  
# \since 10/2015
# \verion 2.0
#
# Uma implementação do algorítmo k-means para clusterização.
#
##
import random
import matplotlib.pyplot as plt

class Centroide:

	def __init__(self, x, y, z, w):
		self.x = x
		self.y = y
		self.z = z
		self.w = w
	
	def setX(self, x):
		self.x = x
	
	def getX(self):
		return self.x
	
	def setY(self, y):
		self.y = y
	
	def getY(self):
		return self.y	

	def setZ(self, z):
		self.z = z
	
	def getZ(self):
		return self.z

	def setW(self, w):
		self.w = w
	
	def getW(self):
		return self.w

class Ponto:
	def __init__(self, x, y, z, w):
		self.x = x
		self.y = y
		self.z = z
		self.w = w
	
	def setX(self, x):
		self.x = x
	
	def getX(self):
		return self.x
	
	def setY(self, y):
		self.y = y
	
	def getY(self):
		return self.y

	def setZ(self, z):
		self.z = z
	
	def getZ(self):
		return self.z

	def setW(self, w):
		self.w = w
	
	def getW(self):
		return self.w

	def setCluster(self, cluster):
		self.cluster = cluster
	
	def getCluster(self):
		return self.cluster

	def setDistancia(self, distancia):
		self.distancia = distancia

	def getDistancia(self):
		return self.distancia

MENOR_DISTANCIA = 10**10

def definirCentroides(indices, amostra):
	centroides = []
	print("\nCentroides inicializados:")

	for indice in indices:
		x = amostra[int(indice)][0]
		y = amostra[int(indice)][1]
		z = amostra[int(indice)][2]
		w = amostra[int(indice)][3]
		centroides.append(Centroide(x, y, z, w))

	for centroide in centroides:
		print("(", centroide.getX(), ", ", centroide.getY(), ", ", centroide.getZ(), ", ", centroide.getW(), ")")

	return centroides

def distanciaEuclidiana(ponto, centroide):
	return (((ponto.getX() - centroide.getX())**2) + ((ponto.getY() - centroide.getY())**2) + ((ponto.getZ() - centroide.getZ())**2) + ((ponto.getW() - centroide.getW())**2))**0.5

def iniciarDados(amostra):
	pontos = []

	for coordenada in amostra:
		x = coordenada[0]
		y = coordenada[1]
		z = coordenada[2]
		w = coordenada[3]
		pontos.append(Ponto(x, y, z, w))

	for ponto in pontos:
		ponto.setDistancia(MENOR_DISTANCIA)

	return pontos

def atribuirClusters(pontos, centroides):    
	for ponto in pontos:
		for centroide in centroides:
			distancia = distanciaEuclidiana(ponto, centroide)

			if (distancia < ponto.getDistancia()):
				ponto.setDistancia(distancia)
				ponto.setCluster(centroides.index(centroide))

	return pontos

def reposicionarCentroides(pontos, centroides):

	for centroide in centroides:
		for ponto in pontos:
			if(ponto.getCluster() == centroides.index(centroide)):
				pontoMedioX = (centroide.getX() + ponto.getX())/2
				pontoMedioY = (centroide.getY() + ponto.getY())/2
				pontoMedioZ = (centroide.getZ() + ponto.getZ())/2
				pontoMedioW = (centroide.getW() + ponto.getW())/2

		centroide.setX(pontoMedioX) 
		centroide.setY(pontoMedioY)
		centroide.setZ(pontoMedioZ)
		centroide.setW(pontoMedioW)

	return centroides

def compararCentroides(centroides, centroidesOLD, erro):
	comp = 0

	for i in range(len(centroides)):
		if (abs(centroides[i].getX() - centroidesOLD[i].getX()) > erro):
			comp = 1
		if (abs(centroides[i].getY() - centroidesOLD[i].getY()) > erro):
			comp = 1
		if (abs(centroides[i].getZ() - centroidesOLD[i].getZ()) > erro):
			comp = 1
		if (abs(centroides[i].getW() - centroidesOLD[i].getW()) > erro):
			comp = 1

	return comp

def lerDados(nome):
	arquivo = open(nome, "r")
	amostra = []

	for linha in list(arquivo):
		linha = linha.split(',')
		linha = removeOcorrencias(linha, ' ')


		for item in linha:
			linha = removeOcorrencias(linha, ' ')
			linha = removeOcorrencias(linha, ',')
			linha = removeOcorrencias(linha, '\n')

		amostra.append([int(x) for x in linha])

	amostra.remove(amostra[len(amostra) - 1])
	arquivo.close()
	return amostra

def imprimirCentroides(centroides):
	print("\nCentroides reposicionados: ")

	for centroide in centroides:
		print("(", "%.2f" % centroide.getX(), ", ", "%.2f" % centroide.getY(), ", ", "%.2f" % centroide.getZ(), ", ", "%.2f" % centroide.getW(),")")

	return

def escolherIndices(qnt, tam_amostra):
	indices = []

	for i in range(qnt):
		indices.append(random.choice(list(range(tam_amostra))))

	return indices

def kmeans(amostra, indicesCentroides):
	rodando = 1

	centroides = definirCentroides(indicesCentroides, amostra)
	pontos = iniciarDados(amostra)
	pontos = atribuirClusters(pontos, centroides)

	while(rodando):
		centroidesOLD = centroides[::]
		centroides = reposicionarCentroides(pontos, centroides)
		pontos = atribuirClusters(pontos, centroides)

		rodando = compararCentroides(centroides, centroidesOLD, 0.00005)

	imprimirCentroides(centroides)
	return

############################################################################################################################
############################################################################################################################
amostra = lerAmostra("iris.txt")
indicesCentroides = escolherIndices(3, 150)

kmeans(amostra, indicesCentroides)
############################################################################################################################
############################################################################################################################