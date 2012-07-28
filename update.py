import sys
import os, urllib
import time
import zipfile
from HTTP4Store import HTTP4Store


def download(url,file,force=0):
	# Check the file exists on disk
	if os.path.exists(file):
		filemtime = os.path.getmtime(file)
		print "Checking file headers"
		connection = urllib.urlopen(url)
		urlmtime = time.mktime(connection.info().getdate('last-modified'))
		if (urlmtime > filemtime) or force:
			print "Fetching updated file..."
			# urllib.urlretrieve(url,file) :::::::::::::::::::::::::::::::::::::REMEMBER TO PUT BACK IN :::::::::::::	
		else:
			sys.exit("File unchanged. Use --force to force update")
	else:
		print "Downloading file..."
		urllib.urlretrieve(url,file)

def unzip(file):
	print "Extracting file..."
	archive = zipfile.ZipFile("R4DOutputsData.zip",'r')
	archive.extract('R4DOutputsData.txt')
	os.rename('R4DOutputsData.txt','R4DOutputsData.rdf')

def upload(file):
	print "Preparing file to upload..."
	store = HTTP4Store('http://localhost:8088')
	file = open("R4DOutputsData.rdf")
	data = file.read()
	print "Storing data..."
	response = store.add_graph("http://www.dfid.gov.uk/r4d/",data,"xml")
	print "Operation complete. Response status " + str(response.status)

if __name__ == '__main__':

	# Provide means to force updates
	if len(sys.argv) > 1 and sys.argv[1] == '--force':
		force = 1
	else:
		force = 0

	download("http://www.dfid.gov.uk/R4D/RDF/R4DOutputsData.zip","R4DOutputsData.zip",force)
	unzip(file)
	upload('R4DOutputsData.rdf')