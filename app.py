import typer
import pysolr
import os

# command line interface object
cli = typer.Typer()

SOLR_PATH = 'http://localhost:8983/solr/techproducts'

# SOLR predefined commands
SOLR_START_SCHEMALESS = 'cd $SOLR_HOME && ./solr start -e schemaless'
SOLR_CREATE_COLLECTION = "cd $SOLR_HOME && ./solr create -c %s -d sample_techproducts_configs -n %s_configs"
SOLR_STOP_ALL = 'cd $SOLR_HOME && ./solr stop -all'

# create solr client instance
# set always_commit to True to update immediately the indexes
solr = pysolr.Solr(SOLR_PATH, always_commit=True)

# check if solr is running
#solr.ping()

# create collection with sample_techproducts_configs 
# these configs support all datatypes and fileformats already
@cli.command()
def create(collection_name: str):
    start_solr_default()

    typer.echo(f'\n\n######### solr is running, now create collection with the name: {collection_name} #########\n\n')

    
    values = (collection_name, collection_name)
    os.system(SOLR_CREATE_COLLECTION %values)

    typer.echo(f'\n\n######### collection created, now add some files ;) #########\n\n')

# starting up solr if it is not already running (on default port 8983)
def start_solr_default():
    typer.echo('######### starting solr... #########')
    
    # start solr
    os.system(SOLR_START_SCHEMALESS)

@cli.command()
def start(collection_name: str, stop_all: bool = False):
    if stop_all:

    typer.echo('######### starting solr... #########')
    os.system('cd $SOLR_HOME && ./solr start -e slides')

@cli.command()
def add_folder(path: str):
    typer.echo(f'add folder @, {path}')

# curl 'http://localhost:8983/solr/techproducts/update/extract?literal.id=doc1&uprefix=ignored_&commit=true' -F "myFile=@example/exampledocs/solr-word.pdf"
@cli.command()
def add_file(path: str):
    typer.echo(f'add file @, {path}')

# curl "http://localhost:8983/solr/techproducts/select?q=Invariant" 
@cli.command()
def search(query: str):
    typer.echo(f'search for: {query}')

    results = solr.search(query)
    typer.echo("Saw {0} result(s).".format(len(results)))
    for result in results:
        typer.echo("The title is '{0}'.".format(result))

if __name__ == '__main__':
    cli()