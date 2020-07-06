INDENT_WIDTH = 4


class SourceWriter:
    def __init__(self):
        self.indent_level = 0
        self.source = str()

    def indent(self):
        self.indent_level += INDENT_WIDTH

    def unindent(self):
        self.indent_level -= INDENT_WIDTH
        assert self.indent_level >= 0

    def reset_indent(self):
        self.indent_level = 0

    def write_line(self, line):
        self.source += " " * self.indent_level + line + "\n"

    def get_source(self):
        return self.source
