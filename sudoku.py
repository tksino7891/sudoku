# coding:utf-8
import tkinter


class Sudoku:
    def __init__(self):
        self.Main_frame = tkinter.Tk()
        self.Main_frame.title("Sudoku program")
        self.Main_frame.geometry("700x900")

        self.output_answer = [0 for i in range(81)]
        self.solve_status = [9 for i in range(81)]  # 1-9: posible number to input, -1: applied problem
        self.can_input_number = [[1 for i in range(9)] for j in range(81)]

        self.Label01 = tkinter.Label(self.Main_frame, text = "Please input problem") 
        self.Label01.pack(pady = 0)

        # Create input form-----from here
        self.Frame01 = tkinter.Frame(self.Main_frame)
        self.Frame01.pack(pady = 10)
        self.Input_frame = []
        for k in range(9):
            self.Input_frame.append(tkinter.Frame(self.Frame01))
            self.Input_frame[k].grid(row=int(k/3), column= k-3*int(k/3) , padx = 3 , pady = 3)

        self.InputBox = []
        for k in range(81):
            self.InputBox.append(tkinter.Entry(self.Input_frame[self.get_block(k)], width=3, font = ("Helevetica",16)))
            self.InputBox[k].grid(row= self.get_row(k) , column = self.get_column(k))
            self.InputBox[k].insert(tkinter.END,k+1)
            self.InputBox[k].bind("<FocusOut>", self.SolveProblem)
        # Create input form---- end here

        self.Button01 = tkinter.Button(self.Main_frame, text = "Clear value") 
        self.Button01.bind("<Button-1>", self.DeleteEntryValue)
        self.Button01.pack(pady = 10)

        self.Button02 = tkinter.Button(self.Main_frame, text = "solve problem")
        self.Button02.bind("<Button-1>",self.SolveProblem)
        self.Button02.pack(pady = 10)

        self.Label02 = tkinter.Label(self.Main_frame, text = "Print answer") 
        self.Label02.pack(pady = 10)

        # Create show answer form -----from here
        self.Frame02 = tkinter.Frame(self.Main_frame)
        self.Frame02.pack(pady = 10)
        self.Output_frame = []
        for k in range(9):
            self.Output_frame.append(tkinter.Frame(self.Frame02))
            self.Output_frame[k].grid(row=int(k/3), column= k-3*int(k/3) , padx = 3 , pady = 3)

        self.OutputLabel = []
        for k in range(81):
            self.OutputLabel.append(tkinter.Label(self.Output_frame[self.get_block(k)], width=5, height=3, bg = "white", font = ("Helevetica",8)))
            self.OutputLabel[k].grid(row= self.get_row(k) , column = self.get_column(k) , padx = 1 , pady = 1)
        # Create show answer form -----end here

        self.Main_frame.mainloop()

    def mod(self, a,b):
        return a - int(a/b)*b

    def get_row(self, k):
        return int(k/9)

    def get_column(self, k):
        return k-int(k/9)*9

    def get_block(self, k):
        row = self.get_row(k)
        column = self.get_column(k)
        return int(row/3)*3 + int(column/3)

    def get_index(self, row,column):
        return row*9+column

    def get_index_block(self, block,row,column):
        r1 = int(block/3)*3 + row
        c1 = self.mod(block,3)*3 + column
        return self.get_index(r1 , c1)

    def check_available_number(self):
        # Check unable cases
        for k in range(81):
            if self.solve_status[k] == -1 or self.solve_status[k] == 1:
                num = self.output_answer[k]
                for row in range(9):
                    index = self.get_index(row, self.get_column(k))
                    if k != index and self.solve_status[index] != -1:
                        if self.can_input_number[index][num-1] == 1:
                            self.can_input_number[index][num-1] = 0
                # Check no same number in same line
                for column in range(9):
                    index = self.get_index(self.get_row(k),column)
                    if k != index and self.solve_status[index] != -1:
                        if self.can_input_number[index][num-1] == 1:
                            self.can_input_number[index][num-1] = 0

                # Check no same number in same block
                for r1 in range(3):
                    for c1 in range(3):
                        index = self.get_index_block(self.get_block(k),r1,c1)
                        if k != index and self.solve_status[index] != -1:
                            if self.can_input_number[index][num-1] == 1:
                                self.can_input_number[index][num-1] = 0

        # Summarize determinant sells
        num_solved = 0
        for k in range(81):
            if self.solve_status[k] != -1:
                self.solve_status[k] = 0
                for n in range(9):
                    if self.can_input_number[k][n] == 1:
                        self.solve_status[k] = int(self.solve_status[k] + 1)
                if self.solve_status[k] == 1:
                    for n in range(9):
                        if self.can_input_number[k][n] == 1:
                            self.output_answer[k] = n+1
                    
            if self.solve_status[k] == -1 or self.solve_status[k] == 1:
                num_solved = num_solved +1
        return num_solved

    def check_limit_cells(self):
        # Check where a number can be set
        for num in range(9):

            # column direcrtion
            for row in range(9):
                avalable_place = 0
                for column in range(9):
                    if self.can_input_number[self.get_index(row,column)][num] == 1:
                        avalable_place = avalable_place +1
                if avalable_place == 1:
                    for column in range(9):
                        index = self.get_index(row,column)
                        if self.can_input_number[index][num] == 1 and self.solve_status[index] != -1:
                            for n in range(9):
                                self.can_input_number[index][n] = 0
                            self.can_input_number[index][num] = 1
            # row direction
            for column in range(9):
                avalable_place = 0
                for row in range(9):
                    if self.can_input_number[self.get_index(row,column)][num] == 1:
                        avalable_place = avalable_place +1
                if avalable_place == 1:
                    for row in range(9):
                        index = self.get_index(row,column)
                        if self.can_input_number[index][num] == 1 and self.solve_status[index] != -1:
                            for n in range(9):
                                self.can_input_number[index][n] = 0
                            self.can_input_number[index][num] = 1
            # Search in block
            for block in range(9):
                avalable_place = 0
                for row in range(3):
                    for column in range(3):
                        if self.can_input_number[self.get_index_block(block,row,column)][num] == 1:
                            avalable_place = avalable_place +1
                if avalable_place == 1:
                    for row in range(3):
                        for column in range(3):
                            index = self.get_index_block(block,row,column)
                            if self.can_input_number[index][num] == 1 and self.solve_status[index] != -1:
                                for n in range(9):
                                    self.can_input_number[index][n] = 0
                                self.can_input_number[index][num] = 1


        # Summarize determinant cells
        num_solved = 0
        for k in range(81):
            if self.solve_status[k] != -1:
                self.solve_status[k] = 0
                for n in range(9):
                    if self.can_input_number[k][n] == 1:
                        self.solve_status[k] = int(self.solve_status[k] + 1)
                if self.solve_status[k] == 1:
                    for n in range(9):
                        if self.can_input_number[k][n] == 1:
                            self.output_answer[k] = n+1
                    
            if self.solve_status[k] == -1 or self.solve_status[k] == 1:
                num_solved = num_solved +1
        return num_solved


    def print_answer(self, k):
        out_put_text = ""
        if self.solve_status[k] == -1:
            for m in range(9):
                if self.can_input_number[k][m] == 1:
                    out_put_text = str(m+1)
            self.OutputLabel[k].configure(text = out_put_text, width=2, height=1, fg = "#0000ff", font = ("Helevetica",22))
        elif self.solve_status[k] == 1:
            for m in range(9):
                if self.can_input_number[k][m] == 1:
                    out_put_text = str(m+1)
            self.OutputLabel[k].configure(text = out_put_text, width=2, height=1, fg = "#000000", font = ("Helevetica",22))
        elif self.solve_status[k] == 0:
            out_put_text = "N/A"
            self.OutputLabel[k].configure(text = out_put_text, width=3, height=1, fg = "#ff0000", font = ("Helevetica",18))
        else:
            for m in range(9):
                if self.can_input_number[k][m] == 1:
                    out_put_text = out_put_text + str(m+1) + " "
                else:
                    out_put_text = out_put_text + "  "

                if m-int(m/3)*3 == 2:
                    out_put_text = out_put_text + "\n"
            self.OutputLabel[k].configure(text = out_put_text, width=5, height=3, fg = "#000000", font = ("Helevetica",8))

    def DeleteEntryValue(self, event):
        # Delete entry
        for k in range(len(self.InputBox)):
            self.InputBox[k].delete(0, tkinter.END)

    def SolveProblem(self, event):
        # Initialize
        for k in range(81):
            self.output_answer[k] = 0
            self.solve_status[k] = 9
            for m in range(9):
                self.can_input_number[k][m] = 1
        # Read problem
        for k in range(len(self.InputBox)):
            if self.InputBox[k].get() == "":
                self.output_answer[k] = 0
            else:
                self.output_answer[k] = int(self.InputBox[k].get())
                if self.output_answer[k] > 9 or self.output_answer[k] < 1:
                    self.output_answer[k] = 0
                else:
                    self.solve_status[k] = -1
                    for m in range(9):
                        self.can_input_number[k][m] = 0
                    self.can_input_number[k][self.output_answer[k]-1] = 1

        # Solve probelm
        pre_solved_num=self.check_available_number()
        for k in range(81):
            self.check_limit_cells()
            solved_num = self.check_available_number()
            if pre_solved_num != solved_num:
                pre_solved_num = solved_num
            else:
                break

        # Print answers
        for k in range(len(self.InputBox)):
            self.print_answer(k)


if __name__ == '__main__':
    Sudoku()

