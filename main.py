from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def print_menu():
    title = Text("Main Menu", style="bold cyan")
    menu_text = Text.assemble(
        "\n1. ", ("Reaction Time Test", "green"),
        "\n2. ", ("Sequence Memory", "green"),
        "\n0. ", ("Exit", "red")
    )

    console.print(Panel(menu_text, title=title, border_style="cyan"))
    return console.input("[cyan]Enter your choice:[/cyan] ")

if __name__ == "__main__":
    from reaction_time_test import main as reaction_main
    from sequence_memory import main as sequence_main

    console.print("[bold blue]Welcome to the Automation Tools[/bold blue]")

    while True:
        choice = print_menu()

        if choice == "1":
            console.print("[yellow]Starting Reaction Time Test...[/yellow]")
            reaction_main()
        elif choice == "2":
            console.print("[yellow]Starting Sequence Memory Test...[/yellow]")
            sequence_main()
        elif choice == "0":
            console.print("[bold red]Goodbye![/bold red]")
            break
        else:
            console.print("[bold red]Invalid choice. Please try again.[/bold red]")
