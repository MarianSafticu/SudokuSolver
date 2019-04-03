import math as mt
import random

class sudoku:
    def __init__(self, n, elems):
        self._n = n
        self._elems = elems
        # atributes for Search
        self._chmove = None
        self._posMoves = None
        self._tm = None
        self._parent = None

        # atributes for GA and HC
        self._zeropos = None  # the free positions, that will be the genes of chromosome for GA
        self._remNumbers = []
        self._fitness = None
        self._remNumbersPos = None

    def getFitness(self):
        return self._fitness

    def getChmove(self):
        return self._chmove

    #referinta
    def getPosMove(self):
        return self._posMoves

    def getThisMove(self):
        return self._tm

    #referinta
    def getZeroPos(self, remnum=False):
        if self._zeropos is None:
            self.blanksAndRemNumbers(False)
        return self._zeropos

    #referinta
    def getRemnumbers(self):
        return self._remNumbers

    #referinta
    def getElems(self):
        return self._elems

    def getNr(self):
        return self._n

    def setChmove(self, new):
        self._chmove = new

    # referinta
    def setPosMove(self, new):
        self._posMoves = new

    def setThisMove(self, new):
        self._tm = new

    # referinta
    def setZeroPos(self, new):
        self._zeropos = new

    # referinta
    def setRemnumbers(self, new):
        self._remNumbers = new

    # referinta
    def setElems(self, new):
        self._elems = new

    def setParrent(self, new):
        self._parent = new

    def copyElems(self):
        nelems = []
        for i in self._elems:
            nelems.append(i[:])
        return nelems

    # copy the sudoku and initialize the zeropos and remNumbers if they are not initialized
    def copy(self, randomize=False):
        # ret = sudoku(self._n, self.copyElems())
        ret = sudoku(self._n, self._elems)
        if self._zeropos is None or self._remNumbers is None:
            self.blanksAndRemNumbers(False)

        if self._remNumbersPos is None:
            self._remNumbersPos = []
            for zp in self._zeropos:
                self._remNumbersPos.append(self.posMove(zp[0], zp[1]))

        ret._zeropos = self._zeropos
        ret._remNumbers = self._remNumbers[:]
        ret._remNumbersPos = self._remNumbersPos

        if randomize:
            ret.randomizeGenes()

        return ret

    # cut point crossover
    def crossover(self, ot):
        p1 = random.randint(0, len(self._zeropos))
        off = sudoku(self._n, self._elems)
        off._zeropos = self._zeropos
        off._remNumbersPos = self._remNumbersPos
        off._remNumbers = []

        for i in range(len(self._zeropos)):
            if i <= p1:
                off._remNumbers.append(self._remNumbers[i])
            else:
                off._remNumbers.append(ot._remNumbers[i])

        return off

    # random gene crossover
    def crossover2(self, ot):
        off = sudoku(self._n, self._elems)
        off._zeropos = self._zeropos
        off._remNumbersPos = self._remNumbersPos
        off._remNumbers = []

        for i in range(len(self._zeropos)):
            if random.random() < 0.5:
                off._remNumbers.append(self._remNumbers[i])
            else:
                off._remNumbers.append(ot._remNumbers[i])

        return off

    # random initialization for population of genetical algorithm
    def randomizeGenes(self):
        self._remNumbers = [self._remNumbersPos[i][random.randint(0, len(self._remNumbersPos[i]) - 1)] for i in
                            range(len(self._zeropos))]
        # self._remNumbers = [random.randint(1, self._n) for i in range(len(self._zeropos))]

    # for GA and HC
    # mutation can modify the current chromosome(inplace) or return a modified copy
    def mutate(self, mutRate, inplace=True):
        if inplace:
            for i in range(len(self._zeropos)):
                if random.random() < mutRate:
                    self._remNumbers[i] = self._remNumbersPos[i][random.randint(0, len(self._remNumbersPos[i]) - 1)]
                    # self._remNumbers[i] = random.randint(1, self._n)
        else:
            ret = self.copy()
            for i in range(len(ret._zeropos)):
                if random.random() < mutRate:
                    ret._remNumbers[i] = self._remNumbersPos[i][random.randint(0, len(self._remNumbersPos[i]) - 1)]
                    # ret._remNumbers[i] = random.randint(1, self._n)
            return ret

    # the fitness is the numbers of wrong numbers
    def calcFitness(self):
        errors = 0
        self.placeNumbers()
        for i in range(len(self._zeropos)):
            aux = self._remNumbers[i]
            self._elems[self._zeropos[i][0]][self._zeropos[i][1]] = 0
            if not self._isValid(self._zeropos[i][0], self._zeropos[i][1], self._remNumbers[i]):
                errors += 1
            self._elems[self._zeropos[i][0]][self._zeropos[i][1]] = self._remNumbers[i]
        self._fitness = errors

    # place numbers in the empty places
    def placeNumbers(self):
        for i in range(len(self._remNumbers)):
            self._elems[self._zeropos[i][0]][self._zeropos[i][1]] = self._remNumbers[i]

    # calculate all posible numbers to put in one square
    def _isValid(self, line, col, elem):
        ssq = int(mt.sqrt(self._n))
        bigsql, bigsqc = line // ssq, col // ssq
        for i in range(self._n):
            if i != col and self._elems[line][i] == elem:
                return False
            if i != line and self._elems[i][col] == elem:
                return False
            l, c = (bigsql * ssq) + i // ssq, (bigsqc * ssq) + i % ssq
            if line != l and col != c and self._elems[l][c] == elem:
                return False
        return True

    #insertion sort (dubios) of frequency
    def _sortPosG(self,pos,fr):
        for i in range(1,len(pos)):
            p = i
            for j in range(i, 0, -1):
                if fr[pos[p]-1] < fr[pos[j]-1]:
                    aux = pos[p]
                    pos[p] = pos[j]
                    pos[j] = aux
                    p = j
        return pos

    # calculate all posible numbers to put in one square
    def posMove(self, line, col):
        ssq = int(mt.sqrt(self._n))
        pos = [x+1 for x in range(self._n)]
        bigsql, bigsqc = line // ssq, col // ssq
        for i in range(self._n):
            if i != col and self._elems[line][i] != 0:
                try:
                    pos.remove(self._elems[line][i])
                except Exception:
                    pass
            if i != line and self._elems[i][col] != 0:
                try:
                    pos.remove(self._elems[i][col])
                except Exception:
                    pass
            l, c = (bigsql*ssq)+i//ssq, (bigsqc*ssq)+i%ssq
            if line != l and col != c and self._elems[l][c] != 0:
                try:
                    pos.remove(self._elems[l][c])
                except Exception:
                    pass
        return pos

    # calculate all posible numbers to put in one square
    # and remove those moves that make others invalid
    def posValMoves(self, line, col):
        ssq = int(mt.sqrt(self._n))
        pos = self.posMove(line, col)
        bigsql, bigsqc = line // ssq, col // ssq
        if len(pos) == 1:
            return pos
        # frequency of other moves
        elems = [0 for i in range(self._n)]
        for i in pos:
            elems[i-1] += 1
        # calculate valid moves for all other position that conflicts with the curent one
        for i in range(self._n):
            if i >= 3 and i != col and self._elems[line][i] == 0:
                p = self.posMove(line, i)
                for elm in p:
                    elems[i-1] += 1
            if i >= 3 and i != line and self._elems[i][col] == 0:
                p = self.posMove(i, col)
                for elm in p:
                    elems[i-1] += 1
            l, c = (bigsql * ssq) + i // ssq, (bigsqc * ssq) + i % ssq
            if line != l and col != c and self._elems[l][c] == 0:
                p = self.posMove(l, c)
                for elm in p:
                    elems[i-1] += 1
        return self._sortPosG(pos, elems)

    # check if some numbers are in conflict
    def valid(self):
        for i in range(self._n):
            for j in range(self._n):
                if self._elems[i][j] != 0:

                    aux = self._elems[i][j]
                    self._elems[i][j] = 0
                    all = self.posMove(i, j)
                    try:
                        all.remove(aux)
                    except ValueError:
                        return i, j

                    self._elems[i][j] = aux
        return None

    # check if sudoku is finished
    def finished(self):
        if self._zeropos is not None:
            self.blanksAndRemNumbers(False)
        return len(self._zeropos) == 0

    # compute all blanks spaces and all remaining numbers
    # rem numbers is for GA and HC
    def blanksAndRemNumbers(self, remnr=True):
        if remnr:
            self._remNumbers = [i+1 for j in range(self._n) for i in range(self._n)]
        self._zeropos = []
        for i in range(self._n):
            for j in range(self._n):
                if self._elems[i][j] == 0:
                    self._zeropos.append((i, j))
                elif remnr:
                    self._remNumbers.remove(self._elems[i][j])


    # get first empty space
    def firstBlank(self):
        if self._zeropos is None:
            self.blanksAndRemNumbers(False)
        if len(self._zeropos) != 0:
            ret = self._zeropos[0]
            self._zeropos.remove(ret)
            return ret
        return None

    # get the empty space with fewest possible numbers to fill
    def getBestBlank(self):
        if self._zeropos is None:
            self.blanksAndRemNumbers(False)
        try:
            minp = self._zeropos[0]
        except IndexError:
            return None
        min = len(self.posMove(self._zeropos[0][0], self._zeropos[0][1]))
        for i in self._zeropos:
            current = len(self.posMove(i[0], i[1]))
            if current < min:
                minp = i
                min = current
            if min == 1:
                self._zeropos.remove(minp)
                return minp[0], minp[1]
        self._zeropos.remove(minp)
        return minp[0], minp[1]

    # get the children (complete the first blank with a number)
    def getChildren(self):
        if self._chmove is None:
            self._chmove = self.firstBlank()
        if self._chmove is None:
            return None
        if self._posMoves is None:
            self._posMoves = self.posMove(self._chmove[0],self._chmove[1])
        if len(self._posMoves) == 0:
            return None
        elem = self._posMoves[0]
        self._posMoves.remove(elem)
        self._elems[self._chmove[0]][self._chmove[1]] = elem
        sp = sudoku(self._n, self._elems)
        sp._tm = self._chmove
        sp._parent = self
        sp._zeropos = self._zeropos
        return sp

    # get the children for Greedy completion ( fill the blank with the fewest possible number of moves )
    def getChildrenGreedy(self):
        if self._chmove is None:
            self._chmove = self.getBestBlank()
        if self._chmove is None:
            return None
        if self._posMoves is None:
            self._posMoves = self.posValMoves(self._chmove[0], self._chmove[1])
        if len(self._posMoves) == 0:
            return None
        elem = self._posMoves[0]
        self._posMoves.remove(elem)
        self._elems[self._chmove[0]][self._chmove[1]] = elem
        sp = sudoku(self._n, self._elems)
        sp._tm = self._chmove
        sp._parent = self
        sp._zeropos = self._zeropos
        return sp

    # remove the last number added
    # None if no number added previously
    def getParent(self):
        if self._parent is not None:
            if self._tm is not None:
                self._zeropos.append((self._tm[0], self._tm[1]))
                self._elems[self._tm[0]][self._tm[1]] = 0
            self._parent._zeropos = self._zeropos
        return self._parent

    def __str__(self):
        stri = ""
        for i in range(self._n):
            stri += str(self._elems[i])+"\n"
        return stri
