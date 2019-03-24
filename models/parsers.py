# Savital https://github.com/Savital
# Reads data from proc

import os

class KeyboardLayouts():
    lowerEN = ["UK", "ESC", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=",
               "BKSP", "TAB", "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "ENTER", "LCTL",
               "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "\"", "`", "LFSH",
               "\\", "z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "RTSH", "Prnt", "ALT", "SPCE",
               "CPLK", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10",
               "NMLK", "Scroll", "HOME", "UP", "PGUP", "-", "LEFT",
               "UK", "RGHT", "+", "END", "DOWN", "PGDN", "INS", "DELE",
               "UK", "UK", "UK", "F11", "F12",
               "UK", "UK", "LWIN", "UK", "UK", "UK", "UK", "<KPEnter>", "<RCTL>", "<KP/>", "<SysRq>", "<ALT>", "UK",
               "<Home>", "<UP>", "<PGUP>", "<LEFT>", "<RGHT>", "<END>", "<DOWN>",
               "<PGDN>", "<INS>", "<DELE>"]

    upperEN = ["UK", "ESC", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+",
               "BKSP", "TAB", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "{", "}", "ENTER", "LCTL",
               "A", "S", "D", "F", "G", "H", "J", "K", "L", ":", "\"", "~", "LFSH",
               "|", "Z", "X", "C", "V", "B", "N", "M", "<", ">", "?", "RTSH", "Prnt", "ALT", "SPCE",
               "CPLK", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10",
               "NMLK", "Scroll", "HOME", "UP", "PGUP", "-", "LEFT",
               "UK", "RGHT", "+", "END", "DOWN", "PGDN", "INS", "DELE",
               "UK", "UK", "UK", "F11", "F12",
               "UK", "UK", "LWIN", "UK", "UK", "UK", "UK", "<KPEnter>", "<RCTL>", "<KP/>", "<SysRq>", "<ALT>", "UK",
               "<Home>", "<UP>", "<PGUP>", "<LEFT>", "<RGHT>", "<END>", "<DOWN>",
               "<PGDN>", "<INS>", "<DELE>"]

    lowerRU = ["UK", "ESC", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=",
               "BKSP", "TAB", "й", "ц", "у", "к", "е", "н", "г", "ш", "щ", "з", "х", "ъ", "ENTER", "LCTL",
               "ф", "ы", "в", "а", "п", "р", "о", "л", "д", "ж", "э", "ё", "LFSH",
               "\\", "я", "ч", "с", "м", "и", "т", "ь", "б", "ю", ".", "RTSH", "Prnt", "ALT", "SPCE",
               "CPLK", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10",
               "NMLK", "Scroll", "HOME", "UP", "PGUP", "-", "LEFT",
               "UK", "RGHT", "+", "END", "DOWN", "PGDN", "INS", "DELE",
               "UK", "UK", "UK", "F11", "F12",
               "UK", "UK", "LWIN", "UK", "UK", "UK", "UK", "<KPEnter>", "<RCTL>", "<KP/>", "<SysRq>", "<ALT>", "UK",
               "<Home>", "<UP>", "<PGUP>", "<LEFT>", "<RGHT>", "<END>", "<DOWN>",
               "<PGDN>", "<INS>", "<DELE>"]

    upperRU = ["UK", "ESC", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+",
               "BKSP", "TAB", "Й", "Ц", "У", "К", "Е", "Н", "Г", "Ш", "Щ", "З", "Х", "Ъ", "ENTER", "LCTL",
               "Ф", "Ы", "В", "А", "П", "Р", "О", "Л", "Д", "Ж", "Э", "Ё", "LFSH",
               "|", "Я", "Ч", "С", "М", "И", "Т", "Ь", "Б", "Ю", ",", "RTSH", "Prnt", "ALT", "SPCE",
               "CPLK", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10",
               "NMLK", "Scroll", "HOME", "UP", "PGUP", "-", "LEFT",
               "UK", "RGHT", "+", "END", "DOWN", "PGDN", "INS", "DELE",
               "UK", "UK", "UK", "F11", "F12",
               "UK", "UK", "LWIN", "UK", "UK", "UK", "UK", "<KPEnter>", "<RCTL>", "<KP/>", "<SysRq>", "<ALT>", "UK",
               "<Home>", "<UP>", "<PGUP>", "<LEFT>", "<RGHT>", "<END>", "<DOWN>",
               "<PGDN>", "<INS>", "<DELE>"]

    def __init__(self):
        super(KeyboardLayouts, self).__init__()
        self.construct()

    def __del__(self):
        pass

    def construct(self):
        pass

class ProcParser():
    def __init__(self):
        super(ProcParser, self).__init__()
        self.construct()

    def __del__(self):
        pass

    def construct(self):
        pass

    def read(self, path):
        if not os.path.exists(path):
            return False

        results = []
        f = open(path, 'r')
        for line in f:
            list = []
            i = 0
            elm = ""
            while i < len(line):
                if line[i] == ' ':
                    list.append(elm.strip())
                    elm = ""
                if line[i] == '\n':
                    list.append(elm.strip())
                    break
                elm += line[i]
                i += 1

            ch = "UK";
            index = int(list[3])
            layout = int(list[2])
            if layout == 0:
                ch = KeyboardLayouts.lowerEN[index]
            if layout == 1:
                ch = KeyboardLayouts.upperEN[index]
            if layout == 2:
                ch = KeyboardLayouts.lowerRU[index]
            if layout == 3:
                ch = KeyboardLayouts.upperRU[index]
            list[6] = ch
            if (int(list[5]) > 5000):
                list[5] = 5000
            results.append(list)
        f.close()
        return results