from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt6.QtCore import QRegularExpression

class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document, file_extension):
        super().__init__(document)
        self.file_extension = file_extension
        self.highlighting_rules = []

        if self.file_extension == ".py":
            self.setup_python_highlighting()

    def setup_python_highlighting(self):
        # Keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("blue"))
        keyword_format.setFontWeight(QFont.Weight.Bold)

        keywords = ["def", "class", "import", "from", "self", "return", "if", "else", "elif", "for", "while", "try", "except", "finally", "with", "as", "pass", "break", "continue", "lambda", "yield", "global", "nonlocal", "assert", "del", "raise", "not", "and", "or", "is", "in"]

        for keyword in keywords:
            pattern = QRegularExpression(f"\\b{keyword}\\b")
            self.highlighting_rules.append((pattern, keyword_format))

        # Numbers
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("magenta"))
        self.highlighting_rules.append((QRegularExpression(r"\b\d+\b"), number_format))


        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("gray"))
        self.highlighting_rules.append((QRegularExpression(r"#.*"), comment_format))

        # Strings
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("green"))
        self.highlighting_rules.append((QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"'), string_format))
        self.highlighting_rules.append((QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'"), string_format))

        # Class definitions
        class_format = QTextCharFormat()
        class_format.setForeground(QColor("darkMagenta"))
        class_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((QRegularExpression(r"\bclass\s+(\w+)\b"), class_format))

        # Class methods
        method_format = QTextCharFormat()
        method_format.setForeground(QColor("darkCyan"))
        method_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((QRegularExpression(r"\bdef\s+(\w+)\b"), method_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            match_iterator = expression.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                if pattern.pattern().startswith(r"\bclass\s+"):
                    self.setFormat(match.capturedStart(1), match.capturedLength(1), format)
                elif pattern.pattern().startswith(r"\bdef\s+"):
                    self.setFormat(match.capturedStart(1), match.capturedLength(1), format)
                else:
                    self.setFormat(match.capturedStart(), match.capturedLength(), format)