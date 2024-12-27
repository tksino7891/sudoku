"""Module to solve sudoku."""

# coding:utf-8
import tkinter
from enum import Enum


class SolveStatus(Enum):
    NUMBER_GIVEN = 1
    SOLVED = 2
    NOT_SOLVED = 3
    NO_ANSWER = 4


def get_row_from_index(index: int) -> int:
    """Get row number from index."""
    return int(index / 9)


def get_column_from_index(index: int) -> int:
    """Get column number."""
    return index - int(index / 9) * 9


def get_block_number_from_index(index: int) -> int:
    """Get block number from index."""
    row = get_row_from_index(index)
    column = get_column_from_index(index)
    return int(row / 3) * 3 + int(column / 3)


def get_index_from_row_column(row: int, column: int) -> int:
    """Get index from row_column."""
    return row * 9 + column


def get_index_from_row_column_in_block(block: int, row: int, column: int) -> int:
    """Get index from row and column in block."""
    r1 = int(block / 3) * 3 + row
    c1 = (block % 3) * 3 + column
    return get_index_from_row_column(r1, c1)


class CellInfo:
    """Container for cell info."""
    def __init__(self):
        self.answer = None
        self.available_number = [True for item in range(9)]
        self.solve_status = SolveStatus.NOT_SOLVED.value


class SudokuSolver:
    """Sudoku solver."""
    def __init__(self):
        self.cell_info = [CellInfo() for item in range(81)]

    def set_given_number(self, index, number):
        self.cell_info[index].answer = number
        self.cell_info[index].solve_status = SolveStatus.NUMBER_GIVEN.value

    def solve(self):
        self.check_available_number()
        self.fill_answer_if_only_one_number_available_in_cell()
        self.fill_answer_if_only_one_location_available_in_row()
        self.fill_answer_if_only_one_location_available_in_column()
        self.fill_answer_if_only_one_location_available_in_block()
        self.check_cell_with_no_answer()

    def check_available_number(self):
        """Check available number for each cell."""
        for k in range(81):
            if self.cell_info[k].answer is not None:
                number = self.cell_info[k].answer
                # Set cell in same row not available for this number.
                row = get_row_from_index(k)
                for column in range(9):
                    index = get_index_from_row_column(row, column)
                    self.cell_info[index].available_number[number - 1] = False
                # Set cell in same column not available for this number.
                column = get_column_from_index(k)
                for row in range(9):
                    index = get_index_from_row_column(row, column)
                    self.cell_info[index].available_number[number - 1] = False
                # Set cell in same block not available for this number.
                block = get_block_number_from_index(k)
                for r in range(3):
                    for c in range(3):
                        index = get_index_from_row_column_in_block(block, r, c)
                        self.cell_info[index].available_number[number - 1] = False

    def fill_answer_if_only_one_number_available_in_cell(self):
        for k in range(81):
            if self.cell_info[k].solve_status == SolveStatus.NOT_SOLVED.value:
                count_available_number = 0
                for i in range(9):
                    if self.cell_info[k].available_number[i] is True:
                        count_available_number += 1
                        possible_answer = i + 1
                if count_available_number == 1:
                    self.cell_info[k].answer = possible_answer
                    self.cell_info[k].solve_status = SolveStatus.SOLVED.value

    def fill_answer_if_only_one_location_available_in_row(self):
        for number_id in range(9):
            for row in range(9):
                num_available_location = 0
                for column in range(9):
                    index = get_index_from_row_column(row, column)
                    if self.cell_info[index].answer == number_id + 1:
                        # The number checking is already set as result.
                        num_available_location = None
                        break
                    if self.cell_info[index].available_number[number_id] is True:
                        num_available_location += 1
                        possible_column_location = column
                if num_available_location == 0:
                    print(f"Number {number_id + 1} cannot be located in row {row}.")
                elif num_available_location == 1:
                    index = get_index_from_row_column(row, possible_column_location)
                    self.cell_info[index].answer = number_id + 1
                    self.cell_info[index].solve_status = SolveStatus.SOLVED.value

    def fill_answer_if_only_one_location_available_in_column(self):
        for number_id in range(9):
            for column in range(9):
                num_available_location = 0
                for row in range(9):
                    index = get_index_from_row_column(row, column)
                    if self.cell_info[index].answer == number_id + 1:
                        # The number checking is already set as result.
                        num_available_location = None
                        break
                    if self.cell_info[index].available_number[number_id] is True:
                        num_available_location += 1
                        possible_row_location = row
                if num_available_location == 0:
                    print(f"Number {number_id + 1} cannot be located in column {column}.")
                elif num_available_location == 1:
                    index = get_index_from_row_column(possible_row_location, column)
                    self.cell_info[index].answer = number_id + 1
                    self.cell_info[index].solve_status = SolveStatus.SOLVED.value

    def fill_answer_if_only_one_location_available_in_block(self):
        for number_id in range(9):
            for block in range(9):
                num_available_location = 0
                for r in range(3):
                    if num_available_location is None:
                        break
                    for c in range(3):
                        index = get_index_from_row_column_in_block(block, r, c)
                        if self.cell_info[index].answer == number_id + 1:
                            # The number checking is already set as result.
                            num_available_location = None
                            break
                        if self.cell_info[index].available_number[number_id] is True:
                            num_available_location += 1
                            possible_r_location = r
                            possible_c_location = c
                if num_available_location == 0:
                    print(f"Number {number_id + 1} cannot be located in block {block}.")
                elif num_available_location == 1:
                    index = get_index_from_row_column_in_block(
                        block, possible_r_location, possible_c_location
                    )
                    self.cell_info[index].answer = number_id + 1
                    self.cell_info[index].solve_status = SolveStatus.SOLVED.value

    def check_cell_with_no_answer(self):
        for k in range(81):
            if self.cell_info[k].solve_status not in [SolveStatus.NUMBER_GIVEN.value,
                                                      SolveStatus.SOLVED.value]:
                count_available_number = 0
                for i in range(9):
                    if self.cell_info[k].available_number[i] is True:
                        count_available_number += 1
                if count_available_number == 0:
                    self.cell_info[k].solve_status = SolveStatus.NO_ANSWER.value


class SudokuGui:
    """GUI for sudoku solver."""

    def __init__(self):
        """Setup the class."""
        self.main_frame = tkinter.Tk()
        self.main_frame.title("Sudoku program")
        self.main_frame.geometry("700x1000")
        self.label01 = tkinter.Label(self.main_frame, text="Please input problem")
        self.label01.pack(pady=0)

        # Create input form-----from here
        self.frame01 = tkinter.Frame(self.main_frame)
        self.frame01.pack(pady=10)
        self.input_frame = []
        for k in range(9):
            self.input_frame.append(tkinter.Frame(self.frame01))
            self.input_frame[k].grid(
                row=int(k / 3), column=k - 3 * int(k / 3), padx=3, pady=3
            )

        self.input_box = []
        for k in range(81):
            self.input_box.append(
                tkinter.Entry(
                    self.input_frame[get_block_number_from_index(k)],
                    width=2,
                    font=("Helevetica", 22),
                )
            )
            self.input_box[k].grid(row=get_row_from_index(k), column=get_column_from_index(k))
            self.input_box[k].insert(tkinter.END, k + 1)
            self.input_box[k].bind("<FocusOut>", self.solve_problem)
        # Create input form---- end here

        self.button01 = tkinter.Button(self.main_frame, text="Clear value")
        self.button01.bind("<Button-1>", self.delete_entry_value)
        self.button01.pack(pady=10)

        self.button02 = tkinter.Button(self.main_frame, text="solve problem")
        self.button02.bind("<Button-1>", self.solve_problem)
        self.button02.pack(pady=10)

        self.label02 = tkinter.Label(self.main_frame, text="Print answer")
        self.label02.pack(pady=10)

        # Create show answer form -----from here
        self.frame02 = tkinter.Frame(self.main_frame)
        self.frame02.pack(pady=10)
        self.output_frame = []
        for k in range(9):
            self.output_frame.append(tkinter.Frame(self.frame02))
            self.output_frame[k].grid(
                row=int(k / 3), column=k - 3 * int(k / 3), padx=3, pady=3
            )

        self.output_label = []
        for k in range(81):
            self.output_label.append(
                tkinter.Label(
                    self.output_frame[get_block_number_from_index(k)],
                    width=5,
                    height=3,
                    bg="white",
                    font=("Helevetica", 8),
                )
            )
            self.output_label[k].grid(
                row=get_row_from_index(k), column=get_column_from_index(k), padx=1, pady=1
            )
        # Create show answer form -----end here

        self.main_frame.mainloop()

    def set_answer_text(self, k):
        """Print answer."""
        out_put_text = ""
        if self.sudoku_solver.cell_info[k].solve_status == SolveStatus.NUMBER_GIVEN.value:
            out_put_text = self.sudoku_solver.cell_info[k].answer
            self.output_label[k].configure(
                text=out_put_text,
                width=2,
                height=1,
                fg="#0000ff",
                font=("Helevetica", 22),
            )
        elif self.sudoku_solver.cell_info[k].solve_status == SolveStatus.SOLVED.value:
            out_put_text = self.sudoku_solver.cell_info[k].answer
            self.output_label[k].configure(
                text=out_put_text,
                width=2,
                height=1,
                fg="#000000",
                font=("Helevetica", 22),
            )
        elif self.sudoku_solver.cell_info[k].solve_status == SolveStatus.NO_ANSWER.value:
            out_put_text = "N/A"
            self.output_label[k].configure(
                text=out_put_text,
                width=3,
                height=1,
                fg="#ff0000",
                font=("Helevetica", 18),
            )
        else:
            for m in range(9):
                if self.sudoku_solver.cell_info[k].available_number[m] is True:
                    out_put_text = out_put_text + str(m + 1) + " "
                else:
                    out_put_text = out_put_text + "  "

                if m - int(m / 3) * 3 == 2:
                    out_put_text = out_put_text + "\n"
            self.output_label[k].configure(
                text=out_put_text,
                width=5,
                height=3,
                fg="#000000",
                font=("Helevetica", 8),
            )

    def delete_entry_value(self, event):
        """Delete entry."""
        for k in range(len(self.input_box)):
            self.input_box[k].delete(0, tkinter.END)

    def solve_problem(self, event):
        """Solve problem."""
        self.sudoku_solver = SudokuSolver()
        # Read problem
        for k in range(len(self.input_box)):
            if self.input_box[k].get() == "":
                pass
            else:
                read_number = int(self.input_box[k].get())
                if read_number > 9 or read_number < 1:
                    pass
                else:
                    self.sudoku_solver.set_given_number(k, read_number)

        # Solve problem
        self.sudoku_solver.solve()

        # Print answers
        for k in range(len(self.input_box)):
            self.set_answer_text(k)


if __name__ == "__main__":
    SudokuGui()
