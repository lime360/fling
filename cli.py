import datetime
import click
from webring import create_db, list_all_sites, insert_site

@click.group()
def app():
    pass

@click.command()
def init():
    create_db()

@click.command()
def list_sites():
    sites = list_all_sites()
    for name, url, owner, added in sites:
        click.echo(f"{name} ({url}) by {owner} - added on {added}")

@click.command()
@click.argument("name")
@click.argument("url")
@click.argument("owner")
def insert(name, url, owner):
    date = datetime.datetime.now(datetime.timezone.utc).isoformat()
    insert_site(name, url, owner, date)

app.add_command(init)
app.add_command(list_sites)
app.add_command(insert)

if __name__ == '__main__':
    app()