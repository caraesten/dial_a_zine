import json, os, string
from lib.common_tools import index_item_string
from lib.text_screen_reader import TextScreenReader
from lib.common_tools import index_header

class ContentsReader:
    def __init__(self, contents_file_path):
        self.issue_directory = os.path.dirname(contents_file_path)
        self.text_reader = TextScreenReader(self.issue_directory)
        contents_file = open(contents_file_path, 'r')
        self.contents_json = json.load(contents_file)
        self.verify_contents()

    def verify_contents(self):
        if not self.contents_json['hello']:
            raise Exception("Contents JSON requires a hello message")
    
    def hello_file_path(self):
        return self.contents_json['hello']

    def read_hello_file(self, wrap_returns=True):
        lines = self.text_reader.read_file_name(self.hello_file_path())
        if wrap_returns:
            return self._wrap_carriage_returns(lines)
        else:
            return lines
    
    def read_index_lines(self):
        index_lines = [index_header()]
        option_number = 1
        for index_item in self.read_story_object():
            index_lines.append(index_item_string(self._index_to_option(option_number), index_item['title'], index_item['author']))
            option_number += 1
        index_lines.append("\n(or X to quit!)\n")
        return self._wrap_carriage_returns(index_lines)

    def read_story_object(self, include_contents=False):
        index_list = []
        story_number = 1
        for index_item in self.contents_json['contents']:
            story_item = {
                'title': index_item['title'],
                'author': index_item['author'],
                'directory': index_item['directory'],
            }
            if include_contents:
                page_number = 1
                story_lines = self.read_story(story_number, page_number, wrap_returns=False)
                pages = []
                while len(story_lines) > 0:
                    pages.append(story_lines)
                    page_number += 1
                    story_lines = self.read_story(story_number, page_number, wrap_returns=False)
                story_item['contents'] = pages
            story_number += 1
            index_list.append(story_item)
        return index_list

    def read_story(self, story_number, page = 1, wrap_returns=True):
        if story_number > len(self.contents_json['contents']):
            return []
        story_obj = self.contents_json['contents'][story_number - 1]
        file_path = "%s/%s.txt" % (story_obj['directory'], page)
        
        if self.text_reader.does_file_exist(file_path):
            page_lines = self.text_reader.read_file_name(file_path)
            if wrap_returns:
                return self._wrap_carriage_returns(page_lines)
            else:
                return page_lines
        else:
            return []

    def _wrap_carriage_returns(self, lines_list):
        return [x + '\r' for x in lines_list]
    
    def map_input_to_numerical_index(self, input_string):
        try:
            return int(input_string)
        except ValueError:
            pass
        try:
            return 10 + string.ascii_uppercase[0:10].index(input_string)
        except ValueError:
            return -1

    def _index_to_option(self, input_index):
        if (input_index < 10):
            return input_index
        else:
            return string.ascii_uppercase[input_index - 10]

