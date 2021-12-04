Демон для линукса.
В методе run() пишем, что хотим запустить





daemon3x.py - демон с гугла под Линукс, адаптированный python3.
mydaemon.py - класс-наследник для запуска демона.
api.py - используется для коннекта к гиту и проверки обновления.
download_repo.py - вызывается внутри api.py, содержит основные методы: status, add, push, pull

Запуск демона:
###API
1. Делаем personal access token - https://github.com/settings/tokens (repo, user)
2. Делаем файл '.env' и добавляем его в .gitignore (т.к его не нужно загружать в гит)
3. в .env размещаем
USERNAME= 'ххх'
GITHUB_TOKEN= 'zzz'

на 22 строке файла mydaemon.py указать путь, где будет Cоздан pid для демона и его название.
daemon = MyDaemon('/home/nanku/PycharmProjects/Daemon3x/daemon/mydaemon.pid')

после этого перейти в директорию, где находится mydaemon.py и ввести команду в терминале:
python mydaemon.py start  (stop/restart)

Не забыть в .env поместить свежий token!