#!/usr/bin/env python3

import sys
import glob
import typing as t
import textwrap
import subprocess

import typer
import cg_at_utils.utils as utils
from cg_at_utils.comments import Comment, CommentSeverity, put_comment


app = typer.Typer(name='tidy')

@app.command()
def main(
    tidy_args: t.List[str] = typer.Argument(
        None, help='Arguments to pass to tidy'
    ),
    ignore_files_not_found: bool = typer.Option(
        False,
        help=textwrap.dedent(
            """
        Ignore comments for files not found in the submission instead of
        raising an error.
        """
        )
    )
) -> t.NoReturn:
    """Run HTML tidy with the given arguments."""
    files: t.List[str] = find_files()
    comments: t.List[str] = []
    
    for file in files:
        comments.extend(process_file(file, tidy_args))
    
    # Uncomment the print statement and comment put_comment for local tests
    #print(comments)
    put_comment({
        'op': 'put_comments',
        'comments': comments,
        'ignore_files_not_found': ignore_files_not_found
    })


def find_files() -> t.List[str]:
    """
    Find all HTML files in the student's folder.
    """
    return glob.glob("*.html")


def process_file(file: str, tidy_args: t.List[str]):
    """
    Processes a single HTML file. This is done in order to preserve the
    filename, which is otherwise lost, due to the way HTML Tidy works.
    
    Each file is processed using the configuration settings declared in the
    config.txt file.
    """
    proc = subprocess.run(
        ['tidy', '-config', 'config.txt', *tidy_args, file],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE, # Tidy outputs the info we want to to stderr
        encoding = 'utf8'
    )
    
    # HTML Tidy seems to be a bit weird, exitign with 1 even when things are
    # running smoothly.
    if proc.returncode != 0 and proc.returncode != 1:
        print('HTML Tidy crashed:\n', proc.returncode, file = sys.stderr)
        # Use sys.exit for local tests
        utils.exit(proc.returncode)
        #sys.exit(proc.returncode)
    
    comments: t.List[str] = []
    # Again, HTML Tidy outputs the interesting information to stderr.
    for err in proc.stderr.splitlines():
        '''
        We're only interested in the error output that starts with "line", as
        no other error output seems to be related to the document checking,
        save for the "Info: Document looks like <doctype>" message.
        '''
        if err.startswith("line"):
            comments.append(translate_error(process_error_message(err), file))
    
    return comments


def translate_error(err: dict, file: str) -> Comment:
    """
    Translates an error message into a comment that CodeGrade can use.
    """
    severity: CommentSeverity = None
    # HTML Tidy only reports two levels: Error and Warning.
    if err['code'].startswith('E'):
        severity = 'error'
    elif err['code'].startswith('W'):
        severity = 'warning'
    
    return {
        'origin': 'HTML Tidy',
        'msg': err['msg'],
        'code': err['code'],
        'severity': severity,
        'line': {
            'start': int(err['line']),
            'end': int(err['line']),
        },
        'column': {
            'start': int(err['col']),
            'end': None,
        },
        'path': [file]
    }


def process_error_message(message: str) -> dict:
    """
    This function parses an error message from HTML Lint and outputs a
    dictionary that can be consumed by translate_error().
    """
    pairs: list = message.split(' - ')
    position_parts: list = pairs[0].split(' ')
    message_parts: list = pairs[1].split(': ')
    line: str = position_parts[1]
    col: str = position_parts[3]
    code: str = message_parts[0]
    msg: str = message_parts[1]
    
    return {'line': line, 'col': col, 'code': code, 'msg': msg}

if __name__ == '__main__':
    app()
