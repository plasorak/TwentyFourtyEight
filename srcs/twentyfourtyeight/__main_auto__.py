from .TwentyFourtyEight import Direction, ReturnCode, Model, Displayer
from rich.console import Console
import copy as cp
import random as rand

def main():
    console = Console()
    model = Model(console)
    display = Displayer(model, console)
    display.show()
    rc = ReturnCode.Success
    directions = [Direction.Up,
                  Direction.Down,
                  Direction.Left,
                  Direction.Right]
    
    weights = [0.05, 0.45, 0.45, 0.05]
    counter = 0
    while rc == ReturnCode.Success or rc == ReturnCode.NotMoved:
        direction = rand.choices(population=directions, weights=weights)[0]
        rc = model.move(direction)
        if rc != ReturnCode.NotMoved:
            display.show()
    console.print(f"[bold red]Automate lost on \"{rc}\"![/bold red]")

if __name__ == "__main__":
    main()
