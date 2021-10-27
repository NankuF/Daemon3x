import requests
from environs import Env

# Считываем переменные окружения с файла '.env'
env = Env()
env.read_env('.env')
username = env('USERNAME')
token = env('GITHUB_TOKEN')


class CheckUpdate:
    start_date = '1970-01-01T00:00:00Z'

    def __init__(self, username, token, update_at=start_date):
        self.username = username
        self.token = token
        self.update_at = update_at

    def get_repo(self):
        repos = requests.get('https://api.github.com/user/repos',
                             auth=(self.username, self.token))
        for repo in repos.json():
            if repo['name'] == 'Moscow_stations':
                self.update_at = repo['updated_at']

    def update_repo(self):
        if self.update_at > self.start_date:
            print('DOWNLOAD repository...')
            self.start_date = self.update_at
        else:
            print(self.update_at)
            print('anyone')


# создаем инстанс класса с заведомо старым апдейтом
moscow = CheckUpdate(username=username, token=token)
moscow.update_repo()  # проверяем что он реально старый
moscow.get_repo()  # скачиваем инфу по апдейту с репозитория
moscow.update_repo()  # удостоверяемся что обновилось
