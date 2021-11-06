## How to run

To run locally, run server.py as a python file e.g. from the root directory

`python3 dialazine/server.py`

To access locally, run

`telnet localhost 23`

(or equivalent with another telnet client)

in server.py, change CONTENT_FOLDER to "example_issue" to see example

## Zine Structure

In the index.json, the "hello" message is the filepath within the issue folder for what is first displayed,

Then the contents is a list with each article, taking the "title" and "author" for the index, and the "directory" is the folder within the issue folder that contains the article pages - the pages must be called `1.txt`, `2.txt` etc. and will automatically display in that order
