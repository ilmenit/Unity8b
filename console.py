class console():
    @classmethod
    def info(cls, *args):
        to_print = ''
        for i, value in enumerate(args):  # styles is a regular dictionary
            if i != 0:
                to_print += ' '
            to_print += str(value)
        print(to_print)
        if cls.consoleWindow!=None:
            cls.consoleWindow.append(to_print)

    @classmethod
    def clear(cls):
        if cls.consoleWindow != None:
            cls.consoleWindow.clear()

    @classmethod
    def init(cls, consoleWindow):
        cls.consoleWindow = consoleWindow