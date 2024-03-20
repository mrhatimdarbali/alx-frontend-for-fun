#!/usr/bin/python3
"""
This script converts a markdown file to an html file

Usage: ./markdown2html.py <input_file> <output_file>
"""

import sys
import os

# Function to parse the number of '#' characters at the beginning of the line


def parse_heading(line):
    count = 0
    while line[count] == '#':
        count += 1
    return count

# Function to parse the number of '*' or '-' characters at the beginning of the line


def parse_list(line):
    count = 0
    while line[count] == '*' or line[count] == '-':
        count += 1
    return count

# Function to parse the number of digits at the beginning of the line for ordered lists


def parse_ordered_list(line):
    count = 0
    while line[count].isdigit() or line[count] == '.':
        count += 1
    return count

# Function to check if a line is empty


def is_empty(line):
    return not line.strip()

# Function to convert a markdown file to an html file


def convert_markdown_to_html(input_file, output_file):
    if not os.path.exists(input_file):
        sys.stderr.write(f"Missing {input_file}\n")
        sys.exit(1)

    # Read markdown content from the input file
    with open(input_file, 'r') as md_file:
        markdown_lines = md_file.readlines()

    html_lines = []
    in_list = False
    list_type = None
    in_paragraph = False
    previous_line_empty = False

    # Iterate through each line of the markdown file
    for line in markdown_lines:
        line = line.strip()

        # If the line is empty, close the list or paragraph if necessary
        if is_empty(line):
            if in_list:
                html_lines.append(f"</{list_type}>")
                in_list = False
            elif in_paragraph:
                html_lines.append("</p>")
                in_paragraph = False
            previous_line_empty = True
            html_lines.append("")
        else:
            if previous_line_empty:
                if in_paragraph:
                    html_lines.append("</p>")
                    in_paragraph = False
                html_lines.append("<p>")
                in_paragraph = True
            previous_line_empty = False

            if line.startswith('#'):
                if in_list:
                    html_lines.append(f"</{list_type}>")
                    in_list = False
                elif in_paragraph:
                    html_lines.append("</p>")
                    in_paragraph = False
                heading_level = parse_heading(line)
                html_line = f"<h{heading_level}>{line[heading_level+1:]}</h{heading_level}>"
                html_lines.append(html_line)
            elif line.startswith('*') or line.startswith('-'):
                list_level = parse_list(line)
                if not in_list or list_type != "ul":
                    if in_list:
                        html_lines.append(f"</{list_type}>")
                    elif in_paragraph:
                        html_lines.append("</p>")
                        in_paragraph = False
                    html_lines.append("<ul>")
                    in_list = True
                    list_type = "ul"
                html_line = f"<li>{line[list_level+1:]}</li>"
                html_lines.append(html_line)
            elif line[0].isdigit() and line[1] == '.':
                list_level = parse_ordered_list(line)
                if not in_list or list_type != "ol":
                    if in_list:
                        html_lines.append(f"</{list_type}>")
                    elif in_paragraph:
                        html_lines.append("</p>")
                        in_paragraph = False
                    html_lines.append("<ol>")
                    in_list = True
                    list_type = "ol"
                html_line = f"<li>{line[list_level+2:]}</li>"
                html_lines.append(html_line)
            else:
                if in_list:
                    html_lines.append(f"</{list_type}>")
                    in_list = False
                if not in_paragraph:
                    html_lines.append("<p>")
                    in_paragraph = True
                line_with_br = line.replace('\n', '<br/>')
                html_lines.append(line_with_br)

    # Close the list or paragraph if necessary
    if in_list:
        html_lines.append(f"</{list_type}>")
    elif in_paragraph:
        html_lines.append("</p>")

    # Write the generated HTML content to the output file
    with open(output_file, 'w') as html_file:
        html_file.write('\n'.join(html_lines))


# Main function
if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write(
            "Usage: ./markdown2html.py <input_file> <output_file>\n")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_markdown_to_html(input_file, output_file)
    sys.exit(0)
