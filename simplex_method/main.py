from fractions import Fraction
import copy
import argparse
file = open("1.txt","r")
data = file.read().split("\n")
data = [i.split(" ") for i in data]
for i in range(len(data)):
    for j in range(len(data[i])):
        data[i][j] = float(data[i][j])
class Matrix:
    def __init__(self,data):
        self.obj = data[0][0]
        self.obj_func = data[1]
        self.original_obj_func = None
        self.add_original_obj_func = None
        self.matrix_x = int(data[2][0])
        self.matrix_y = int(data[2][1])
        self.add_matrix_y = None
        self.matrix_obj = [data[i][int(data[2][1])+1] for i in range(3,int(data[2][0])+3)]
        self.target = [data[i][int(data[2][1])] for i in range(3,int(data[2][0])+3)]
        self.matrix = [i[:int(data[2][1])] for i in data[3:int(data[2][0])+3]]
        self.add_obj_func = None
        self.stage = 1
        self.step = 1
    
    def standard(self):
        for idx,value in enumerate(self.matrix_obj):
            if(value == 2):
                self.matrix_obj[idx] = 0
                for idy,row in enumerate(self.matrix):
                    x = 0.0
                    if(idx == idy):
                        x = -1.0
                    self.matrix[idy].append(x)
                self.obj_func.append(0.0)
                self.matrix_y += 1
            elif(value == 1):
                self.matrix_obj[idx] = 0
                for idy,row in enumerate(self.matrix):
                    x = 0.0
                    if(idx == idy):
                        x = 1.0
                    self.matrix[idy].append(x)
                self.obj_func.append(0.0)
                self.matrix_y += 1
    def col_index(self):
        index = [[i,-1] for i in range(self.matrix_x)]
        for i in range(self.matrix_x):
            for j in range(self.matrix_y):
                if(self.matrix[i][j] == 1):
                    flag = 1
                    for k in range(self.matrix_x):
                        if(self.matrix[k][j]!=0 and k!=i):
                            flag = 0
                    if(flag):
                        index[i][1] = j
                        break
        return index
    
    def cal_sigma(self,index):
        update_target = []
        for i in range(self.matrix_y):
            total = Fraction(0)
            for j in range(self.matrix_x):
                total += Fraction(self.obj_func[index[j][1]])*Fraction(self.matrix[j][i])
            outcome = Fraction(self.obj_func[i])-total
            update_target.append(outcome)
        return update_target
    
    def find_replace_col(self):
        max_col = -1
        col_idx = -1
        for col in range(self.matrix_y):
            if(self.obj_func[col] > Fraction(max_col)):
                max_col = self.obj_func[col]
                col_idx = col
        return col_idx
    
    def find_replace_row(self,col):
        row_idx = -1
        min_row = 10000
        for row in range(self.matrix_x):
            if(self.matrix[row][col]<=0):
                continue
            elif(self.target[row]/self.matrix[row][col]<min_row):
                min_row = self.target[row]/self.matrix[row][col]
                row_idx = row
        return row_idx
            
    
    def judge(self):#flag=1表示找到最优解 flag=0表示还没有找到最优解 flag=2表示有无界解
        flag = 1
        for col in range(self.matrix_y):
            if(self.obj_func[col]>0):
                flag = 2
                for row in range(self.matrix_x):
                    if(self.matrix[row][col]>0):
                        flag = 0
                        break
        return flag
    
    def move_forward(self,row_idx,col_idx):
        k = Fraction(self.matrix[row_idx][col_idx])
        self.target[row_idx] = Fraction(self.target[row_idx])/k
        for col in range(self.matrix_y):
            self.matrix[row_idx][col] = Fraction(self.matrix[row_idx][col])/k
        for row in range(self.matrix_x):
            if(row == row_idx):
                continue
            else:
                factor = -Fraction(self.matrix[row][col_idx])/Fraction(self.matrix[row_idx][col_idx])
                for col in range(self.matrix_y):
                    self.matrix[row][col] += factor*self.matrix[row_idx][col]
                self.target[row] += factor*self.target[row_idx]
                        
    def show(self):
        print("Stage{}, step{}".format(self.stage,self.step))
        print("------------------------------------------------")
        print("C               |",end='')
        for i in self.obj_func:
            print("{} ".format(int(i)),end = '')
        print('\n')
        print("------------------------------------------------")
        print("Cb  |  Xb  | B  | ",end='')
        for i in range(len(self.obj_func)):
            print("x{} ".format(int(i+1)),end = '')
        print('\n')
        print("------------------------------------------------")
        index = self.col_index()
        for i in range(self.matrix_x):
            print("{} | x{} | {} | ".format(self.obj_func[index[i][1]],index[i][1]+1,self.target[i]),end='')
            for j in range(self.matrix_y):
                print("{} ".format(self.matrix[i][j]),end='')
            print("\n")
        print("------------------------------------------------")
        update_target = self.cal_sigma(index)
        print("Sigma          |",end='')
        for i in update_target:
            print(" {}  ".format(i),end='')
        self.obj_func = update_target
        print("\n\n")
        col = self.find_replace_col()
        row = self.find_replace_row(col)
        flag = self.judge()
        self.step += 1
        return (flag,row,col)
    
    def frac_wise(self):
        for row in range(self.matrix_x):
            for col in range(self.matrix_y):
                self.matrix[row][col] = Fraction(self.matrix[row][col])
            self.target[row] = Fraction(self.target[row])
            
    def show_result(self,limited,obj_func):
        index = self.col_index()
        result = [0 for i in range(self.matrix_y)]
        for i in index:
            result[i[1]] = self.target[i[0]]
        if(limited):
            print("x*=[",end='')
            for i in result:
                print("{} ".format(i),end='')
            print("]")
        z = 0
        for i in range(len(obj_func)):
            z += obj_func[i]*result[i]
        print("z*={}\n".format(z))
            
        
    def start(self):
        self.standard()
        index = self.col_index()
        add = False
        for i in index:
            if(i[1] == -1):
                add = True
        if(add):
            self.add_obj_func = copy.deepcopy(self.obj_func)
            self.original_obj_func = copy.deepcopy(self.obj_func)
            self.add_matrix_y = self.matrix_y
            for col in range(self.matrix_y):
                self.obj_func[col] = 0
            for row in range(self.matrix_x):
                if(index[row][1]==-1):
                    for i in range(self.matrix_x):
                        if(i == row):
                            self.matrix[i].append(1.0)
                        else:
                            self.matrix[i].append(0.0)
                    self.obj_func.append(-1)
                    self.matrix_y += 1
            self.frac_wise()
            self.add_original_obj_func = copy.deepcopy(self.obj_func)
            flag, row, col = self.show()
            while(flag == 0):
                self.move_forward(row,col)
                (flag,row,col) = self.show()
            index = self.col_index()
            for i in range(self.add_matrix_y,self.matrix_y):
                for k in index:
                    if(k[0]==i and k[1]!=-1):
                        print("The problem doesn’t have a feasible solution.")
                        exit(0)
            self.stage += 1
            self.step = 1
            print("The problem has feasible solution.")
            print("Result of Stage 1:")
            self.show_result(True,self.add_original_obj_func)
            
        
        if(add):
            self.obj_func = self.add_obj_func
            self.matrix_y = self.add_matrix_y
        flag, row, col = self.show()
        while(flag == 0):
            self.move_forward(row,col)
            (flag,row,col) = self.show()    
        if(flag == 2):
            print("The optimal solution of the problem is unbounded.")
            print("x* is unbounded")       
            print("z* is unbounded")
        else:
            for col in range(self.matrix_y):
                for i in self.col_index():
                    if(self.obj_func[col] == 0 and col != i[1]):
                        print("The number of optimal solution is unlimited.")
                        self.show_result(False,self.original_obj_func)
                        exit(0)
            print("The optimal solution of the problem is")
            self.show_result(True,self.original_obj_func)

if(__name__ == '__main__'):
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument(
      "--file",
      type=str,
      default="test.txt",
      help="the path to th test file")
    args, unparsed = parser.parse_known_args()
    file = open(args.file,"r")
    data = file.read().split("\n")
    data = [i.split(" ") for i in data]
    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = float(data[i][j])
    m = Matrix(data)
    m.start()
