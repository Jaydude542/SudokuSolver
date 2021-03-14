import tkinter as tk
from time import sleep
sudoku_board = [[0,0,0,0,0,0,0,0,0],
                [0,2,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,3,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,8,0,0,6,0,0,0]]
memo = [None]

class GUI(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.frame_list = []
        self.button_list = []
        self.button_locations = []
        # used to create a pattern
        self.color_change = True
        self.pattern = ("red","blue")
        self.pack()
        self.create_widgets()
    def create_widgets(self):
        # frame that contains all of the grid frames
        self.main_frame = tk.Frame(master=self,width=1000,height=1000,padx=5,pady=5)
        self.main_frame.pack(side="top")
        # button to start sudoku
        self.start_button = tk.Button(master=self,width=20,height=3,bg="green",command=self.start_sudoku,text="START")
        self.start_button.pack(side="bottom")
        # slider to control speed of sudoku
        self.speed_slider = tk.Scale(master=self,orient="horizontal", from_=0, to=10)
        self.speed_slider.pack(side='top')
        self.speed_slider.set(5)
        # create gui of sudoku board
        self.create_frames()
        self.caculate3x3ButtonLocations()
        self.create_buttons()
    def create_frames(self):
        # creating the 3x3 grids that will store the sudoku board and storing them in the frame_list
        for r in range(3):
            for c in range(3):
                frame = tk.Frame(master=self.main_frame, width=500,height=500,padx=5,pady=5)
                frame.grid(row=r,column=c)
                # simple bool switch to create a pattern on the frames
                if self.color_change:
                    frame["bg"] = self.pattern[0]
                    self.color_change = False
                else:
                    frame["bg"] = self.pattern[1]
                    self.color_change = True
                self.frame_list.append(frame)
    def create_buttons(self):
        # the index that every button is on
        index = 0
        for frame in self.frame_list:
            # putting 9 buttons in each frame in the frame_list in a 3x3 grid
            for r in range(3):
                for c in range(3):
                    button = tk.Button(master=frame, width=3, height=3)
                    button.grid(row=r,column=c)
                    self.button_list.append(button)
                    self.update_widgets(index)
                    index+=1
    # this function creates a list of where all the 3x3 square numbers are in the sudoku_list. (kinda hard to explain)
    def caculate3x3ButtonLocations(self):
        row_start,col_start,row,col = 0,0,0,0
        while len(self.button_locations) <= 80:
            # when 3 rows of 3x3 squares are located and stored, it moves to the next row
            if col_start == 9:
                # set the column back to zero to start a the beginning
                col_start = 0
                # move to the next set of 3 3x3 squares
                row_start+=3
            # starts off at the designated row
            row=row_start
            for i in range(row,row+3):
                # starts off at the designated column
                col=col_start
                # add 3 to the row to jump to the next row in the sudoku_board
                row+=3
                for j in range(col,col+3):
                    self.button_locations.append((i,j))
                    # add 3 to the col to jump to the next column in the sudoku_board
                    col+=3
            # move to the next square in the 3 3x3 squares
            col_start+=3
    def update_widgets(self,index):
        # grab the correct location from the index provided
        r,c = self.button_locations[index]
        # if empty spot at row-column
        if sudoku_board[r][c] == 0:
            # set it to a empty space
            self.button_list[index]["text"] = " "
            return
        # otherwise set it to the number in the sudoku_board at row-column
        self.button_list[index]["text"] = sudoku_board[r][c] 
    # changes color of current button
    def change_button_color(self,index,color):
        # reset all button colors
        self._reset_button_color()
        # if placement succesful
        if color=="green": self.button_list[index-1]["bg"] = "green"
        # else if placement unsuccesful
        elif color=="red": self.button_list[index-1]["bg"] = "red"
    def _reset_button_color(self):
        for button in self.button_list:
            button["bg"] = "white"
    def start_sudoku(self):
        self.start_button.destroy()
        self.sudoku_solver(sudoku_board)
    def get_correct_button(self,index):
        r,c = self.button_locations[index]
        return ((9*r)+c)+1

    def sudoku_solver(self,sudoku_board):
        # find the next open space that isnt a number
        row,column = find_next_open(sudoku_board)
        # base=case: if end of sudoku 
        if row == None:
            return True
        # to control speed of sudoku
        sleep(self.speed_slider.get()/10)
        # update GUI
        self.master.update()
        # exploration for loop
        for i in range(1,10):
            # checks if every number (1-9) is valid
            if valid_position(row,column,i,sudoku_board):
                # if it's valid, change the spot to the valid number
                sudoku_board[row][column] = i
                # change button-color at row-column index to green since valid number placement
                self.change_button_color(self.get_correct_button((row*9)+column),"green")
                # loops over all numbers, and updates them
                for i in range(81):
                    self.update_widgets(i)
                # recursion call - if it dosen't return true (meaning that the number was not correct), it backtracks to the number that was last persumed valid 
                if self.sudoku_solver(sudoku_board):
                    return True
            # changes current number to zero because it wasn't valid
            sudoku_board[row][column] = 0
        # if the sudoku board cannot be solved
        return False


def find_next_open(sudoku_board):
    for row in range(9):
        for col in range(9):
            if sudoku_board[row][col] == 0:
                return (row,col) # next empty space
    return (None,None) # no spaces are left empty
# return false if number at row-column position is not valid accoring to sudoku's rules
def valid_position(row,column,num,sudoku_board):
    # tests if it is in horizontal plane
    for col in range(9):
        if sudoku_board[row][col] == num:
            return False
    # tests if it is in verticle plane
    for r in range(9):
        if sudoku_board[r][column] == num:
            return False
    # throw away the remainder and multiply by 3 to get start of row and column
    row_start = ((row//3)*3) 
    col_start = ((column//3)*3)
    # tests if in 3x3 square
    for r in range(row_start, row_start+3):
        for col in range(col_start, col_start+3):
            if sudoku_board[r][col] == num:
                return False

    return True

def main():

    root = tk.Tk()
    sudoku_gui = GUI(root)
    sudoku_gui.mainloop()

if __name__ == '__main__':
    main()