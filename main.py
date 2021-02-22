import os.path
import random


def testfunc(a):
    print(a + 1)
    return a + 1


def newtest(s):
    print(s * 3 * 6)


class Call(object):

    def __init__(self):
        self.folder = ''
        self.count = 0
        self.call = []
        self.num = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.folder:
            f = open(self.folder, 'r', encoding="1251")
            if self.num < self.count:
                for i, line in enumerate(f):
                    if i == self.num:
                        line = line.rstrip('\n')
                        self.call = list(line.split(';'))
                        self.num += 1
                        f.close()
                        return self.call
            else:
                raise StopIteration
        else:
            raise Exception("Use set_folder(path) before iteration")

    def __repr__(self):
        return str(self.call)

    def __getitem__(self, i):
        return self.call[i]

    def __setattr__(self, attr, value):
        if attr == 'folder' or attr == 'count' or attr == 'call' or attr == 'num':
            self.__dict__[attr] = value

        elif attr.startswith('call[') and attr.endswith(']'):
            j = self.count

            for i in range(j):
                if attr == 'call[' + str(i) + ']':
                    self.__dict__[attr] = value

                elif i + 1 == j:
                    raise AttributeError

    def set_folder(self, this):
        self.folder = this
        try:
            with open(self.folder, 'r', encoding="1251") as f:
                self.count = sum(1 for _ in f)
        except Exception:
            raise Exception('Error opening the file')


class Calls(Call):
    def __init__(self):
        Call.__init__(self)
        self.str = []

    def __setattr__(self, attr, value):
        if attr == 'folder' or attr == 'count' or attr == 'call' or attr == 'num' or attr == 'str':
            self.__dict__[attr] = value

    def __iter__(self):
        return self

    def __next__(self):
        if self.folder:
            if self.num < self.count:
                for i in range(self.count):
                    if i == self.num:
                        self.num += 1
                        return self.call[i]
            else:
                raise StopIteration
        else:
            raise Exception("Use read_file(path) before iteration")

    def __getitem__(self, i=0, j=None):
        if isinstance(i, int) and j is None:
            return self.call[i]
        elif isinstance(i, int) and isinstance(j, int):
            return self.call[i][j]

    def __repr__(self):
        return str(self.call)

    def read_file(self, folder):
        with open(folder, 'r', encoding="1251") as f:
            self.count = sum(1 for _ in f)

        f = open(folder, 'r', encoding="1251")
        self.call = f.read().splitlines()
        f.close()
        self.call = list(self.call[i].split(';') for i in range(self.count))
        self.folder = folder

    def save_file(self, dir=''):
        arr = []
        if self.str:
            arr = self.str
        elif not self.str:
            arr = self.call
        if not dir:
            dir = self.folder
        f = open(dir, 'w', encoding="1251")
        f.writelines('\n'.join(';'.join(arr[i]) for i in range(len(arr))))
        f.close()

    def name_sort(self):
        self.str = sorted(self.call, key=lambda object: str(object[2]).lower())

    def number_sort(self):
        self.str = sorted(self.call, key=lambda object: int(object[0]))

    def phone_operator(self, pnum=917):
        self.str = [i for i in self.call if pnum == int(i[1][1:4])]

    def change_line(self, line=0):
        if line < self.count:
            self.num = line

    def get_list(self):
        if not self.str:
            if not self.call:
                raise Exception("Nothing to get")
            elif self.call:
                return self.call
        elif self.str:
            return self.str

    def return_orig(self):
        if self.str:
            self.str = []

    @staticmethod
    def gen_call(count):
        problemset = ['Подключение', 'Соединение', 'Ремонт', 'Установка']
        solveset = ['Да', 'Нет', 'Неизвестно']
        providerset = ['8917', '8905', '8921', '8967', '8987', '8900']
        population = list(range(1, count + 1))
        if count >= 1:
            for _ in range(count):
                phone = str(providerset[random.randint(0, 5)])
                for _ in range(7):
                    phone += str(random.randint(0, 9))
                num = random.randint(0, count - 1)
                past = population[num]
                del population[num]
                count -= 1
                simple = [str(past), phone, problemset[random.randint(0, 3)],
                          solveset[random.randint(0, 2)]]
                yield simple

    @staticmethod
    def folder_count(this):
        path = len([i for i in os.listdir(this) if os.path.isfile(os.path.join(this, i))])
        return path


c = Calls()
c.read_file('F:/dir/data.csv')
c.number_sort()
print(c.get_list())
c.save_file('F:/dir/numbersort.csv')
s = Calls.gen_call(1)
for i in s:
    print(i)
