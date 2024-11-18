import os


path = os.getcwd() + '/assets/data/'
folders = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
# print(folders[-40:])


folders = folders[-40:]
prefix = 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/'
folder_paths = []
for f in folders:
    folder_paths.append(prefix+f+'/')

print(folder_paths)


