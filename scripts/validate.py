import subprocess
import argparse
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import sys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_git_base_directory():
    result = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error: Not in a git repository or git not available.")
        sys.exit(1)
    return result.stdout.strip()

def run_command(command, print_output_on_fail=False):
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        if print_output_on_fail:
            print(result.stdout + result.stderr)
        return False, result.stdout + result.stderr
    return True, ''

def validate_file(file_path):
    print(f"Validating {file_path}...", end="", flush=True)
    mypy_passed, mypy_output = run_command(["mypy", file_path], print_output_on_fail=True)
    black_passed, black_output = run_command(["black", "-l", "120", "-S", "--check", file_path], print_output_on_fail=True)
    pyflakes_passed, pyflakes_output = run_command(["pyflakes", file_path], print_output_on_fail=True)
    if mypy_passed and black_passed and pyflakes_passed:
        print(" Pass")
        return True
    else:
        print(" Fail")
        if not mypy_passed:
            print(mypy_output)
        if not black_passed:
            print(black_output)
        if not pyflakes_passed:
            print(pyflakes_output)
        return False

def run_pytest(directory):
    print("Running pytest...", end="", flush=True)
    pytest_passed, pytest_output = run_command(["pytest", directory], print_output_on_fail=True)
    if pytest_passed:
        print(" Pass")
    else:
        print(" Fail\n", pytest_output)
        return False
    return True

def validate_directory(directory):
    all_checks_passed = True
    for file_path in Path(directory).rglob('*.py'):
        if not validate_file(str(file_path)):
            all_checks_passed = False
    return all_checks_passed and run_pytest(directory)

class EventHandler(FileSystemEventHandler):
    def __init__(self, directory):
        self.directory = directory

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.py'):
            clear_screen()
            validate_file(event.src_path)
            run_pytest(self.directory)

def watch_directory(directory):
    event_handler = EventHandler(directory)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()
    print("Watching for changes. Press Ctrl+C to stop.")
    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run validation tools and pytest on Python files in the backend directory.")
    parser.add_argument("--watch", action="store_true", help="Watch the directory for changes and rerun validation tools and pytest on changed files.")
    args = parser.parse_args()

    git_base_dir = get_git_base_directory()
    target_directory = os.path.join(git_base_dir, "story-viz/backend")

    if args.watch:
        watch_directory(target_directory)
    else:
        print("Running validation on all Python files in the directory...")
        all_checks_passed = validate_directory(target_directory)
        if not all_checks_passed:
            sys.exit(1)
