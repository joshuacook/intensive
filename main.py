import pandas as pd
import codecs
import json
import re
import xml.etree.ElementTree as ET
import subprocess
import glob, os
# from lib.parse import cell_type, LINE_BREAK, parse_book_data_cell, parse_notebook
from lib.parse import (LINE_BREAK,
                       get_cell_type,
                       get_cells,
                       parse_book_data_cell,
                       parse_notebook)

for f in glob.glob("final.*"):
    os.remove(f)

with open('meta/document_meta_beginning.tex', 'r') as f:
    meta_beginning = ''.join(f.readlines())
with open('meta/document_meta_end.tex', 'r') as f:
    meta_end = ''.join(f.readlines()    )

STARTING_NOTEBOOK = 'contents.ipynb'
cells = get_cells(STARTING_NOTEBOOK)
title_cell_text = [cell_text for cell_text in cells.source if get_cell_type(cell_text) == 'title'][0]

book_data = parse_book_data_cell(title_cell_text)

tex_document = book_data + meta_beginning + LINE_BREAK

tex_document += parse_notebook(STARTING_NOTEBOOK)

tex_document += meta_end

with open('final.tex', 'w') as final:
    final.write(tex_document)

subprocess.call(['pdflatex', 'final.tex'])
subprocess.call(['pdflatex', 'final.tex'])
subprocess.call(['pdflatex', 'final.tex'])

os.rename('final.pdf', 'Intensive.pdf')
