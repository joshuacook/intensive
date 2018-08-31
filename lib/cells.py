import re
import base64

LINE_BREAK = "\n"

def bold(markdown_cell_text):
    regex = re.compile(r"\*\*(.+?)\*\*")
    return regex.sub("\\\\textbf{\\1}", markdown_cell_text)

def code(markdown_cell_text, outputs, execution_count):

    try:
        execution_count = int(execution_count)
    except:
        import pdb; pdb.set_trace()
    caption = re.search(r"###### (.+?)\n", markdown_cell_text).groups()[0]
    label = (caption
             .replace('`','')
             .replace('$', '')
             .replace(',', '')
             .replace('?', '')
             .replace(' ','_')
             .replace('\\','')
             .lower())

    caption = inline_code(caption)
    caption = pound_symbol(caption)

    if type(outputs) == tuple:
        if outputs[0] == 'img':
            output_image = outputs[1]
            output_table = None
            outputs = None
            with open(f"img/{label}.png", "wb") as fh:
                fh.write(base64.decodebytes(output_image))
        elif outputs[0] == 'table':
            output_image = None
            output_table = outputs[1]
            output_table = ("\\begin {table}[H]" +
                            f"\\caption{{{caption}}}" +
                            f"\\label{{tab:{label}}}" +
                            "\\begin{center}") + output_table
            output_table += "\\end{center}\\end {table}"
            outputs = None

    else:
        output_image = None
        output_table = None
    markdown_cell_text = re.sub(r"###### .+\n\n","",markdown_cell_text)
    markdown_cell_text = (markdown_cell_text
                          .replace("\n", "\n          "))

    text  = "\n\n\\begin{minipage}{\\linewidth}"
    text += "\\begin{lstlisting}"
    text += f"[label=lst:{label}, caption={{{caption}}}]\n"
    try:
        text += f"In [{execution_count}]: ".rjust(10)
        text += markdown_cell_text + LINE_BREAK
    except TypeError:
        import pdb; pdb.set_trace()
    if outputs:
        outputs = (outputs
                   .replace("\n", "\n          ")
                   .replace('’', "'")
                   .replace('‘', "'"))
        text += LINE_BREAK + f"Out[{execution_count}]: ".rjust(10)
        text += outputs + LINE_BREAK
    text += "\\end{lstlisting}\n"
    text += "\\end{minipage}"

    if output_image:
        text += image(label, caption)
    if output_table:
        text += LINE_BREAK + output_table
    return text

def enumerate_list(markdown_cell_text):
    if markdown_cell_text.startswith(tuple(str(i) for i in range(10))):
        regex_begin_list = re.compile(r"^\d\. ")
        regex_end_list = re.compile(r"(\d\. .+?)$")
        regex_item = re.compile(r"\d\. (.+)")

        markdown_cell_text = regex_begin_list.sub(
            '\\\\begin{enumerate}\n1. ', markdown_cell_text
        )
        markdown_cell_text = regex_end_list.sub(
            '\n\\1\n\\\\end{enumerate}', markdown_cell_text
        )

        markdown_cell_text = regex_item.sub(
            "\\item \\1", markdown_cell_text
        )
    return markdown_cell_text

def footnotes(markdown_cell_text):
    regex = re.compile(r"<sup>(.+?)</sup>", re.S)
    footnotetags = regex.findall(markdown_cell_text)

    footnotes = []
    for tag in footnotetags:
        regex = re.compile(re.escape(tag)+ r': (.+?)\n', re.S)
        match = regex.search(markdown_cell_text)
        if match:
            footnotes.append((tag, match.groups()[0]))

    for tag, note in footnotes:
        regex = re.compile(f"<sup>{tag}</sup>")
        markdown_cell_text = regex.sub(f"\\\\footnote{{{note}}}", markdown_cell_text)
        regex = re.compile(f"{tag}: {note}")
        markdown_cell_text = regex.sub("", markdown_cell_text)
        # markdown_cell_text = markdown_cell_text.replace("_", "\\_")

    return markdown_cell_text

def header(cell_type, markdown_cell_text):

    title = footnotes(markdown_cell_text)
    title = re.sub(r"#.+? ", "", title)
    title = inline_code(title)
    label = (title
             .replace('`','')
             .replace('$', '')
             .replace('%', '')
             .replace(',', '')
             .replace('?', '')
             .replace(' ','_')
             .replace('\\','')
             .lower())
    title = pound_symbol(title)

    if cell_type == 'chapter':
        processed_text = f"\chapter{{{title}}}\label{{ch:{label}}}"
    elif cell_type == 'section':
        processed_text = f"\section{{{title}}}\label{{sec:{label}}}"
    elif cell_type == 'subsection':
        processed_text = f"\subsection*{{{title}}}\label{{ssec:{label}}}"
    else:
        processed_text = f"\subsubsection*{{{title}}}\label{{sssec:{label}}}"

    return processed_text

def image(url, caption):
    if caption:
        caption = inline_code(caption)
        caption = bold(caption)
        caption = italics(caption)
        caption = pound_symbol(caption)
    text = "\\begin{figure}"
    text += f"[H]\\includegraphics[width=\\linewidth]{{{url}}}"
    text += f"\\caption{{{caption}}}\label{{fig:{url}}}"
    text += "\\end{figure}"
    return text

def italics(markdown_cell_text):
    regex = re.compile(r"\*(.+?)\*")
    return regex.sub("\\\\textit{\\1}", markdown_cell_text)

def itemize(markdown_cell_text):
    if markdown_cell_text.startswith('- '):
        regex_begin_list = re.compile(r"^- ")
        regex_end_list = re.compile(r"\n(- .+?)$")
        regex_item = re.compile(r"- (.+)")

        markdown_cell_text = regex_begin_list.sub(
            '\\\\begin{itemize}\n- ', markdown_cell_text
        )
        markdown_cell_text = regex_end_list.sub(
            '\n\\1\n\\\\end{itemize}', markdown_cell_text
        )

        markdown_cell_text = regex_item.sub(
            "\\item \\1", markdown_cell_text
        )

    return markdown_cell_text

def inline_code(markdown_cell_text):
    # markdown_cell_text = markdown_cell_text.replace('%', "\\%")

    regex = re.compile(r"`(.+?)`")
    match = regex.search(markdown_cell_text)
    if match:
        markdown_cell_text = regex.sub("\\\\texttt{\\1}", markdown_cell_text)
    return markdown_cell_text

def listing(label, caption, markdown_cell_text):
    caption = inline_code(caption)
    caption = pound_symbol(caption)

    markdown_cell_text = re.sub(r"<include.+\n","",markdown_cell_text)
    markdown_cell_text = re.sub(r"###### .+\n","",markdown_cell_text)
    regex = re.compile(r"```\n(.+)```", re.S)
    code = regex.search(markdown_cell_text)
    if code:
        code = code.groups()[0]
    text  = "\n\n\\begin{minipage}{\\linewidth}"
    text += "\\begin{lstlisting}"
    text += f"[label=lst:{label}, caption={{{caption}}}]\n"
    try:
        text += code + LINE_BREAK
    except TypeError:
        import pdb; pdb.set_trace()
    text += "\\end{lstlisting}\n"
    text += "\\end{minipage}"
    return text

def math(markdown_cell_text):
    math = re.compile(r"\$.+?\$")
    matches = math.findall(markdown_cell_text)
    for match in matches:
        markdown_cell_text = (markdown_cell_text
                              .replace(match, match.replace('\\_','_')))
    return markdown_cell_text

def pound_symbol(markdown_cell_text):
    return (markdown_cell_text
            .replace('#', '\#')
            .replace('_', '\_')
            .replace('’', "'")
            .replace('‘', "'")
            .replace('%', "\%")
            .replace('\\s', "\\\\s"))
