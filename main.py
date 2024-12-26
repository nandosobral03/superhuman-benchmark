from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def print_menu():
    title = Text("Main Menu", style="bold cyan")
    menu_text = Text.assemble(
        "\n1. ", ("Reaction Time Test", "green"),
        "\n2. ", ("Sequence Memory", "green"),
        "\n3. ", ("Chimp Test", "green"),
        "\n4. ", ("Aim Trainer", "green"),
        "\n5. ", ("Number Memory", "green"),
        "\n6. ", ("Verbal Memory", "green"),
        "\n0. ", ("Exit", "red")
    )

    console.print(Panel(menu_text, title=title, border_style="cyan"))
    return console.input("[cyan]Enter your choice:[/cyan] ")

if __name__ == "__main__":
    from reaction_time_test import main as reaction_main
    from sequence_memory import main as sequence_main
    from chimp_test import main as chimp_main
    from aim_trainer_test import main as aim_trainer_main
    from number_memory import main as number_memory_main
    from verbal_memory import main as verbal_memory_main

    console.print("[bold blue]Welcome to the Automation Tools[/bold blue]")

    while True:
        choice = print_menu()

        if choice == "1":
            console.print("[yellow]Starting Reaction Time Test...[/yellow]")
            reaction_main()
        elif choice == "2":
            console.print("[yellow]Starting Sequence Memory Test...[/yellow]")
            sequence_main()
        elif choice == "3":
            console.print("[yellow]Starting Chimp Test...[/yellow]")
            chimp_main()
        elif choice == "4":
            console.print("[yellow]Starting Aim Trainer...[/yellow]")
            aim_trainer_main()
        elif choice == "5":
            console.print("[yellow]Starting Number Memory...[/yellow]")
            number_memory_main()
        elif choice == "6":
            console.print("[yellow]Starting Verbal Memory...[/yellow]")
            verbal_memory_main()
        elif choice == "0":
            console.print("[bold red]Goodbye![/bold red]")
            break
        else:
            console.print("[bold red]Invalid choice. Please try again.[/bold red]")
