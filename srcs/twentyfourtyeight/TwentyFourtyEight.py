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


class ReturnCode(Enum):
    Unknown=0
    Success=1
    NotMoved=2
    NoMoreMove=3
    ImpossibleInsert=4


class Model():

    grid = []
    FOUR_PROB = 0.1
    size = None
    console = None
    score = 0
    max_numb = 0
    
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
        self._update_score()


    def _update_score(self) -> NoReturn:
        self.score = 0
        self.max_numb = 0
        for row in self.grid:
            for numb in row:
                if numb is not None:
                    self.score += numb
                    if numb > self.max_numb:
                        self.max_numb = numb
        
    def _new_random_number(self) -> ReturnCode:
        done = ReturnCode.ImpossibleInsert
        if not self._has_empty():
            return ReturnCode.ImpossibleInsert

        MAX_TRIES = 10000
        itry=0
        while done != ReturnCode.Success:
            row = rand.randint(0, self.size-1)
            col = rand.randint(0, self.size-1)
            two_or_four = rand.choices(population=[2,4], weights=[9.,1.])[0]
            done = self._insert_number_on_empty(row, col, two_or_four)

            itry += 1
            if itry>MAX_TRIES:
                break

        return done


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

    def _insert_number_on_empty(self, r:int, c:int, number:int) -> ReturnCode:
        if r<0 or c<0 or r>=self.size or c>=self.size:
            raise RuntimeError(f"Wrong index row: {r}, column: {c}, size: {self.size}")
        if not self.grid[r][c]:
            self._assign_number_on_grid(r, c, number)
            return ReturnCode.Success
        else:
            return ReturnCode.ImpossibleInsert

    def _has_number(self, array:[int]) -> bool:
        for i in array:
            if i is not None:
                return True
        return False


    def shift(self, array:[int]) -> [int]:
        if not self._has_number(array):
            return array

        new_array = []
        # get rid of none
        for i in range(len(array)):
            if array[i] is not None:
                new_array.append(array[i])

        # sum the same numbers
        new_new_array = []
        for i in range(len(new_array)):
            if i<len(new_array)-1 and new_array[i] == new_array[i+1]:
                new_new_array.append(new_array[i]+new_array[i+1])
                new_array[i+1] = None
            elif new_array[i] is not None:
                new_new_array.append(new_array[i])

        # resize array
        new_new_new_array = [None]*self.size
        for i in range(len(new_new_array)):
            new_new_new_array[i] = new_new_array[i]
        return new_new_new_array

    
    def can_move(self) -> ReturnCode:
        grid_cp = cp.deepcopy(self.grid)
        if self._move(Direction.Up, grid_cp) == ReturnCode.Success:
            return ReturnCode.Success
        
        grid_cp = cp.deepcopy(self.grid)
        if self._move(Direction.Down, grid_cp) == ReturnCode.Success:
            return ReturnCode.Success
        
        grid_cp = cp.deepcopy(self.grid)
        if self._move(Direction.Left, grid_cp) == ReturnCode.Success:
            return ReturnCode.Success
        
        grid_cp = cp.deepcopy(self.grid)
        if self._move(Direction.Right, grid_cp) == ReturnCode.Success:
            return ReturnCode.Success

        return ReturnCode.NoMoreMove

    
    def move(self, direction:Direction) -> ReturnCode:
        rc = self._move(direction, self.grid)
        self._update_score()
        
        if rc != ReturnCode.Success:
            return rc
        rc = self._new_random_number()

        if rc != ReturnCode.Success:
            return rc
        rc = self.can_move()

        return rc

    
    def _move(self, direction:Direction, grid) -> ReturnCode:
        mvmt = False
        size = len(grid)
        size_range = range(size)
        
        if   direction == Direction.Up:
            for i in size_range:
                column = [None]*size

                for j in size_range:
                    column[j] = grid[j][i]

                new_column = self.shift(column)

                if new_column != column:
                    mvmt = True

                for j in size_range:
                     grid[j][i] = new_column[j]


        elif direction == Direction.Down:
            for i in size_range:
                column = [None]*size

                for j in size_range:
                    column[j] = grid[j][i]

                column = column[::-1]
                new_column = self.shift(column)

                if new_column != column:
                    mvmt = True

                for j in size_range:
                     grid[j][i] = new_column[self.size-j-1]


        elif direction == Direction.Left:
            for i in size_range:
                row = grid[i]

                new_row = self.shift(row)

                if new_row != row:
                    mvmt = True

                grid[i] = new_row


        elif direction == Direction.Right:
            for i in size_range:
                row = cp.deepcopy(grid[i][::-1])

                new_row = self.shift(row)

                if new_row != row:
                    mvmt = True

                grid[i] = cp.deepcopy(new_row[::-1])

        if not mvmt:
            return ReturnCode.NotMoved

        return ReturnCode.Success


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
        self.console.print(f'[blue]Score: {self.model.score}, Max {self.model.max_numb}[/blue]')
