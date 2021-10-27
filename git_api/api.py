import requests
from environs import Env
from pprint import pprint

# Считываем переменные окружения с файла '.env'
env = Env()
env.read_env('.env')
username = env('USERNAME')
token = env('GITHUB_TOKEN')

# смотрим все репозитории юзера и даты их обновления
repos = requests.get('https://api.github.com/user/repos', auth=(username, token))
for repo in repos.json():
    pprint(repo['html_url'])
    pprint(f'updated at: {repo["updated_at"]}')
