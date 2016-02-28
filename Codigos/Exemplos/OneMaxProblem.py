import random

from deap import base
from deap import creator
from deap import tools

################################################################################
# Função creator é usada para criar novas classes.                             #
# O primeiro argumento é o nome da nova classe, o segundo é a classe ancestral #
# e os seguintes são novos atributos que serão adicionados.                    #
################################################################################
creator.create("FitnessMax", base.Fitness, weights = (1.0,))
creator.create("Individual", list, fitness = creator.FitnessMax)

################################################################################
# Toolbox serve para armazenar funções com seus argumentos para serem lançadas #
# depois.                                                                      #
################################################################################
toolbox = base.Toolbox()

################################################################################
# Adicionando atributos, que no caso é true ou false.                          #
################################################################################
toolbox.register("attr_bool", random.randint, 0, 1)

################################################################################
# Iniciando estruturas. Para cada indivíduo é criado um array de 100 elementos #
# e atribuído valores booleanos para cada posição. Uma população é uma lista   #
# de indivíduos.                                                               #
################################################################################
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 100)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

################################################################################
# O valor máximo de um indivíduo é dado pela soma de seus atributos.           #
################################################################################
def evalOneMax(individual):
    return sum(individual),

################################################################################
# Registrando novas instruções. Mate: Two-Point Crossover. Mutate: Mutação do  #
# individuo podendo ocorrer em cada atributo; indpb é a chance de ocorrer uma  #
# mutação para cada atributo (eventos independentes). Select: No caso,         #
# seleciona 3 indivíduos da população.                                         #
################################################################################
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
# Fim da main.

NGEN = int(input('Numero de geracoes: '))
CXPB = float(input('Probabilidade de crossover: '))
MUTPB = float(input('Probabilidade de mutacao: '))
main(NGEN, CXPB, MUTPB)