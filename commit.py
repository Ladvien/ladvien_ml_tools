import sys, os

commit_message = input('Git message: ')
os.system('git add .')
os.system(f'git commit -m {commit_message}')
os.system('git push')
os.system('pip uninstall ladvien_ml -y')
