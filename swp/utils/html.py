from contextlib import suppress
from html.parser import HTMLParser
from pathlib import Path


class IsHTMLParser(HTMLParser):

    class IsHTMLException(Exception):
        pass

    def handle_endtag(self, tag):
        raise self.IsHTMLException(tag)

    @classmethod
    def is_html(cls, filepath: Path) -> bool:
        parser = cls(convert_charrefs=False)

        with suppress(UnicodeDecodeError):
            with open(filepath) as fp:
                for line in fp:
                    try:
                        parser.feed(line)
                    except cls.IsHTMLException:
                        return True
        try:
            HTMLParser.close(parser)
        except cls.IsHTMLException:
            return True

        return False


is_html = IsHTMLParser.is_html
