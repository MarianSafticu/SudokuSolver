import sudokuParser
import service
import time
import tkinter as tk

class UI:
    def __init__(self):
        self._s = None
        self._ofile = None
        self._root = tk.Tk()

    def run(self):
        print("type \"exit\" to exit the program")
        while True:
            path = self._getFilePath()
            if path is None:
                return

            self._s = service.Service(sudokuParser.Sudokup(path))
            if self._valid():
                break

            self._ofile = self._getFilePath("w")
            if self._ofile is None:
                return
            algorithm = self._getAlg()
            if algorithm == "EXIT":
                return
            show = False
            if algorithm is not None:
                print("show updates of sudoku (can REALLY SLOW DOWN the algorithm)?(Y/n)")
                show = self._getResponse()
                print("print solved sudoku on screen too ? (Y/n)")
                show_final = self._getResponse()
            timeS = time.time()
            if algorithm is None:
                return
            elif algorithm == "GREEDY":
                s = self._s.greedy(self._ofile, show, show_final)
            elif algorithm == "GA":
                s = self._ga()
            elif algorithm == "HC":
                s = self._hc()
            else:
                s = self._s.dfs(self._ofile, show, show_final)
            if show_final:
                print(s)
            print("finished in {} seconds".format(time.time() - timeS))

    def _ga(self):
        popSize, generations, mutationRate = int(input("Population size: ")), int(
            input("Number of generations: ")), float(input("mutationRate: "))
        s, no, canv = self._s.GA(self._ofile, popSize, generations, mutationRate, self._root)
        print("fitness: {} after {} generations".format(s.getFitness(), no))
        if canv is not None:
            tk.mainloop()
        self._root = tk.Tk()

        return s

    def _hc(self):

        # i = int(input("nr simulari"))
        generations, mutationRate = int(input("Number of iterations: ")), float(input("mutationRate: "))
        # suma = 0
        # for _ in range(i):
        s, no, canv = self._s.HC(self._ofile, generations, mutationRate, self._root)
        print("fitness: {} after {} iterations".format(s.getFitness(), no))
        # suma += s.getFitness()
        # self._root.destroy()
        if canv is not None:
            tk.mainloop()
        self._root = tk.Tk()
        # print("media fitness: {} ".format(suma/i))
        return s

    def _valid(self):
        ret = self._s.Validate()
        if ret is not None:
            print("Invalid sudoku file, invalid number at line:{}  column:{}".format(ret[0], ret[1]))
            return self._getResponse()


    def _getFilePath(self, typef="r"):
        try:
            path = input("relative path to the {} file:".format("input" if typef == "r" else "output")+("(default is \"final.txt\")" if typef == "w" else ""))
            if path == "exit":
                return None
            elif path == "":
                path = "final.txt"
            with open(path, typef) as _:
                pass
            return path
        except FileNotFoundError:
            print("INVALID FILE PATH OR NOT EXISTING FILE!!")
            print("try again?(Y/n)")
            if self._getResponse():
                return self._getFilePath()
            else:
                return None

    def _getAlg(self):
        algorithm = input("choose algorithm (greedy / dfs / GA / HC)")
        if algorithm.upper() not in ("EXIT", "GREEDY", "DFS", "GA", "HC"):
            print("invalid algorithm !!")
            print("try again?(Y/n)")
            if self._getResponse():
                return self._getAlg()
            else:
                return None
        else:
            return algorithm.upper()

    def _getResponse(self):
        response = input()
        if response == "" or response[0] == "Y" or response[0] == 'y':
            return True
        elif response[0] == "n" or response[0] == "N":
            return False

        else:
            print("invalid option!!")
            return self._getResponse()