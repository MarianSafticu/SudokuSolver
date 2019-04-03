from Sudoku import sudoku

class Sudokup:
    def __init__(self, fname):
        self._fname = fname

    # read a sudoku from file and return a sudoku object
    def getS(self):
        with open(self._fname, "r") as f:
            line = f.readline(1000)
            nr = int(line)
            elems =[]
            for i in range(nr):
                elline = []
                for elm in f.readline().split(","):
                    elline.append(int(elm))
                elems.append(elline[:])
            s = sudoku(nr,elems)
            return s

    # write a sudoku to a new file
    def writeS(self, fname, S):
        with open(fname, "w") as f:
            f.write(str(S.getNr())+"\n")
            for i in S.getElems():
                for j in range(len(i)):
                    f.write(str(i[j]))
                    if j != (len(i)-1):
                        f.write(",")
                f.write("\n")
