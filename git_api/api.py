import time
import requests

from environs import Env
from scripts.download_repo import Git

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
            if repo['name'] == 'Moscow_stations':
                self.update_at = repo['updated_at']

        if self.update_at > self.__start_date:
            self.__start_date = self.update_at
            print('DOWNLOAD repository...')
            git = Git('/home/nanku/PycharmProjects/Daemon3x/')
            git.command(pull=1)

        else:
            print(f'Обновление не требуется, {self.update_at} == {self.__start_date}')


if __name__ == '__main__':

    # создаем инстанс класса с заведомо старым апдейтом
    moscow = CheckUpdate(username=username, token=token)
    while 1:
        time.sleep(5)
        moscow.get_update_repo()  # скачиваем инфу по апдейту с репозитория
