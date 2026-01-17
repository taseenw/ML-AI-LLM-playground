import typer

app = typer.Typer(no_args_is_help=True)

@app.command()
def tester():
    print("jot")

@app.command()
def tester2():
    print("jot2")

@app.command(name="eval-run")
def evailrun():
    print("we in here")
