# Savital https://github.com/Savital
# Implements methods to calculate stats by log data

class Calc():
    funckeys = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12']
    shortcuts = ['LCTL', 'LFSH', 'RTSH', 'WIN', 'ALT']
    alphabetRU = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    freqCmbsRU = [['ж', 'и'], ['ш', 'и'], ['ч', 'а'], ['щ', 'а'], ['ч', 'у'], ['щ', 'у'], ['ч', 'к'], ['ч', 'н']]
    # жи ши ча ща чу щу чк чн

    def __init__(self):
        super(Calc, self).__init__()
        self.construct()

    def __del__(self):
        pass

    def set(self, log):
        self.clear()
        self.len = len(log)
        for i in range(self.len):
            self.username.append(log[i][0])
            self.id.append(log[i][1])
            self.state.append(log[i][2])
            self.layout.append(log[i][3])
            self.scancode.append(log[i][4])
            self.downtime.append(log[i][5])
            self.searchtime.append(log[i][6])
            self.keyname.append(log[i][7])

    def clear(self):
        self.username.clear()
        self.id.clear()
        self.state.clear()
        self.layout.clear()
        self.scancode.clear()
        self.downtime.clear()
        self.searchtime.clear()
        self.keyname.clear()
        self.len = 0

    def construct(self):
        self.username = []
        self.id = []
        self.state = []
        self.layout = []
        self.scancode = []
        self.downtime = []
        self.searchtime = []
        self.keyname = []
        self.len = 0

    def formStats(self, log):
        stats = [0.0, 0.0, 0.0, 0, 0, [], []]
        self.set(log)

        if self.len == 0:
            return stats

        self.nodes = []
        for i in range(self.len):
            self.nodes.append(False)

        self.lvl = 0
        self.listShrcts = []
        self.count = 0
        self.countShrcts = 0
        self.countFuncs = 0
        self.sumDowntime = 0.0
        self.sumSearchtime = 0.0
        i = 0
        while i < self.len:
            if (self.state[i] == 0) and (not self.nodes[i]) and (self.keyname[i] in self.shortcuts):
                shrct = []
                self.reachTail(i, shrct)

            if self.state[i] == 2:
                self.sumDowntime += self.downtime[i]
                self.sumSearchtime += self.searchtime[i]
                self.count += 1
                if self.keyname[i] in self.funckeys:
                    self.countFuncs += 1
            i += 1

        if self.count == 0:
            return stats

        self.avrDowntime = self.sumDowntime / self.count
        self.avrSearchtime = self.sumSearchtime / self.count
        self.inpSpeed = 1000 * self.count / (self.sumDowntime + self.sumSearchtime)

        self.formRULetterCmbs()

        stats = [self.avrDowntime, self.avrSearchtime, self.inpSpeed, self.countShrcts, self.countFuncs, self.listShrcts, self.listRUCmbs]

        return stats

    def reachTail(self, i, shrct):
        self.nodes[i] = True
        shrct.append(self.keyname[i])
        self.lvl += 1

        j = i + 1
        while j < self.len and self.lvl:
            if not self.nodes[j]:
                if not (self.keyname[j] in self.shortcuts):
                    if self.state[j] == 0 or self.state[j] == 1:
                        tmp = shrct.copy()
                        tmp.append(self.keyname[j])
                        self.listShrcts.append(tmp)
                        self.countShrcts += 1
                else:
                    if self.state[j] == 2:
                        try:
                            k = shrct.index(self.keyname[j])
                        except:
                            k = -1
                        if k != -1:
                            self.nodes[j] = True
                            self.lvl -= 1
                            shrct.pop(k)

                    if self.state[j] == 0:
                        self.reachTail(j, shrct)

            j += 1


    def formRULetterCmbs3(self):
        self.listRUCmbs = []
        i = 0
        while i < self.len - 1:
            if (self.state[i] == 0) and (self.keyname[i] in self.alphabetRU):
                j = i + 1
                while j < self.len:
                    if self.state[j] == 0:
                        if (self.keyname[j] in self.alphabetRU):
                           cmb = []
                           cmb.append(self.keyname[i])
                           cmb.append(self.keyname[j])
                           self.listRUCmbs.append((cmb.copy()))
                        break

                    j += 1
            i += 1


    def isCmbRUFreq(self, cmbRU):
        return self.freqCmbsRU.count(cmbRU)

    def formRULetterCmbs(self):
        self.listRUCmbs = []
        i = 0
        while i < self.len - 1:
            if (self.state[i] == 0) and (self.keyname[i] in self.alphabetRU):
                j = i + 1
                while j < self.len:
                    if self.state[j] == 0:
                        if (self.keyname[j] in self.alphabetRU):
                            cmb = []
                            cmb.append(self.keyname[i])
                            cmb.append(self.keyname[j])
                            if self.isCmbRUFreq(cmb):
                                self.listRUCmbs.append((cmb.copy()))
                        break

                    j += 1
            i += 1
