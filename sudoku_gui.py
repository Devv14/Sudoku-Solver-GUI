# sudoku game board

from solver import *
import numpy as np
import random
import tkinter as tk
import time
import pyautogui


class Sudoku:
    
    board = [[0 for i in range(9)] for j in range(9)]
    hint_board = []
    
    def __init__(self,masterr):
        self.masterr = masterr
        self.entry_list = [[" " for i in range(9)] for j in range(9)]
        
        # - - Timer - -  #
        self.start = time.time()
        # - - run handle - - #
        self.running = False

        # -- Visual Control -- #
        self.visualize = True
        self.select_time = 0
        self.green_time = 0.05
        self.red_time = 0.04
        self.bot_time = 0


    def current_pos(self,x,y):
        self.posx = x
        self.posy = y
        self.update_entrys(x,y)
        
        
    def update_entrys(self,x,y):
        if not self.running:
            self.running = True  
            for i in range(9):
                for j in range(9):
                    value = str(self.entry_list[i][j].get()).removeprefix(" ")
                    try:
                        self.entry_list[i][j].config(bg="#ffffff")
                        self.entry_list[i][j].delete(0,tk.END)
                        self.entry_list[i][j].insert(0,' {}'.format(value[0]))
                    except: pass
            self.entry_list[x][y].config(bg="#bbdefb")
            self.running = False

    def Clear_all(self):
        if not self.running:
            self.running = True
            Sudoku.hint_board.clear()
            for i in range(9):
                for j in range(9):
                    self.entry_list[i][j].config(bg="#ffffff")
                    self.entry_list[i][j].delete(0,tk.END)
                    self.entry_list[i][j].insert(0,"")
            self.running = False

    def write_on_file(self,board):
        with open("log.txt",'w+') as file:
            # file.truncate()
            file.write("{}".format(board))
        file.close()

    def hint_board_(self):
        with open("log.txt",'r') as file:
            Sudoku.hint_board = eval(file.read())
        file.close()

    def Genrate_sudoku(self,dif):
        if not self.running:
            self.running = True

            _used_ = []
            Sudoku.board = [[0 for i in range(9)] for j in range(9)]
            i = 0
            while len(_used_) < 9 and i < 9:
                num = random.randint(1,9)
                if num not in _used_:

                    Sudoku.board[0][i] = num
                    i += 1
                    _used_.append(num)

            # solve the genrated sudoku
            solve(Sudoku.board)
            self.write_on_file(Sudoku.board)
            self.masterr.update()
            
            # Remove Numbers from boards
            for k in range(dif):
                Sudoku.board[random.randint(0,8)][random.randint(0,8)] = 0

            self.masterr.update()
            # inserting values to GUI
            self.running = False
            self.Clear_all()
            self.running = True
            for i in range(9):
                for j in range(9):
                    if Sudoku.board[i][j] == 0:
                        self.entry_list[i][j].insert(0,"")
                    else:
                        self.entry_list[i][j].insert(0," {}".format(Sudoku.board[i][j]))
            
            # Sudoku.hint_board = Sudoku.board.copy()
            # solve(Sudoku.hint_board)
            self.hint_board_()      #   Hint Board

            self.masterr.update()
            self.running = False
            

    def Genrate_sudoku_board(self):
        p = 0
        for i in range(9):
            q = 0
            for j in range(9):
                
                if (p+1)%4==0 and p!=0:
                    l1 = tk.Label(self.masterr)
                    l1.grid(row=p, column=q)
                    p += 1 
                if (q+1)%4==0 and q!=0:
                    l1 = tk.Label(self.masterr, text=" ")
                    l1.grid(row=p, column=q)
                    q += 1
                
                entry =  tk.Entry(self.masterr, width=2, font= ("Helvetica",30,"bold"), bg="#ffffff", relief="ridge")
                entry.grid(row=p, column=q)
                entry.bind("<Button-1>",lambda e = None,x=i,y=j:self.current_pos(x=x,y=y))
                entry.insert(0,"")
                q += 1 
                try:
                    self.entry_list[i][j] = entry                       
                except: pass
                
            p += 1


        self.New_game_b = tk.Label(text='New Game', bg="#76a8e2", fg="white")
        self.New_game_b.grid(row=0, column=11, padx=5)

        self.Easy_b = tk.Button(text='Easy', bg="#4a90e2", fg="white", relief='flat', activebackground="white", width=8, command= lambda:self.Genrate_sudoku(60))
        self.Easy_b.grid(row=1, column=11, padx=5)

        self.Hard_b = tk.Button(text='Hard', bg="#4a90e2", fg="white", relief='flat', activebackground="white", width=8, command=lambda: self.Genrate_sudoku(100))
        self.Hard_b.grid(row=2, column=11, padx=5)
        
        self.Hint_b = tk.Button(text='Hint', bg="#4a90e2", fg="white", relief='flat', activebackground="white", width=8, command=self.Hint)
        self.Hint_b.grid(row=4, column=11, padx=5)
        
        self.Clear_b = tk.Button(text='Clear All', bg="#4a90e2", fg="white", relief='flat', activebackground="white", width=8, command=self.Clear_all)
        self.Clear_b.grid(row=5, column=11, padx=5)

        self.Auto_Solve_b = tk.Button(text='Visual Solve', bg="#4a90e2", fg="white", relief='flat', activebackground="white", width=8,command=self.Visual_solve)
        self.Auto_Solve_b.grid(row=6, column=11, padx=5)

        self.Speed_Solve_b = tk.Button(text='Speed Solve', bg="#4a90e2", fg="white", relief='flat', activebackground="white", width=8,command=self.Speed_solve)
        self.Speed_Solve_b.grid(row=8, column=11, padx=5)
    
        self.Bot_b = tk.Button(text='BOT', bg="#4a90e2", fg="white", relief='flat', activebackground="white", width=8,command=self.Bot)
        self.Bot_b.grid(row=9, column=11, padx=5)
    


    def Hint(self):
        try:
            self.entry_list[self.posx][self.posy].delete(0,tk.END)
            self.entry_list[self.posx][self.posy].insert(0,' {}'.format(Sudoku.hint_board[self.posx][self.posy]))
        except: pass


    def Visual_solve(self):
        self.visualize = True
        self.Auto_solve_update()

    def Speed_solve(self):
        self.visualize = False
        self.Auto_solve_update()

    def Auto_solve_update(self):
        if not self.running:
            self.running = True
            Sudoku.board = [[0 for i in range(9)] for j in range(9)]
            
            for i in range(9):
                for j in range(9):    
                    value = str(self.entry_list[i][j].get()).removeprefix(" ")
                    if value == "":
                        Sudoku.board[i][j] = 0 
                    else:
                        Sudoku.board[i][j] = int(value)
            
            print("!Get\t",np.matrix(Sudoku.board))
            
            self.Auto_solve(Sudoku.board)
            self.running = False
            

    def green_bg(self,x,y,n):
        self.entry_list[x][y].config(bg="#BEFD7F")
        self.entry_list[x][y].config(fg='black')
        self.entry_list[x][y].delete(0,tk.END)
        self.entry_list[x][y].insert(0,' {}'.format(n))
        if self.visualize:
            time.sleep(self.green_time)
            self.masterr.update()

    def select_green(self,x,y):
        self.entry_list[x][y].config(bg="#BEFD7F")
        self.masterr.update()

    def red_bg(self,x,y):
        if self.visualize:
            self.entry_list[x][y].config(bg="#FD7F7F")
            # self.entry_list[x][y].delete(0,tk.END)
            # self.entry_list[x][y].insert(0,' {}'.format(0))
            time.sleep(self.red_time)
            self.masterr.update()
            
    def selected_bg(self,x,y,n):
        if self.visualize:
            self.entry_list[x][y].config(fg='white')
            self.entry_list[x][y].delete(0,tk.END)
            self.entry_list[x][y].insert(0,' {}'.format(n))
            time.sleep(self.select_time)
            self.masterr.update()

    def Auto_solve(self,board):
        # print("$\t",np.matrix(board))
        
        find = find_empty(board)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1,10):
            self.selected_bg(row,col,i)
            self.red_bg(row,col)
            if valid(board, i, (row, col)):
                board[row][col] = i
                self.green_bg(row,col,i)
                
                if self.Auto_solve(board):
                    return True

                board[row][col] = 0
                self.red_bg(row,col)
                
        return False    

    def Bot(self):
        if self.running == False:
            self.running = True
            if pyautogui.confirm(title='Confirm', text="Do you want to activate Bot in 5 seconds", buttons=['Yes', 'No']) == "Yes":
                time.sleep(5)
                for i in range(9):
                    for j in range(9):
                        if (i+1)%2!=0:
                            self.select_green(i,j)
                            pyautogui.press('{}'.format(Sudoku.board[i][j]))
                            pyautogui.press('right')       
                        elif (i+1)%2==0:
                            self.select_green(i,8-j)
                            pyautogui.press('{}'.format(Sudoku.board[i][8-j]))
                            pyautogui.press('left')
                        time.sleep(self.bot_time)
                        
                    pyautogui.press('down')
            self.running = False

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("530x492")
    root.maxsize(530,492)
    root.minsize(530,492)
    root.title("MY Sudoku Game | ©NN")
    try:
        root.iconbitmap("sudoku-ico.ico")
    except: pass
    game = Sudoku(root)
    game.Genrate_sudoku_board()
    
    root.mainloop()
