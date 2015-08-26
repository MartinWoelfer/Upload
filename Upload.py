

# mainly copied from https://cherrypy.readthedocs.org/en/3.2.6/progguide/files/uploading.html
import mimetypes
import os
localDir = os.path.dirname(__file__) # current working directory
absDir = os.path.join(os.getcwd(), localDir) # os.getcwd() : Return a string representing the current working directory.
import cherrypy



class FileUpload(object):
    @cherrypy.expose
    def index(self):
        #Open the index webpage
        return open("index.html")

    def upload(self, myFile):
        out = """<html>
                <link rel="stylesheet" href="css/stylesheet.css">
	            <body>
	                <p id="output">
		                Size: %s kb<br />
		                filename: %s<br />
		                mime-type: %s
                    </p>
                </body>
                </html>"""
        # Although this just counts the file length, it demonstrates
        # how to read large files in chunks instead of all at once.
        # CherryPy reads the uploaded file into a temporary file;
        # myFile.file.read reads from that.
        size = 0
        whole_data = bytearray() # Neues Bytearray
        while True:
            data = myFile.file.read(8192) #8192 entsprechen 8 KiB
            whole_data += data # Save data chunks in ByteArray whole_data

            if not data:
                break
            size += len(data)

            written_file = open(myFile.filename, "wb") # open file in write bytes mode
            written_file.write(whole_data) # write file

        #Nach dem Uploaden wird Daten ueber das geuploadete File geschrieben
        return out % (size / 1000, myFile.filename, myFile.content_type)
    upload.exposed = True

conf = {'/css':
    {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': '/Users/DMS/PycharmProjects/untitled/css'
    }
}

if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    cherrypy.quickstart(FileUpload(), "/", config=conf)
else:
    # This branch is for the test suite; you can ignore it.
    cherrypy.tree.mount(FileUpload(), "/", config=conf)