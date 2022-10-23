# coding:utf-8


import tkinter
import math

Main_frame = tkinter.Tk()
Main_frame.title("Num place program")
Main_frame.geometry("700x900")

output_answer = [0 for i in range(81)]
solve_status = [9 for i in range(81)]  # 1-9: posible number to input, -1: applied problem
can_input_number = [[1 for i in range(9)] for j in range(81)]

def mod(a,b):
    return a - int(a/b)*b

def get_row(k):
    return int(k/9)

def get_column(k):
    return k-int(k/9)*9

def get_block(k):
    row = get_row(k)
    column = get_column(k)
    return int(row/3)*3 + int(column/3)

def get_index(row,column):
    return row*9+column

def get_index_block(block,row,column):
    r1 = int(block/3)*3 + row
    c1 = mod(block,3)*3 + column
    return get_index(r1 , c1)

def check_available_number():
    #不可条件探索
    for k in range(81):
        if solve_status[k] == -1 or solve_status[k] == 1:
            num = output_answer[k]
            #同じ行に同じ数字を入力できない
            for row in range(9):
                index = get_index(row,get_column(k))
                if k != index and solve_status[index] != -1:
                    if can_input_number[index][num-1] == 1:
                        can_input_number[index][num-1] = 0

            #同じ列に同じ数字を入力できない
            for column in range(9):
                index = get_index(get_row(k),column)
                if k != index and solve_status[index] != -1:
                    if can_input_number[index][num-1] == 1:
                        can_input_number[index][num-1] = 0

            #同じブロックに同じ数字を入力できない
            for r1 in range(3):
                for c1 in range(3):
                    index = get_index_block(get_block(k),r1,c1)
                    if k != index and solve_status[index] != -1:
                        if can_input_number[index][num-1] == 1:
                            can_input_number[index][num-1] = 0

    #値確定セル数を集計
    num_solved = 0
    for k in range(81):
        if solve_status[k] != -1:
            solve_status[k] = 0
            for n in range(9):
                if can_input_number[k][n] == 1:
                    solve_status[k] = int(solve_status[k] + 1)
            if solve_status[k] == 1:
                for n in range(9):
                    if can_input_number[k][n] == 1:
                        output_answer[k] = n+1
                
        if solve_status[k] == -1 or solve_status[k] == 1:
            num_solved = num_solved +1
    return num_solved

def check_limit_cells():
    #ある数字の入れられる限定セルを探索
    for num in range(9):

        #列方向探索
        for row in range(9):
            avalable_place = 0
            for column in range(9):
                if can_input_number[get_index(row,column)][num] == 1:
                    avalable_place = avalable_place +1
            if avalable_place == 1:
                for column in range(9):
                    index = get_index(row,column)
                    if can_input_number[index][num] == 1 and solve_status[index] != -1:
                        for n in range(9):
                            can_input_number[index][n] = 0
                        can_input_number[index][num] = 1
        #行方向探索
        for column in range(9):
            avalable_place = 0
            for row in range(9):
                if can_input_number[get_index(row,column)][num] == 1:
                    avalable_place = avalable_place +1
            if avalable_place == 1:
                for row in range(9):
                    index = get_index(row,column)
                    if can_input_number[index][num] == 1 and solve_status[index] != -1:
                        for n in range(9):
                            can_input_number[index][n] = 0
                        can_input_number[index][num] = 1
        #Block内探索
        for block in range(9):
            avalable_place = 0
            for row in range(3):
                for column in range(3):
                    if can_input_number[get_index_block(block,row,column)][num] == 1:
                        avalable_place = avalable_place +1
            if avalable_place == 1:
                for row in range(3):
                    for column in range(3):
                        index = get_index_block(block,row,column)
                        if can_input_number[index][num] == 1 and solve_status[index] != -1:
                            for n in range(9):
                                can_input_number[index][n] = 0
                            can_input_number[index][num] = 1


    #値確定セル数を集計
    num_solved = 0
    for k in range(81):
        if solve_status[k] != -1:
            solve_status[k] = 0
            for n in range(9):
                if can_input_number[k][n] == 1:
                    solve_status[k] = int(solve_status[k] + 1)
            if solve_status[k] == 1:
                for n in range(9):
                    if can_input_number[k][n] == 1:
                        output_answer[k] = n+1
                
        if solve_status[k] == -1 or solve_status[k] == 1:
            num_solved = num_solved +1
    return num_solved


def print_answer(k):
    out_put_text = ""
    if solve_status[k] == -1:
        for m in range(9):
            if can_input_number[k][m] == 1:
                out_put_text = str(m+1)
        OutputLabel[k].configure(text = out_put_text, width=2, height=1, fg = "#0000ff", font = ("Helevetica",22))
    elif solve_status[k] == 1:
        for m in range(9):
            if can_input_number[k][m] == 1:
                out_put_text = str(m+1)
        OutputLabel[k].configure(text = out_put_text, width=2, height=1, fg = "#000000", font = ("Helevetica",22))
    elif solve_status[k] == 0:
        out_put_text = "N/A"
        OutputLabel[k].configure(text = out_put_text, width=3, height=1, fg = "#ff0000", font = ("Helevetica",18))
    else:
        for m in range(9):
            if can_input_number[k][m] == 1:
                out_put_text = out_put_text + str(m+1) + " "
            else:
                out_put_text = out_put_text + "  "

            if m-int(m/3)*3 == 2:
                out_put_text = out_put_text + "\n"
        OutputLabel[k].configure(text = out_put_text, width=5, height=3, fg = "#000000", font = ("Helevetica",8))

def DeleteEntryValue(event):
    #エントリーの中身を削除
    for k in range(len(InputBox)):
        InputBox[k].delete(0, tkinter.END)

def SolveProblem(event):
    #値を初期化
    for k in range(81):
        output_answer[k] = 0
        solve_status[k] = 9
        for m in range(9):
            can_input_number[k][m] = 1
    #問題を読み取り
    for k in range(len(InputBox)):
        if InputBox[k].get() == "":
            output_answer[k] = 0
        else:
            output_answer[k] = int(InputBox[k].get())
            if output_answer[k] > 9 or output_answer[k] < 1:
                output_answer[k] = 0
            else:
                solve_status[k] = -1
                for m in range(9):
                    can_input_number[k][m] = 0
                can_input_number[k][output_answer[k]-1] = 1

    #問題を解く
    pre_solved_num=check_available_number()
    for k in range(81):
        check_limit_cells()
        solved_num = check_available_number()
        if pre_solved_num != solved_num:
            pre_solved_num = solved_num
        else:
            break

    #解答欄に出力
    for k in range(len(InputBox)):
        print_answer(k)

Label01 = tkinter.Label(Main_frame, text = "問題を入力してください。") 
Label01.pack(pady = 0)

#入力ボックスの作成-----ここから
Frame01 = tkinter.Frame(Main_frame)
Frame01.pack(pady = 10)
Input_frame = []
for k in range(9):
    Input_frame.append(tkinter.Frame(Frame01))
    Input_frame[k].grid(row=int(k/3), column= k-3*int(k/3) , padx = 3 , pady = 3)

InputBox = []
for k in range(81):
    InputBox.append(tkinter.Entry(Input_frame[get_block(k)], width=3, font = ("Helevetica",16)))
    InputBox[k].grid(row= get_row(k) , column = get_column(k))
    InputBox[k].insert(tkinter.END,k+1)
    InputBox[k].bind("<FocusOut>",SolveProblem)
#入力ボックスの作成-----ここまで

Button01 = tkinter.Button(Main_frame, text = "値をクリアする") 
Button01.bind("<Button-1>",DeleteEntryValue)
Button01.pack(pady = 10)

Button02 = tkinter.Button(Main_frame, text = "問題を解く")
Button02.bind("<Button-1>",SolveProblem)
Button02.pack(pady = 10)

Label02 = tkinter.Label(Main_frame, text = "解答を出力します。") 
Label02.pack(pady = 10)

#出力ボックスの作成-----ここから
Frame02 = tkinter.Frame(Main_frame)
Frame02.pack(pady = 10)
Output_frame = []
for k in range(9):
    Output_frame.append(tkinter.Frame(Frame02))
    Output_frame[k].grid(row=int(k/3), column= k-3*int(k/3) , padx = 3 , pady = 3)

OutputLabel = []
for k in range(81):
    OutputLabel.append(tkinter.Label(Output_frame[get_block(k)], width=5, height=3, bg = "white", font = ("Helevetica",8)))
    OutputLabel[k].grid(row= get_row(k) , column = get_column(k) , padx = 1 , pady = 1)
#出力ボックスの作成-----ここまで

Main_frame.mainloop()

