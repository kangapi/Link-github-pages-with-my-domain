import subprocess
import typer

app = typer.Typer()

@app.command()
def add(sub_domain: str, repo_name: str):
    subprocess.run(["python3", "add-link.py", sub_domain, repo_name])

@app.command()
def remove(sub_domain: str, repo_name: str):
    subprocess.run(["python3", "remove-link.py", sub_domain, repo_name])


if __name__ == "__main__":
    app()
