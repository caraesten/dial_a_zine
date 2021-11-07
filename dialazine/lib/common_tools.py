
def index_header(include_linebreaks=True):
    linebreak_char = ''
    if include_linebreaks:
        linebreak_char = '\n'
    return linebreak_char + "     [ INDEX ]     " + linebreak_char

def index_item_string(option, title, author, include_linebreaks=True):
    linebreak_char = ''
    if include_linebreaks:
        linebreak_char = '\n'
    return linebreak_char + ("%s > %s < ...by %s" % (option, title, author)) + linebreak_char
