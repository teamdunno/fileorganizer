import os
import shutil
import mimetypes
import time
from pathlib import Path
from rich.console import Console

def move_file(file_path, dest_dir, file_name, console):
    try:
        # Move the file to the corresponding directory
        shutil.move(file_path, dest_dir / file_name)
        console.print(f"[bold green]{file_name}[/] -> [blue]{dest_dir.name}[/]")
    except Exception as e:
        console.print(f"[bold red]Failed to move {file_name}: {e}[/]")

def categorize_files(cleanup_folder, console):
    for file in os.listdir(cleanup_folder):
        file_path = cleanup_folder / file

        if file_path.is_file():
            mime_type, encoding = mimetypes.guess_type(file)

            if mime_type:
                category = mime_type.split("/")[0]
                category_dir = cleanup_folder / category.capitalize()

                if not category_dir.exists():
                    category_dir.mkdir()

                move_file(file_path, category_dir, file, console)
            else:
                unknown_dir = cleanup_folder / "Unknown"

                if not unknown_dir.exists():
                    unknown_dir.mkdir()

                move_file(file_path, unknown_dir, file, console)

def main():
    console = Console()

    cleanup_folder = console.input("[green]Clean up path:[/] ")
    cleanup_folder = Path(cleanup_folder) if cleanup_folder else Path.cwd()

    if cleanup_folder.exists() and cleanup_folder.is_dir():
        categorize_files(cleanup_folder, console)
    else:
        console.print("[bold red]Folder doesn't exist or the folder isn't a directory.[/]")

    console.print("[bold yellow]Team[/][green]Dunno[/]'s file organizer")
    console.print("[bold yellow]Version 1.0[/]")
    console.print("[bold yellow]If you see a directory called Plain, it means the file HAS an extension, MIME just has no idea what file type it is.\nUnknown just means the MIME type was empty.[/]")
    time.sleep(0.5)

if __name__ == "__main__":
    main()
