import os

selected_pages = [12, 52, 87, 108]
b64s = ['OTY4NDg5NDM=', 'MTY0NTQ2NQ==', 'NjU0NTYxMw==', 'MTU0NjQ1NQ==']
os.system('pwd')



for i in range(4):
    filename = 'imgdatas/knowledge_is_power{0}.png'.format(selected_pages[i])
    os.system('exiftool -comment="{0}=" {1}'.format(b64s[i], filename))
    print(filename, 'modified')