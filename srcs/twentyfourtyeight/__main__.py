from .TwentyFourtyEight import Direction, ReturnCode, Model, Displayer
from rich.console import Console
import copy as cp


def main():
    console = Console()
    model = Model(console)
    display = Displayer(model, console)
    display.show()
    while True:
        ipt = input("up (w), down (s), left (a), right (d), undo (u), quit (q): ")
        play_on = ReturnCode.Unknown
        if   ipt == 'q': break
        elif ipt == 'w': play_on = model.move(Direction.Up   )
        elif ipt == 's': play_on = model.move(Direction.Down )
        elif ipt == 'a': play_on = model.move(Direction.Left )
        elif ipt == 'd': play_on = model.move(Direction.Right)
        elif ipt == 'u': model.undo()
        else:
            console.print("[bold red]Invalid input![/bold red]")
            continue
        if play_on == ReturnCode.NoMoreMove:
            console.print("[bold red]You lost![/bold red]")
            break
        if play_on == ReturnCode.Success:
            display.show()


if __name__ == "__main__":
    main()
