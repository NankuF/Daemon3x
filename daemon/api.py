import time
import requests

from environs import Env
from download_repo import Git

# Считываем переменные окружения с файла '.env'
env = Env()
env.read_env('.env')
username = env('USERNAME')
token = env('GITHUB_TOKEN')


class CheckUpdate:
    __start_date = '1970-01-01T00:00:00Z'

    def __init__(self, username, token, update_at=__start_date):
        self.username = username
        self.token = token
        self.update_at = update_at

    def get_update_repo(self):
        repos = requests.get('https://api.github.com/user/repos',
                             auth=(self.username, self.token))
        for repo in repos.json():
            if repo['name'] == 'Daemon3x':
                self.update_at = repo['updated_at']

        if self.update_at > self.__start_date:
            print('DOWNLOAD repository...')
            git = Git('/home/nanku/PycharmProjects/Daemon3x/')
            # git.command(pull=1)
            # self.__start_date = self.update_at

        else:
            print(f'Обновление не требуется, {self.update_at} == {self.__start_date}')
        print('Конец цикла')


if __name__ == '__main__':
    # создаем инстанс класса с заведомо старым апдейтом
    moscow = CheckUpdate(username=username, token=token)
    while 1:
        time.sleep(1)
        moscow.get_update_repo()  # скачиваем инфу по апдейту с репозитория
