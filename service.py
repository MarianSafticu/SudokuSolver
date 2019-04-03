import os
from population import Population
import tkinter as tk


class Service:
    def __init__(self, sp):
        self._sp = sp
        self._s = self._sp.getS()

    # check if sudoku is valid
    def Validate(self):
        return self._s.valid()

    # complete with greedy algorithm
    def greedy(self, ofile, show_update=False, show_final=True):
        cn = self._s
        while cn is not None:
            if show_update:
                print(cn)
                os.system("cls")

            a = cn.getChildrenGreedy()
            if a is not None:
                cn = a
            elif cn.finished():
                try:
                    cn.valid()
                except Exception:
                    input("Error in finishing sudoku, Fail to complete valid!!")
                self._sp.writeS(ofile, cn)
                return cn if show_final else None
            else:
                cn = cn.getParent()

    # complete with DFS
    def dfs(self, ofile, show_update=False, show_final=True ):
        cn = self._sp.getS()
        while cn is not None:
            if show_update:
                print(cn)
                os.system("cls")
            a = cn.getChildren()
            if a is not None:
                cn = a
            elif cn.finished():
                try:
                    cn.valid()
                except Exception:
                    input("Error in finishing sudoku, Fail to complete valid!!")
                if show_final:
                    print(cn)
                    self._sp.writeS(ofile, cn)
                return
            else:
                cn = cn.getParent()

    # genetical algorithm returns the solution and generation
    def GA(self, ofile, popSize, generations, mutationRate, root):
        generation = 0
        p = Population(popSize, self._s)
        p.init()
        p.eval()
        best = p.best()

        maxim = len(best.getZeroPos())
        canv = self._graph(root, maxim, generations)
        cx = 21
        dx = 980 / generations
        try:
            prev = (cx, map(best.getFitness(), 0, maxim, 490, 0))
            for generation in range(generations):
                best = p.best()

                cx += dx
                prev = self._drawLine(cx, best, maxim, prev, root, canv)

                if best.getFitness() == 0:
                    best.placeNumbers()
                    return best, generation, canv
                newpop = [best]
                # newpop=[]
                for _ in range(popSize - 1):
                    selected = p.select(2)
                    off = selected[0].crossover(selected[1])
                    off.mutate(mutationRate)
                    newpop.append(off)
                p.setPop(newpop)
                p.eval()

            best = p.best()
            best.placeNumbers()
            self._sp.writeS(ofile, best)
            return best, generations, canv
        except Exception:
            best = p.best()
            best.placeNumbers()
            self._sp.writeS(ofile, best)
            return best, generation, None

    def HC(self, ofile, generations, mutationRate, root):
        try:
            best = self._s.copy(True)
            best.calcFitness()

            maxim = len(best.getZeroPos())
            canv = self._graph(root, maxim, generations)

            cx = 21
            dx = 980 / generations
            prev = (cx, map(best.getFitness(), 0, maxim, 490, 0))

            for generation in range(generations):
                ot = best.mutate(mutationRate, False)
                ot.calcFitness()
                if ot.getFitness() < best.getFitness():
                    best = ot

                cx += dx
                prev = self._drawLine(cx, best, maxim, prev, root, canv)

                if best.getFitness() == 0:
                    best.placeNumbers()
                    return best, generation, canv

            best.placeNumbers()
            self._sp.writeS(ofile, best)
            return best, generations, canv
        except Exception:
            self._sp.writeS(ofile, best)
            return best, generation, None

    @staticmethod
    def _graph(root, maxim, popSize):
        # create canvas on root
        canv = tk.Canvas(root, width=1000, height=500)
        canv.pack()
        # create lines of graph
        canv.create_line(20, 500, 20, 0)
        canv.create_line(18, 490, 1000, 490)

        canv.create_text(2, map(maxim, 0, maxim, 490, 0), text="%03d" % maxim, anchor=tk.NW)
        canv.create_text(23, 0, text="fitness", anchor=tk.NW, fill="#008f00")

        canv.create_text(2, map(int(maxim / 2), 0, maxim, 490, 0), text="%03d" % int(maxim / 2), anchor=tk.NW)
        canv.create_line(20, map(int(maxim / 2), 0, maxim, 490, 0), 1000, map(int(maxim / 2), 0, maxim, 490, 0),
                         fill="#0000ff")

        canv.create_text(2, map(0, 0, maxim, 490, 0), text="000", anchor=tk.NW)

        canv.create_text(2, map(int(maxim / 4), 0, maxim, 490, 0), text="%03d" % int(maxim / 4), anchor=tk.NW)
        canv.create_line(20, map(int(maxim / 4), 0, maxim, 490, 0), 1000, map(int(maxim / 4), 0, maxim, 490, 0),
                         fill="#0000ff")

        canv.create_text(2, map(int((3 * maxim) / 4), 0, maxim, 490, 0), text="%03d" % int((3 * maxim) / 4),
                         anchor=tk.NW)
        canv.create_line(20, map(int((3 * maxim) / 4), 0, maxim, 490, 0), 1000,
                         map(int((3 * maxim) / 4), 0, maxim, 490, 0), fill="#0000ff")

        canv.create_text(2, map(int(maxim / 8), 0, maxim, 490, 0), text="%03d" % int(maxim / 8), anchor=tk.NW)
        canv.create_line(20, map(int(maxim / 8), 0, maxim, 490, 0), 1000, map(int(maxim / 8), 0, maxim, 490, 0),
                         fill="#0000ff")

        canv.create_text(2, map(int((maxim * 3) / 8), 0, maxim, 490, 0), text="%03d" % int((maxim * 3) / 8),
                         anchor=tk.NW)
        canv.create_line(20, map(int((maxim * 3) / 8), 0, maxim, 490, 0), 1000,
                         map(int((maxim * 3) / 8), 0, maxim, 490, 0), fill="#0000ff")

        canv.create_text(2, map(int((maxim * 5) / 8), 0, maxim, 490, 0), text="%03d" % int((5 * maxim) / 8),
                         anchor=tk.NW)
        canv.create_line(20, map(int((maxim * 5) / 8), 0, maxim, 490, 0), 1000,
                         map(int((maxim * 5) / 8), 0, maxim, 490, 0), fill="#0000ff")

        canv.create_text(2, map(int((7 * maxim) / 8), 0, maxim, 490, 0), text="%03d" % int((7 * maxim) / 8),
                         anchor=tk.NW)
        canv.create_line(20, map(int((7 * maxim) / 8), 0, maxim, 490, 0), 1000,
                         map(int((7 * maxim) / 8), 0, maxim, 490, 0), fill="#0000ff")

        canv.create_text(15 + (980 // 2), 490, text="%03d" % (popSize // 2), anchor=tk.NW)
        canv.create_line(20 + (980 // 2), 0, 20 + (980 // 2), 490, fill="#0000ff")

        canv.create_text(15 + (980 // 4), 490, text="%03d" % (popSize // 4), anchor=tk.NW)
        canv.create_line(20 + (980 // 4), 0, 20 + (980 // 4), 490, fill="#0000ff")

        canv.create_text(15 + (3 * 980 // 4), 490, text="%03d" % (3 * popSize // 4), anchor=tk.NW)
        canv.create_line(20 + (3 * 980 // 4), 0, 20 + (3 * 980 // 4), 490, fill="#0000ff")

        canv.create_text(940, 485, text="generation", anchor=tk.NW, fill="#008f00")

        return canv

    @staticmethod
    def _drawLine(cx, best, maxim, prev, root, canv):
        # draw line
        next = (cx, map(best.getFitness(), 0, maxim, 490, 0))
        canv.create_line(prev[0], prev[1], next[0], next[1], fill="#ff0000")
        root.update()
        return next


def map(val, x, y, a, b):
    return ((val - x) * (b - a)) / (y - x) + a
