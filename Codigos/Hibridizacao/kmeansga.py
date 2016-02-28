import random
from deap import base
from deap import creator
from deap import tools
from sklearn import cross_validation
from sklearn import datasets

class Ponto:
	def __init__(self, coordenadas):
		self.coordenadas = coordenadas
	
	def setCoordenada(self, coordenada, n):
		self.coordenadas[n] = coordenada

	def getCoordenadas(self):
		return self.coordenadas

	def setCluster(self, cluster):
		self.cluster = cluster
	
	def getCluster(self):
		return self.cluster

	def setDistancia(self, distancia):
		self.distancia = distancia

	def getDistancia(self):
		return self.distancia

	def setCentroide(self, centroide):
		self.centroide = centroide

	def getCentroide(self):
		return self.centroide

MENOR_DISTANCIA = 10**10
K = 3
TAM = 4

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

def removeOcorrencias(lista, val):
	while val in lista:
		lista.remove(val)

	return lista


def lerAmostra(nomeArquivo):
	arquivo = open(nomeArquivo, "r")
	amostra = []

	for linha in list(arquivo):
		linha = linha.split()
		amostra.append([float(x) for x in linha])

	arquivo.close()
	return amostra

def iniciarDados(amostra):
	pontos = []

	for coordenada in amostra:
		pontos.append(Ponto(coordenada))

	for ponto in pontos:
		ponto.setDistancia(MENOR_DISTANCIA)

	return pontos

def distanciaEuclidiana(ponto, centroides):
	distancia = 0

	for i in range(TAM):
		distancia += (ponto.getCoordenadas()[i] - centroides[i])**2

	distancia = distancia**(.5)

	return distancia

def atribuirClusters(pontos, centroides):
	for ponto in pontos:
		distancias = []

		ponto.setDistancia(MENOR_DISTANCIA)
		n = TAM

		i = 0
		while (i <= (len(centroides) - n)):
			distancias.append(distanciaEuclidiana(ponto, centroides[i:(i+n)]))
			i += n

		menorDistancia = min(distancias)
		ponto.setDistancia(menorDistancia)
		
		i = 0
		while (i <= (len(centroides) - n)):
			if (menorDistancia == distancias[int(i/n)]):
				ponto.setCentroide(centroides[i:(i+n)])
			i += n

	return pontos

def verificarCluster(ponto, individual, erro):
	cont = 0
	for i in range(TAM):
		if(abs(ponto.getCentroide()[i] - individual[i]) > erro):
			cont += 1

	if(cont == 0):
		return True
	else:
		return False

def avaliarFitness(individual, pontos):
	distancia = 0

	pontos = atribuirClusters(pontos, individual)

	for ponto in pontos:
		n = TAM

		i = 0
		while (i <= (len(individual) - n)):
			if(verificarCluster(ponto, individual[i:(i+n)], 0.005)):
				distancia += distanciaEuclidiana(ponto, individual[i:(i+n)])
			i += n

	distancia /= TAM
	return distancia,

# X_train = lerDados("pendigits.tra")
# X_test = lerDados("pendigits.tes")

# X_train = X_train[:500]
# X_test = X_test[:1000]

# # amostra = lerAmostra("iris.txt")
# amostra = amostra[:150]

iris = datasets.load_iris()
X_train, X_test, y_train, y_test = cross_validation.train_test_split(iris.data, iris.target, test_size=0.3, random_state=0)

def ga(treino_, teste_):
	treino = iniciarDados(treino_)
	teste = iniciarDados(teste_)

	MINIMO = 10**10
	MAXIMO = -1*MINIMO

	for lista in treino_:
		if(min(lista) < MINIMO):
			MINIMO = min(lista)
		if(max(lista) > MAXIMO):			
			MAXIMO = max(lista)

	creator.create("FitnessMax", base.Fitness, weights = (-1.0,))
	creator.create("Individual", list, fitness = creator.FitnessMax)

	toolbox = base.Toolbox()

	toolbox.register("atribuirValor", random.uniform, MINIMO, MAXIMO + abs(MAXIMO - MINIMO)/2)

	toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.atribuirValor, K*TAM)
	toolbox.register("population", tools.initRepeat, list, toolbox.individual)

	toolbox.register("evaluate", avaliarFitness, pontos = treino)
	toolbox.register("evaluateTeste", avaliarFitness, pontos = teste)
	toolbox.register("mate", tools.cxTwoPoint)
	toolbox.register("mutate", tools.mutGaussian, mu = 0, sigma = 1, indpb = 0.5)
	toolbox.register("select", tools.selTournament, tournsize = 3)

	pop = toolbox.population(n = 250)

	NGEN = 100
	CXPB = .75
	MUTPB = .1

	# Avaliando os individuos.
	# Para cada par (ind, fit), atribua o valor fitness para o respectivo individuo.

	fitnesses = list(map(toolbox.evaluate, pop))
	for ind, fit in zip(pop, fitnesses):
		ind.fitness.values = fit

	# Evolucao:
	for g in range(NGEN):
		print("\n-- Generation %i --" % g)

		# Selecao da proxima geracao.
		offspring = toolbox.select(pop, len(pop))
		# Duplica os selecionados.	

		offspring = list(map(toolbox.clone, offspring))

		# Crossover na populacao, cada par e composto por um elemento impar e um par da lista.
		for child1, child2 in zip(offspring[::2], offspring[1::2]):
			# Levando em conta o sucesso definido para crossover...
			if random.random() < CXPB:
				toolbox.mate(child1, child2)
				del child1.fitness.values
				del child2.fitness.values

		# Chance de mutacao.
		for mutant in offspring:
			if random.random() < MUTPB:
				toolbox.mutate(mutant)
				del mutant.fitness.values

		# Verificando se os fitness sao validos, e corrigindo caso contrario.
		invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
		fitnesses = map(toolbox.evaluate, invalid_ind)
		for ind, fit in zip(invalid_ind, fitnesses):
			ind.fitness.values = fit

		pop[:] = tools.selBest(offspring + tools.selBest(pop, 2), len(pop))
		# pop[:] = offspring

		# Array com todos os fitness para estatisticas.
		fits = [ind.fitness.values[0] for ind in pop]
		
		length = len(pop)
		mean = sum(fits) / length
		sum2 = sum(x*x for x in fits)
		std = abs(sum2 / length - mean**2)**0.5
		
		print("  Min: ", round(min(fits), 2))   # Valor maximo.
		print("  Max: ", round(max(fits), 2))   # Valor minimo.
		print("  Avg: ", round(mean, 2))        # Valor medio.
		print("  Std: ", round(std, 2))         # Desvio padrao da geracao.
		# print(" Melhor Individuo:\n", tools.selBest(pop, 1))
		# print(" Pior Individuo:\n", tools.selWorst(pop, 1))

		if(CXPB > .60):
			CXPB -= .001

		if(MUTPB < .20):
			MUTPB += .001

	fitnesses = list(map(toolbox.evaluateTeste, pop))
	for ind, fit in zip(pop, fitnesses):
		ind.fitness.values = fit

	fits = [ind.fitness.values[0] for ind in pop]

	length = len(pop)
	mean = sum(fits) / length
	sum2 = sum(x*x for x in fits)
	std = abs(sum2 / length - mean**2)**0.5
	
	print("\n\nAplicando os centroides nos dados de teste: ")
	print("  Min: ", round(min(fits), 2))   # Valor maximo.
	print("  Max: ", round(max(fits), 2))   # Valor minimo.
	print("  Avg: ", round(mean, 2))        # Valor medio.
	print("  Std: ", round(std, 2))         # Desvio padrao da geracao.
	print(" Melhor Individuo:\n", tools.selBest(pop, 1))
	print(" Pior Individuo:\n", tools.selWorst(pop, 1))

ga(X_train, X_test)