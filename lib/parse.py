import pandas as pd
import numpy as np
import codecs
import json
import re
import requests
import xml.etree.ElementTree as ET

from lib.cells import (bold, code, enumerate_list, footnotes,
                       header, image, inline_code, itemize,
                       italics, listing, math, pound_symbol)
LINE_BREAK = '\n'

def get_cells(notebook_file):

    codec = codecs.open(notebook_file)
    nb = json.load(codec)
    cells = pd.DataFrame(nb['cells'])
    # cells = cells[['source']]
    cells.source = cells.source.apply(lambda x: ''.join(x))
    if 'outputs' in cells.columns:
        cells.outputs = cells.outputs.apply(get_cell_outputs)
    else:
        cells['outputs'] = np.nan
        cells['execution_count'] = np.nan
    return cells

def get_cell_type(markdown_cell_text):
    types = ['paragraph', 'title', 'chapter', 'section', 'subsection', 'subsubsection', 'code']
    heading = re.match('^#+ ', markdown_cell_text)
    include = re.match(r'<include', markdown_cell_text)
    if heading:
        count = heading[0].count('#')
    elif include:
        include_type = re.match(r'.+ type="(.+?)"', markdown_cell_text).groups()[0]
        return include_type
    else:
        count = 0
    return types[count]

def get_cell_outputs(outputs):
    if (not outputs is np.nan) and (not outputs == []):
        if 'data' in outputs[0].keys():
            data = outputs[0]['data']
        else:
            return ''.join(outputs[0]['text'])
        if 'image/png' in data.keys():
            return ('img', data['image/png'].encode())
        elif 'text/html' in data.keys():
            text = '\n'.join(data['text/html'])
            try:
                df = pd.read_html(text)[0]
                r = re.compile(r"Unnamed: \d+")
                latex = df.to_latex(index=False)
                outputs = ('table', r.sub(' ', latex))
            except:
                outputs = ''.join(data['text/plain'])
            return outputs
        else:
            if data == {}:
                return None
            outputs = data['text/plain']
            return ''.join(outputs)
    else:
        return None

def get_image(url, name, d='../img/'):
    f = open(d+name,'wb')
    f.write(requests.get(url).content)
    f.close()

def get_metadata(markdown_cell_text):
    caption_regex = re.compile('.+###### (.+?)\n', re.S)
    caption   = caption_regex.match(markdown_cell_text)
    label     = re.match('.+ label="(.+?)"', markdown_cell_text)

    if caption:     caption = caption.groups()[0]
    if label:         label = label.groups()[0]

    try:
        cell_type = get_cell_type(markdown_cell_text)
    except IndexError:
        import pdb; pdb.set_trace()

    if cell_type == 'notebook':
        r = re.compile('href="(.+?)"', re.S)
        url = r.search(markdown_cell_text).groups()[0]
    elif cell_type == 'image':
        r = re.compile('img/(.+?)\)', re.S)
        url = r.search(markdown_cell_text).groups()[0]
    else:
        url = None

    return caption, cell_type, label, url

def parse_book_data_cell(markdown_cell_text):
    lines = markdown_cell_text.split("\n")
    lines = [re.sub('^#+ ', '', line) for line in lines]
    no_pounds = '<cell>'+'\n'.join(lines)+'</cell>'

    cell_xml = ET.fromstring(no_pounds)

    for child in cell_xml.getchildren():
        if child.tag == 'booktitle':
            title = child.text
        if child.tag == 'author':
            author = child.text

    book_data = parse_book_data(title, author)
    return book_data

def parse_book_data(title, author):
    tex_doc_beginning = f"""
    \\documentclass{{book}}
    \\title{{{title}}}
    \\author{{{author}}}"""

    return tex_doc_beginning

def parse_markdown(markdown_cell_text):
    markdown_cell_text = footnotes(markdown_cell_text)
    markdown_cell_text = inline_code(markdown_cell_text)
    markdown_cell_text = bold(markdown_cell_text)
    markdown_cell_text = italics(markdown_cell_text)
    markdown_cell_text = pound_symbol(markdown_cell_text)
    markdown_cell_text = itemize(markdown_cell_text)
    markdown_cell_text = enumerate_list(markdown_cell_text)
    markdown_cell_text = math(markdown_cell_text)
    return "\paragraph{}\n" + markdown_cell_text

def parse_notebook(notebook_file):

    cells = get_cells(notebook_file)

    processed_text = ''
    for text, outputs, execution_count in cells[['source', 'outputs', 'execution_count']].values:
        caption, cell_type, label, url = get_metadata(text)
        if cell_type in ['chapter', 'section', 'subsection', 'subsubsection']:
            processed_text += header(cell_type, text)
        elif cell_type == 'code':
            processed_text += code(text, outputs, execution_count)
        elif cell_type == 'image':
            processed_text += image(url, caption)
        elif cell_type == 'listing':
            processed_text += listing(label, caption, text)
        elif cell_type == 'notebook':
            print(url)
            processed_text += parse_notebook(url)
        elif cell_type == 'paragraph':
            processed_text += parse_markdown(text)
        processed_text += LINE_BREAK
    return processed_text
