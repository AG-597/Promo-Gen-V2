from colorama import Fore, Style
import os

gray = Fore.LIGHTBLACK_EX
orange = Fore.LIGHTYELLOW_EX
lightblue = Fore.LIGHTBLUE_EX

class log:
    @staticmethod
    def slog(type, color, message, time):
        msg = f"{gray} [ {color}{type}{gray} ] [ {color}{message}{gray} ] [ {Fore.CYAN}{time:.2f}s{gray} ]"
        print(log.center(msg))
        
    @staticmethod
    def ilog(type, color, message):
        msg = f"{gray} [ {color}{type}{gray} ] [ {color}{message}{gray} ]"
        inputmsg = input(log.center(msg) + " ")
        return inputmsg

    @staticmethod
    def log(type, color, message):
        msg = f"{gray} [ {color}{type}{gray} ] [ {color}{message}{gray} ]{Style.RESET_ALL}"
        print(log.center(msg))

    @staticmethod
    def success(message, time):
        log.slog('+', Fore.GREEN, message, time)

    @staticmethod
    def fail(message):
        log.log('X', Fore.RED, message)

    @staticmethod
    def warn(message):
        log.log('!', Fore.YELLOW, message)

    @staticmethod
    def info(message):
        log.log('i', lightblue, message)
        
    @staticmethod
    def input(message):
        return log.ilog('i', lightblue, message)

    @staticmethod
    def working(message):
        log.log('-', orange, message)

    @staticmethod
    def center(text):
        try:
            t_width = os.get_terminal_size().columns
        except OSError:
            t_width = 80 

        textlen = len(text)
        if textlen >= t_width:
            return text
        l_pad = (t_width - textlen) // 2
        return ' ' * l_pad + text