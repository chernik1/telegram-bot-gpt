

class Regular:

    def __init__(self, name_regex):
        self.name_regex = name_regex

    def __str__(self):
        return 'Регулярное выражение: ' + self.name_regex

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name_regex})'

