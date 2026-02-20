import sys

import markdown
import docopt

__doc__="""
Usage:
    markdown_to_html [<fname>]
"""

def main(argv=sys.argv[1:]):
    args=docopt.docopt(__doc__,argv)
    fname=args["<fname>"]
    if fname:
        encoding="utf8"
        with open(fname,"r",encoding=encoding) as f:
            text=f.read()
    else:
        text=sys.stdin.read()
    response=markdown.markdown(text)
    print(response)

if __name__ == "__main__":
    main()
