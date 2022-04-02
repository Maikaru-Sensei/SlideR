from ast import IsNot
import typer
import os
import requests
import json

# command line interface object
cli = typer.Typer()

# SOLR predefined commands
SOLR_START_SCHEMALESS = 'cd $SOLR_HOME && ./solr start -e schemaless'
SOLR_CREATE_COLLECTION = "cd $SOLR_HOME && ./solr create -c %s -d sample_techproducts_configs -n %s_configs -shards %d -replicationFactor %d"
SOLR_STOP_ALL = 'cd $SOLR_HOME && ./solr stop -all'

SOLR_ADD_FILE = 'cd $SOLR_HOME && curl http://localhost:8983/solr/slides/update/extract?literal.id=doc1&uprefix=ignored_&commit=true -F "myFile=@%s"'

# create collection with sample_techproducts_configs 
# these configs support all datatypes and fileformats already
@cli.command()
def create(name: str = typer.Option
                        (..., "--name", "-n", help="name of the new collection"),
            shards: int = typer.Option
                        (..., "--shards", "-s", help="number of shards"),
            replicas: int = typer.Option
                        (..., "--replicas", "-r", help="number of replicas per shard")):
    
    start_solr_default()

    typer.echo(f'\n\n######### solr is running, now create collection with the name: {name} #########\n\n')
    
    values = (name, name, shards, replicas)

    os.system(SOLR_CREATE_COLLECTION %values)

    typer.echo(f'\n\n######### collection created, now add some files ;) #########\n\n')

# starting up solr if it is not already running (on default port 8983)
def start_solr_default():
    typer.echo('######### starting solr... #########')
    
    # start solr
    os.system(SOLR_START_SCHEMALESS)

@cli.command()
def start(stop_all: bool = typer.Option(
                ..., 
                prompt="Do you want to stop other nodes?",
                help="stops all current running Solr nodes")):
    
    if stop_all:
        typer.echo('######### stopping all other solr nodes ... #########')
        os.system(SOLR_STOP_ALL)

    typer.echo('######### starting Solr ... #########')
    os.system(SOLR_START_SCHEMALESS)

@cli.command()
def add_folder(path: str):
    typer.echo(f'add folder @, {path}')

# curl 'http://localhost:8983/solr/techproducts/update/extract?literal.id=doc1&uprefix=ignored_&commit=true' -F "myFile=@example/exampledocs/solr-word.pdf"
@cli.command()
def add_file(path: str):

    if os.path.isfile(path):
        typer.echo(f'add file @, {path},test')
        os.system(SOLR_ADD_FILE %path)
        typer.echo(f'Added')

@cli.command()
def search(collection_name: str = typer.Option
                        (..., "--collection", "-c", help="name of the collection"),
            query: str = typer.Option
                        (..., "--query", "-q", help="search phrase")):

    q = 'http://localhost:8983/solr/%s/select?hl=true&q=%s~1"'
    
    typer.echo(f'command: {q %(collection_name, query)}')

    r = requests.get(q %(collection_name, query))

    if "ERROR 404" in r.text:
        typer.echo(f"collection: {collection_name} not found, try again!")
        return
        
    res = json.loads(r.text)
    num_found = res['response']['numFound']
    hl = res['highlighting']

    typer.echo(f'documents found: {num_found}\n')
    if (num_found > 0):
        max_len = len(max(hl, key=len))

        print("{:<90} {:<10}".format('Document','Pages'))

        for i in hl:
            print("{:<90} {:<10}".format(i, "{4, 5, 8}"))
        
    

if __name__ == '__main__':
    cli()