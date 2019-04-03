import random
import math
from Sudoku import sudoku


class Population:
    def __init__(self, popSize, game):
        self.popSize = popSize
        self._basegame = game
        self._pop = []

    def setPop(self, newpop):
        self._pop = newpop

    def getPop(self):
        return self._pop[:]

    def halfPop(self):
        self.sortByFitness()
        self._pop = self._pop[0:self.popSize]

    # initialize the population with random genes
    def init(self):
        self._pop = [self._basegame.copy(True) for _ in range(self.popSize)]

    def eval(self):
        for p in self._pop:
            p.calcFitness()
        # self.sortByFitness()

    def sortByFitness(self):
        for i in range(len(self._pop)):
            for j in range(i, len(self._pop)):
                if self._pop[j].getFitness() < self._pop[i].getFitness():
                    self._pop[i], self._pop[j] = self._pop[j], self._pop[i]

    # roulete select
    def select(self, noSelected=1):
        if noSelected < 1:
            return None
        sum = 0
        beta = -0.1
        for p in self._pop:
            # if the fitness is 0 we found the solution so we select just in case
            if p.getFitness() != 0:
                sum += math.exp(beta * p.getFitness())
            else:
                return [p for _ in range(noSelected)]

        sum0 = 0

        ret = []
        for _ in range(noSelected):
            r = random.uniform(0, sum)
            for p in self._pop:
                sum0 += math.exp(beta * p.getFitness())
                if r < sum0:
                    ret.append(p)
                    break
            sum0 = 0
        return ret if noSelected > 1 else ret[0]

    # index select
    def select2(self, noSelected=1):
        if noSelected < 1:
            return None
        sum = (len(self._pop) * len(self._pop) - 1) // 2
        sum0 = 0
        ret = []
        for _ in range(noSelected):
            r = random.randint(0, sum)
            l = len(self._pop)
            for i in range(len(self._pop)):
                sum0 += l - i
                if r <= sum0:
                    ret.append(self._pop[i])
                    break
            sum0 = 0
        return ret

    # tournir
    def select2(self, noSelected=1, nrcht=4):
        ret = []

        for _ in range(noSelected):
            r = [random.randint(0, len(self._pop) - 1) for _ in range(nrcht)]
            ret.append(self._pop[min(r, key=lambda x: self._pop[x].getFitness())])
        return ret

    # get the best member of population
    def best(self):
        minf = self._pop[0].getFitness()
        b = self._pop[0]
        for p in self._pop:
            if p.getFitness() < minf:
                minf = p.getFitness()
                b = p
        return b
