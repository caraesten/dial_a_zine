#!/usr/bin/python3
import os
import argparse
from pathlib import Path
from lib.html_generator import HtmlGenerator

TEMPLATES = "default_templates"
CONTENT_FOLDER = "dial_a_zine_issue1"

parser = argparse.ArgumentParser(description="Use this tool to export html documents for your zine")
parser.add_argument("outputdir", type=Path, help="output directory for generated HTML")

args = parser.parse_args()

if not args.outputdir:
    raise ValueError("Required param outputdir missing, run program with -h")

html_directory = args.outputdir.as_posix()

root_dir_path = Path(__file__).parent.parent.absolute()
index_directory = "%s/%s" % (root_dir_path.as_posix(), f"{CONTENT_FOLDER}/index.json")
templates_directory = "%s/%s" % (root_dir_path.as_posix(), TEMPLATES)
generator = HtmlGenerator(index_directory, html_directory, templates_directory)
generator.write_zine_html()