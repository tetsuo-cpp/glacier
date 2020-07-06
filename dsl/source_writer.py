INDENT_WIDTH = 4


class SourceWriter:
    def __init__(self):
        self.indent = 0
        self.source = str()

    def indent(self):
        self.indent += INDENT_WIDTH

    def unindent(self):
        self.indent -= INDENT_WIDTH

    def reset_indent(self):
        self.indent = 0

    def write_line(self, line):
        self.source += " " * self.indent + line + "\n"

    def get_source(self):
        return self.source
