#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3
import datetime
import click
import csv

def now():
	return datetime.datetime.now().isoformat()

CATEGORIES = [
	'code',
	'write',
	'check',
	'plan',
	'organize',
	'derive',
	'research'
	]

class DataStore(object):
	"""docstring for DataStore"""
	def __init__(self, filename):
		self.filename = filename
		reader = csv.DictReader(open(self.filename, 'r'))
		self.keys = reader.fieldnames
		self.writer = csv.DictWriter(open(self.filename, 'a'), fieldnames=self.keys)

	def add_entry(self, row):
		self.writer.writerow(row)

datastore = DataStore('/Users/koren/timelog.csv')

@click.group()
def cli():
    pass

@click.command()
@click.argument('project')
@click.argument('category', type=click.Choice(CATEGORIES))
@click.option('-m', 'comment', default='', help='Comment')
def start(project, category, comment):
	row = dict(event='start', project=project, category=category, comment=comment, time_stamp=now())
	datastore.add_entry(row)

@click.command()
@click.argument('project')
@click.option('-m', 'comment', default='', help='Comment')
def stop(project, comment):
	row = dict(event='stop', project=project, comment=comment, time_stamp=now())
	datastore.add_entry(row)

@click.command()
@click.argument('project')
@click.argument('category', type=click.Choice(CATEGORIES))
@click.argument('hours', default=1.0)
@click.option('-m', 'comment', default='', help='Comment')
def add(project, category, comment, hours):
	row = dict(event='add', project=project, category=category, comment=comment, time_stamp=now(), hours=hours)
	datastore.add_entry(row)

cli.add_command(start)
cli.add_command(stop)
cli.add_command(add)

if __name__ == '__main__':
	cli()