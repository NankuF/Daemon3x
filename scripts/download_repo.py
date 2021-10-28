import subprocess

cwd = '/home/nanku/PycharmProjects/Daemon3x/'

# subprocess.call(['pwd'], cwd=cwd)
# subprocess.call(['git', '--version'], cwd=cwd)
# subprocess.call(['git', 'status'], cwd=cwd)
# subprocess.call(['git', 'status'], cwd=cwd)

git_status = ['git', 'status']
process = subprocess.Popen(git_status, stdout=subprocess.PIPE, cwd=cwd)
data = process.communicate()
# decode bytes in utf-8
data_utf_8: str = data[0].decode('utf-8')
print(data_utf_8)
# оставляем только файлы для добавления в гит
lst_data = data_utf_8.split('изменено:      ')
# разворачиваем и удаляем все, что не относится к файлам для добавления в гит
lst_data.reverse()
lst_data.pop(-1)
cleaned_data = []
for file in lst_data:
    cleaned_data.append(file.split('/')[-1].strip())

for file in cleaned_data:
    process = subprocess.Popen(['git', 'commit', '-am', 'test commit'], stdout=subprocess.PIPE, cwd=cwd)
    data = process.communicate()


git_status = ['git', 'status']
process = subprocess.Popen(git_status, stdout=subprocess.PIPE, cwd=cwd)
data = process.communicate()
# decode bytes in utf-8
data_utf_8: str = data[0].decode('utf-8')
print(data_utf_8)