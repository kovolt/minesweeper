import ctypes
import random
import sys
from tkinter import Button, Label, messagebox

import settings


class Cell:
    all = []
    cell_count = settings.CELL_COUNT
    cell_count_label_object = None

    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_mine_candidate = False
        self.cell_btn_object = None
        self.x = x
        self.y = y

        # Append the object to the Cell.all list
        Cell.all.append(self)

    def create_btn_object(self, location):
        btn = Button(
            location,
            width=12,
            height=4,
        )
        btn.bind("<Button-1>", self.left_click_actions)
        btn.bind("<Button-2>", self.right_click_actions)
        self.cell_btn_object = btn

    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            bg="black",
            fg="white",
            text=f"Cells Left: {Cell.cell_count}",
            width=12,
            font=("", 30)
        )
        Cell.cell_count_label_object = lbl

    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounding_cells_mines_length == 0:
                for cell_obj in self.surrounding_cells:
                    cell_obj.show_cell()
            self.show_cell()
            # If Mines count is equal to Cells Left count, player wins game
            if Cell.cell_count == settings.MINES_COUNT:
                messagebox.showinfo("Game Over!", "Congratulations! You win!")

        # Cancel Left and Right click events if cell is already opened:
        self.cell_btn_object.unbind("<Button-1>")
        self.cell_btn_object.unbind("<Button-2>")

    def get_cell_by_axis(self, x, y):
        # Return a cell object based on the value of x, y
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def surrounding_cells(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y + 1)
        ]
        cells = [cell for cell in cells if cell is not None]
        return cells

    @property
    def surrounding_cells_mines_length(self):
        counter = 0
        for cell in self.surrounding_cells:
            if cell.is_mine:
                counter += 1
        return counter

    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(text=self.surrounding_cells_mines_length)
            # Replace the text of cell count label with remaining cell count
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text=f"Cells Left: {Cell.cell_count}"
                )
            # If this was a mine candidate: for safety, configure bg color to systemTransparent
            self.cell_btn_object.configure(highlightbackground="systemTransparent")
        # Mark the cell as opened (Use as last line of method)
        self.is_opened = True

    def show_mine(self):
        messagebox.showwarning("Game Over!", "Game Over! You clicked on a mine!")
        self.cell_btn_object.configure(highlightbackground="red")
        sys.exit()

    def right_click_actions(self, event):
        if not self.is_mine_candidate:
            self.cell_btn_object.configure(highlightbackground="orange")
            self.is_mine_candidate = True
        else:
            self.cell_btn_object.configure(highlightbackground="systemTransparent")
            self.is_mine_candidate = False

    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(Cell.all, settings.MINES_COUNT)
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"
