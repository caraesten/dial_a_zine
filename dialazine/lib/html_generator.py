import chevron
from pathlib import Path
from lib.common_tools import index_item_string, index_header
from lib.contents_reader import ContentsReader

class HtmlGenerator:
    def __init__(self, index_file_path, html_output_path, templates_path):
        self.contents_reader = ContentsReader(index_file_path)
        self.html_output_path = html_output_path
        self.templates_path = templates_path
        # TODO: this could be customizeable 
        self.index_url = "story_index.html"

    def write_zine_html(self):
        intro_text = self.contents_reader.read_hello_file(wrap_returns=False)
        zine_dict = self.contents_reader.read_story_object(include_contents=True)

        intro_template_path = f'{self.templates_path}/intro.html'
        index_template_path = f'{self.templates_path}/story_index.html'
        story_template_path = f'{self.templates_path}/story_page.html'

        Path(self.html_output_path).mkdir(parents=True, exist_ok=True)

        self._write_intro_html(intro_template_path, intro_text)
        self._write_index_html(index_template_path, zine_dict)
        self._write_stories_html(story_template_path, zine_dict)
    
    def _write_intro_html(self, intro_template_path, intro_text):
        intro_html = ''
        html_text = [self._htmlize_whitespace(x) for x in intro_text]
        with open(intro_template_path, 'r') as f:
            intro_html = chevron.render(f, {'intro_lines': html_text, 'index_url': self.index_url})
        file_output_path = self.html_output_path + "/index.html"
        print("Writing intro page to: %s" % file_output_path)
        with open(file_output_path, 'w') as f:
            f.write(intro_html)
    
    def _write_index_html(self, index_template_path, zine_dict):
        index_html = ''
        with open(index_template_path, 'r') as f:
            index_items = []
            for index in range(len(zine_dict)):
                item = zine_dict[index]
                first_page_link = "%s/1.html" % item['directory']
                item_dict = {
                    'title_text': index_item_string(index, item['title'], item['author'], include_linebreaks=False),
                    'story_link': first_page_link
                }
                index_items.append(item_dict)
            index_html = chevron.render(f, {
                'header': index_header(include_linebreaks=False),
                'stories': index_items,
                'index_url': self.index_url
            })
        file_output_path = self.html_output_path + "/" + self.index_url
        print("Writing index page to: %s" % file_output_path)
        with open(file_output_path, 'w') as f:
            f.write(index_html)

    def _write_stories_html(self, story_page_template_path, zine_dict):
        story_template = ''
        with open(story_page_template_path, 'r') as f:
            story_template = f.read()

        for item in zine_dict:
            output_directory = item['directory']
            story_contents = item['contents']
            for index, page in enumerate(story_contents):
                # pages are 1-indexed, just to make them a bit more human readable
                current_page = index + 1
                previous_page = f'{str(current_page - 1)}.html' if index > 0 else ''
                next_page = f'{str(current_page + 1)}.html' if index < len(story_contents) -1 else ''
                page_html = chevron.render(story_template, {
                    'back_link': previous_page,
                    'next_link': next_page,
                    'story_lines': [self._htmlize_whitespace(x.replace("\n", "")) for x in page],
                    'index_url': '../story_index.html',
                    'story_title': item['title'],
                    'story_author': item['author'],
                    'page_number': current_page,
                })
                file_output_dir = self.html_output_path + "/" + output_directory + "/"
                file_output_path = file_output_dir + str(current_page) + ".html"
                Path(file_output_dir).mkdir(parents=True, exist_ok=True)
                print("Writing story page to: %s" % file_output_path)
                with open(file_output_path, 'w') as f:
                    f.write(page_html)
    
    def _htmlize_whitespace(self, string):
        # linebreaks are already determined via newlines in source text files.
        # we can (and should) just make all spaces non-breaking.
        # TODO: evaluate this with screen readers
        return string.replace(' ', '&nbsp;')
