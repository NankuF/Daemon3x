import subprocess


# cwd = '/home/nanku/PycharmProjects/Daemon3x/'
#
# git_status = ['git', 'status']
# process = subprocess.Popen(git_status, stdout=subprocess.PIPE, cwd=cwd, text=True)
# data = process.communicate()
# decode bytes in utf-8
# data_utf_8: str = data[0].decode('utf-8')
# print(data)


# # оставляем только файлы для добавления в гит
# lst_data = data.split('изменено:      ')
# # разворачиваем и удаляем все, что не относится к файлам для добавления в гит
# lst_data.reverse()
# lst_data.pop(-1)
# cleaned_data = []
# for file in lst_data:
#     cleaned_data.append(file.split('/')[-1].strip())
#
# # add and commit
# for file in cleaned_data:
#     process = subprocess.Popen(['git', 'commit', '-am', 'test commit'], stdout=subprocess.PIPE, cwd=cwd)
#     data = process.communicate()
#
# process = subprocess.Popen(['git', 'push'], stdout=subprocess.PIPE, cwd=cwd, text=True)
# data = process.communicate()
# # data_utf_8: str = data[0].decode('utf-8')
# print(data_utf_8)


# Проверка результата
# git_status = ['git', 'status']
# process = subprocess.Popen(git_status, stdout=subprocess.PIPE, cwd=cwd)
# data = process.communicate()
# # decode bytes in utf-8
# data_utf_8: str = data[0].decode('utf-8')
# print(data_utf_8)


class Git:
    """work with git in the system
    cwd - directory with git repository"""

    def __init__(self, cwd: str,
                 stdout=subprocess.PIPE,
                 stderr=subprocess.DEVNULL,
                 encoding='utf-8'):
        self.cwd = cwd
        self.stdout = stdout
        self.stderr = stderr
        self.encoding = encoding
        self.data = None

    def process(self, args):
        process = subprocess.Popen(args, stdout=self.stdout, stderr=self.stderr, encoding=self.encoding, cwd=self.cwd)
        data = process.communicate()
        return data

    def command(self, status=0, pull=0):

        if status:
            args = ['git', 'status']
            data = self.process(args)
            self.data = data

        if pull:
            args = ['git', 'pull']
            result = self.process(args)[0].strip('\n')
            print(result)

    def git_add(self):
        """Делает add всех файлов и записывает коммит с сообщением"""
        args = ['git', 'commit', '-am', 'autocommit']
        result = self.process(args)
        print(result)

    def check_add(self):
        """Получаем список файлов для git add"""
        self.command(status=1)
        data = self.data[0].strip().rstrip(r'\n\n').split(
            '\n\nнет изменений добавленных для коммита\n(используйте «git add» и/или «git commit -a»)')
        data = ''.join(data)
        data = data.strip(
            'На ветке master\nВаша ветка обновлена в соответствии с «origin/master».\n\nИзменения, которые не в индексе для коммита:\n  (используйте «git add <файл>…», чтобы добавить файл в индекс)\n  (используйте «git restore <файл>…», чтобы отменить изменения в рабочем каталоге)\n')
        data = data.rstrip().lstrip().split('изменено:      ')
        data.reverse()
        data.pop(-1)
        new_data = []
        for file in data:
            new_data.append(file.split('/')[-1].strip())

        if new_data is None:
            print('git add не требуется')
        if new_data:
            print(f'Изменения в локальном репозитории:\n{new_data}')
            answer = input('Хотите сделать git add? [Y/n]: ').lower()
            if answer == 'y':
                self.git_add()
                print('Локальный репозиторий')
            else:
                print('END')


if __name__ == '__main__':
    git = Git(cwd='/home/nanku/PycharmProjects/Daemon3x/')
    # git.command(pull=0, status=1)
    git.check_add()
