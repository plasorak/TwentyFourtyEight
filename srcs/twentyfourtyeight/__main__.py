from .TwentyFourtyEight import Direction, Model, Displayer
from rich.console import Console
import copy as cp


def main():
    console = Console()
    model = Model(console)
    display = Displayer(model, console)
    display.show()
    while(True):
         ipt = input("up (w), down (s), left (a), right (d), undo (u), quit (q): ")
         if   ipt == 'q': break
         elif ipt == 'w': model.move(Direction.Up   )
         elif ipt == 's': model.move(Direction.Down )
         elif ipt == 'a': model.move(Direction.Left )
         elif ipt == 'd': model.move(Direction.Right)
         elif ipt == 'u': model.undo()
         else:
             console.print("[bold red]Invalid input![/bold red]")
             continue
         display.show()


if __name__ == "__main__":
    main()
