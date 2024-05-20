
from bs4 import BeautifulSoup
import re
import os
import glob
import fileinput
import subprocess
import semver

# Check for staged or unstaged changes
changes = subprocess.check_output(['git', 'status', '--porcelain']).decode('utf-8').strip()
if changes:
    print("You have uncommitted changes. Please commit or stash them before running this script.")
    exit(1)

# Get the latest tag
try:
    latest_tag = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0']).decode('utf-8').strip()
except subprocess.CalledProcessError:
    latest_tag = 'v0.0.1'

V_PREFIX=True
if latest_tag[0] != 'v':
    V_PREFIX=False
else:
    latest_tag = latest_tag[1:]

# Increment the patch version number
new_tag = semver.bump_patch(latest_tag)
new_tag = 'v' + new_tag if V_PREFIX else new_tag

# Define the jsdelivr base URL
base_url = 'https://cdn.jsdelivr.net/gh/tyeth/serialfruit-connect@'

# Read the HTML file
with open('src/index.html', 'r') as f:
    html_content = f.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find the stylesheet link
stylesheet_link = soup.find('link', rel='stylesheet')['href']

# Extract the commit SHA or 'main' from the stylesheet link
commit_sha_or_main = re.search(r'@(.+?)/', stylesheet_link).group(1)

# Define the paths to the src directory and the README file
src_dir = './src/'
readme_file = './README.md'

# Find all files in the src directory
src_files = glob.glob(src_dir + '**', recursive=True)

# Replace the old commit SHA or 'main' with the new tag in each file
for file in src_files:
    if os.path.isdir(file):
        continue
    with fileinput.FileInput(file, inplace=True) as f:
        for line in f:
            print(line.replace(base_url + commit_sha_or_main + "/", base_url + new_tag + "/"), end='')
            print(line.replace(base_url + 'main/', base_url + new_tag + "/"), end='')

# Repeat the process for the README file
with fileinput.FileInput(readme_file, inplace=True) as f:
    for line in f:
        print(line.replace(base_url + commit_sha_or_main + "/", base_url + new_tag + "/"), end='')
        print(line.replace(base_url + 'main/', base_url + new_tag + "/"), end='')

# Commit the changes
subprocess.run(['git', 'add', '.'])
subprocess.run(['git', 'commit', '-m', f'Update jsdelivr links to {new_tag}'])

# Tag the new commit
subprocess.run(['git', 'tag', new_tag])

# Push the commit and the tags
subprocess.run(['git', 'push'])
subprocess.run(['git', 'push', '--tags'])















# from bs4 import BeautifulSoup
# import re
# import os
# import glob
# import fileinput
# import subprocess

# # Get the latest commit SHA
# latest_commit_sha = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip().decode('utf-8')

# # Define the jsdelivr base URL
# base_url = 'https://cdn.jsdelivr.net/gh/tyeth/serialfruit-connect@'

# # Read the HTML file
# with open('src/index.html', 'r') as f:
#     html_content = f.read()

# # Parse the HTML content
# soup = BeautifulSoup(html_content, 'html.parser')

# # Find the stylesheet link
# stylesheet_link = soup.find('link', rel='stylesheet')['href']

# # Extract the commit SHA or 'main' from the stylesheet link
# commit_sha_or_main = re.search(r'@(.+?)/', stylesheet_link).group(1)

# # Define the paths to the src directory and the README file
# src_dir = './src/'
# readme_file = './README.md'

# # Find all files in the src directory
# src_files = glob.glob(src_dir + '**', recursive=True)

# # Replace the old commit SHA or 'main' with the latest commit SHA in each file
# for file in src_files:
#     with fileinput.FileInput(file, inplace=True) as f:
#         for line in f:
#             print(line.replace(base_url + commit_sha_or_main + "/", base_url + latest_commit_sha + "/"), end='')
#             print(line.replace(base_url + 'main/', base_url + latest_commit_sha + "/"), end='')

# # Repeat the process for the README file
# with fileinput.FileInput(readme_file, inplace=True) as f:
#     for line in f:
#         print(line.replace(base_url + commit_sha_or_main + "/", base_url + latest_commit_sha + "/"), end='')
#         print(line.replace(base_url + 'main/', base_url + latest_commit_sha + "/"), end='')

