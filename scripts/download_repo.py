import subprocess

s = 'tessst'
class Git:
    """Интерфейс для команд git
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
        """Неблокирующий процесс"""
        process = subprocess.Popen(args, stdout=self.stdout, stderr=self.stderr, encoding=self.encoding, cwd=self.cwd)
        data = process.communicate()
        return data

    def command(self, status=0, pull=0):
        """Попытка сделать интерфейс для команд гита"""

        if status:
            args = ['git', 'status']
            data = self.process(args)
            self.data = data

        if pull:
            args = ['git', 'pull']
            result = self.process(args)[0].strip('\n')
            print(result)

    def git_add(self, my_commit):
        """Сделать git add всех файлов и записать коммит с сообщением"""
        args = ['git', 'commit', '-am', my_commit]
        result = self.process(args)
        print(result)

    def git_push(self):
        """Сделать push"""
        args = ['git', 'push']
        result = self.process(args)
        if result[1] is None:
            print('Push успешно выполнен.')

    def auto_add_and_push(self, my_commit: str = 'autocommit'):
        """
        Получаем список файлов для git add
        Предлагаем сделать git add и git push
        Текст коммита можно передать в аргументах
        """
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
            answer = input('Хотите сделать git add + git push? [Y/n]: ').lower()
            if answer == 'y':
                self.git_add(my_commit)
                self.git_push()

            else:
                print('END')


if __name__ == '__main__':
    git = Git(cwd='/home/nanku/PycharmProjects/Daemon3x/')
    # git.command(pull=0, status=1)
    git.auto_add_and_push()
