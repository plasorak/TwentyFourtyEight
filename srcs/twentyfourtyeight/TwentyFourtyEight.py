from typing import NoReturn
from enum import Enum
import random as rand
from rich.console import Console
from rich.table import Table
from rich import box
import copy as cp

class Direction(Enum):
    Up=1
    Down=2
    Left=3
    Right=4

class Model():

    grid = []
    FOUR_PROB = 0.1
    size = None
    console = None

    def __init__(self, console:Console, size:int = 4):
        self.console = console
        self.size = size
        one_row = []
        for _ in range(size):
            one_row.append(None)

        self.grid = []
        for _ in range(size):
            self.grid.append(cp.deepcopy(one_row))

        self._new_random_number()
        self._new_random_number()


    def _new_random_number(self) -> NoReturn:
        done = False
        while not done:
            row = rand.randint(0, self.size-1)
            col = rand.randint(0, self.size-1)
            two_or_four = rand.choices(population=[2,4], weights=[9.,1.])[0]
            done = self._insert_number_on_empty(row, col, two_or_four)


    def _has_empty(self) -> bool:
        for i in range(self.size):
            for j in range(self.size):
                if not self.grid[i][j]:
                    return True
        return False


    def _assign_number_on_grid(self, r:int, c:int, number:int) -> NoReturn:
        if r<0 or c<0 or r>=self.size or c>=self.size:
            raise RuntimeError(f"Wrong index row: {r}, column: {c}, size: {self.size}")
        self.grid[r][c] = number

    def _insert_number_on_empty(self, r:int, c:int, number:int) -> bool:
        if r<0 or c<0 or r>=self.size or c>=self.size:
            raise RuntimeError(f"Wrong index row: {r}, column: {c}, size: {self.size}")
        if not self.grid[r][c]:
            self._assign_number_on_grid(r, c, number)
            return True
        else:
            return False

    def _has_number(self, array:[int]) -> bool:
        for i in array:
            if i is not None:
                return True
        return False


    def shift(self, array:[int]) -> [int]:
        if not self._has_number(array):
            return array

        new_array = []
        print("array", array)
        # get rid of none
        for i in range(len(array)):
            if array[i] is not None:
                new_array.append(array[i])
        print("new_array", new_array)

        # sum the same numbers
        new_new_array = []
        for i in range(len(new_array)):
            if i<len(new_array)-1 and new_array[i] == new_array[i+1]:
                new_new_array.append(new_array[i]+new_array[i+1])
                new_array[i+1] = None
            elif new_array[i] is not None:
                new_new_array.append(new_array[i])
        print("new_new_array", new_new_array)

        # resize array
        new_new_new_array = [None]*self.size
        for i in range(len(new_new_array)):
            new_new_new_array[i] = new_new_array[i]
        print("new_new_new_array", new_new_new_array)
        return new_new_new_array

    def move(self, direction:Direction) -> NoReturn:
        if   direction == Direction.Up:
            for i in range(self.size):
                column = [None]*self.size
                for j in range(self.size):
                    column[j] = self.grid[j][i]
                column = self.shift(column)
                for j in range(self.size):
                     self.grid[j][i] = column[j]
        elif direction == Direction.Down:
            for i in range(self.size):
                column = [None]*self.size
                for j in range(self.size):
                    column[j] = self.grid[j][i]
                column = self.shift(column[::-1])
                for j in range(self.size):
                     self.grid[j][i] = column[self.size-j-1]
        elif direction == Direction.Left:
            for i in range(self.size):
                self.grid[i] = self.shift(self.grid[i])
        elif direction == Direction.Right:
            for i in range(self.size):
                array = cp.deepcopy(self.grid[i][::-1])
                array = self.shift(array)
                self.grid[i] = cp.deepcopy(array[::-1])
        self._new_random_number()

    def undo(self) -> NoReturn:
        pass


class Displayer():
    def __init__(self, model:Model, console:Console):
        self.model = model
        self.console = console

    def show(self) -> NoReturn:
        table = Table(box=box.ROUNDED, show_lines=True, show_header=False)
        for i in range(self.model.size):
            table.add_row(*[str(n) if n else "" for n in self.model.grid[i]])
        self.console.print(table)
