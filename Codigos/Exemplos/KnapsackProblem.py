#########################################################################################
# Knapsack Problem.                                                                     #
# Com um conjunto de itens aleatórios, e sabendo seus pesos e valores, queremos encher  #
# uma mochila de modo que sua capacidade máxima não seja ultrapassada e sua carga tenha #
# o maior valor total possível.                                                         #
#########################################################################################

import random
import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

IND_INIT_SIZE = 5   # "Tamanho" do indivíduo.
MAX_ITEM = 50       # Quantidade máximo de itens na mochila.
MAX_WEIGHT = 50     # Capacidade máxima supordada.
NBR_ITEMS = 20      # Variedade de itens.

creator.create("Fitness", base.Fitness, weights = (-1.0, 1.0))
# Nesse problema, cada indivíduo é um conjundo de itens a serem colocados na mmochila.
creator.create("Individual", set, fitness = creator.Fitness)

# Dicionário de itens. O nome de cada item é um número inteiro, e seu valor é dado por  #
# um par (peso, valor).                                                                 #
items = {}

# Criando itens aleatórios.
for i in range(NBR_ITEMS):
    items[i] = (random.randint(1, 10), random.uniform(0, 100))

toolbox = base.Toolbox()
toolbox.register("attr_item", random.randrange, NBR_ITEMS)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_item, IND_INIT_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Função para avaliar o estado da mochila.
def evalKnapsack(individual):
    weight = 0.0
    value = 0.0
    for item in individual:
        weight += items[item][0]
        value += items[item][1]
    if len(individual) > MAX_ITEM or weight > MAX_WEIGHT:
        return 10000, 0             # Ensure overweighted bags are dominated
    return weight, value

# Definindo operador de crssover para conjuntos.
def cxSet(ind1, ind2):
    # Nesse crossover, o primeiro filho é gerado pela intersecção dos conjuntos pais,
    # o segundo é gerado pela diferença.

    temp = set(ind1)                
    ind1 &= ind2    # Insterseção
    ind2 ^= temp    # Diferença.
    return ind1, ind2   # Dois pais gerando dois filhos.   
    
def mutSet(individual):
    # A mutação é definida pela remoção ou inserção de algum item aleatório.
    if random.random() < 0.5:
        if len(individual) > 0:
            individual.remove(random.choice(sorted(tuple(individual))))
    else:
        individual.add(random.randrange(NBR_ITEMS))
    return individual,

toolbox.register("evaluate", evalKnapsack)
toolbox.register("mate", cxSet)
toolbox.register("mutate", mutSet)
toolbox.register("select", tools.selNSGA2)

# Colocando argumentos para testes manuais.
def main(MU, LAMBDA, CXPB, MUTPB):
    NGEN = 50       # Número de gerações. Não entendi o motivo, mas o algorítmo apresenta erro para valores != 50.
#   MU = 50         # Número de indivíduos para selecionar para próxima geração.
#   LAMBDA = 100    # Número de filhos para serem produzidos a cada geração.
#   CXPB = 0.7      # Probapilidade de crossover.
#   MUTPB = 0.2     # Probabilidade de Mutação.
    
    pop = toolbox.population(n = MU)    # População.
    hof = tools.ParetoFront()           # Melhores individuos.
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)

    algorithms.eaMuPlusLambda(pop, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, stats, halloffame = hof)
    
    return pop, stats, hof

MU = int(input("Número de individuos a serem selecionados para a próxima geracao: "))
LAMBDA = int(input("Número de filhos a serem produzidos a cada geracao: "))
CXPB = float(input("Chance de sucesso de crossover: "))
MUTPB = float(input("Chance de sucesso de mutacao: "))

main(MU, LAMBDA, CXPB, MUTPB)