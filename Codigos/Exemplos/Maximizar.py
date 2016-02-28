################################################################################
# Ícaro Marcelino Miranda                                                      #
# Programa para maximizar funções em um intervalo.                             #
# Baseado no exemplo OneMaxProblem e no livro Genetics Algorithms (Goldberg)   #
################################################################################
import random
import math

from deap import base
from deap import creator
from deap import tools

print ("Maximizando Funcoes")
# Obs.: Como um dicionário binário está sendo utilizado, os limites do intervalo
# só coincidirão quando o valor digitado for uma potência de 2 menos 1. (p.e 7, 31, 63...)
INTER = int(input("Digite o alcance do intervalo (centrado no zero): "))

TAM = int((math.log((INTER), 2)))+1 # Tamanho da string binária

creator.create("FitnessMax", base.Fitness, weights = (1.0,))
creator.create("Individual", list, fitness = creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("attr_bool", random.randint, 0, 1)

toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, TAM)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Função a ser maximizada
def f(x):
    return (100 - x**2)

def evalOneMax(individual):
    soma = 0
    peso = len(individual)-1
    i = 1

# Conversão de uma string binária em um número inteiro.   
    while peso >= 0:
        soma += individual[1]*2**peso
        peso -= 1
        i += 1

    if individual[1] == 1:
        soma *= -1

    return f(soma), # Retornado o fitness.

toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

# Coloquei argumentos para testar várias possibilidades de com diferentes populações. 
def main(NGEN, CXPB, MUTPB):
    # População com 300 indivíduos.
    pop = toolbox.population(n=300)

    # Avaliando os indivíduos.
    # Para cada par (ind, fit), atribua o valor fitness para o respectivo indivíduo.
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    # Evolução:
    for g in range(NGEN):
        print("-- Generation %i --" % g)

        # Seleção da próxima geração.
        offspring = toolbox.select(pop, len(pop))
        # Duplica os selecionados.
        offspring = list(map(toolbox.clone, offspring))

        # Crossover na população, cada par é composto por um elemento ímpar e um par da lista.
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            # Levando em conta o sucesso definido para crossover...
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        # Chance de mutação.
        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Verificando se os fitness são válidos, e corrigindo caso contrário.
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # A prole se torna a nova população.
        pop[:] = offspring

        # Array com todos os fitness para estatísticas.
        fits = [ind.fitness.values[0] for ind in pop]
        
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5
        
        print("  Min %s" % min(fits))   # Valor máximo.
        print("  Max %s" % max(fits))   # Valor mínimo.
        print("  Avg %s" % mean)        # Valor médio.
        print("  Std %s" % std)         # Desvio padrão da geração.
        print("  Melhor %s" % str((evalOneMax((tools.selBest(pop, 1)[0]))[0]-100)**0.5));
        print("  Pior %s" % str((evalOneMax((tools.selWorst(pop, 1)[0]))[0]-100)**0.5));
# Fim da main.

NGEN = int(input('Numero de geracoes: '))
CXPB = float(input('Probabilidade de crossover: '))
MUTPB = float(input('Probabilidade de mutacao: '))
main(NGEN, CXPB, MUTPB)