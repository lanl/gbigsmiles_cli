import typer

from gbigcli.generation import check_entry, get_stochastic_samples

application = typer.Typer()
application.command("check")(check_entry)
application.command("get")(get_stochastic_samples)

if __name__ == "__main__":
    application()