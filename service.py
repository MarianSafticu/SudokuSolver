import os
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
