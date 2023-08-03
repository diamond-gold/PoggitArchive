from urllib.request import Request, urlopen
import json
import os.path
from datetime import datetime

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'

req = Request('https://poggit.pmmp.io/plugins.min.json')
req.add_header('User-Agent', UA)
try:
    with urlopen(req) as f:
        jsonStr = f.read().decode('utf-8')
    plugins = json.loads(jsonStr)
except:
    print("Poggit not reachable")
    exit()
with open('plugins.json','w') as f:
    f.write(json.dumps(plugins, indent=4))
# with open('plugins.json','r') as f:
    # jsonStr = f.read()
    # plugins = json.loads(jsonStr)

pm4 = []
pm5 = []
for plugin in plugins:
    if len(plugin['api']) == 0:
        # print(plugin['name'] + " " + plugin['version'] + ": no api specified")
        continue
    # who still uses pm3 nowadays...
    if plugin['api'][0]['from'][0:1] == '4':
        pm4.append(plugin)
    if plugin['api'][0]['from'][0:1] == '5':
        pm5.append(plugin)

def generateReadme(plugin):
    readme  = '# {:s}\n'.format(plugin['name'])
    if plugin['icon_url'] is not None:
        readme += '<img src="{:s}" width="128" height="128" />\n\n'.format(plugin['icon_url'])
    readme += '## {:s}\n'.format(plugin['tagline'])
    readme += '```properties\n'
    readme += 'Version: {:s}\n'.format(plugin['version'])
    readme += '    API: {:s}\n'.format(plugin['api'][0]['from'])
    readme += '    Updated: {:s} UTC\n'.format(datetime.utcfromtimestamp(plugin['last_state_change_date']).strftime('%d-%m-%Y %H:%M:%S'))
    readme += 'Repo: https://github.com/{:s}\n'.format(plugin['repo_name'])
    readme += 'License: {:s}\n'.format(plugin['license'])
    readme += 'Categories: {:s}\n'.format(','.join([cat['category_name'] for cat in plugin['categories']]))
    readme += 'Keywords: {:s}\n'.format(','.join([words for words in plugin['keywords']]))
    readme += '```'
    return readme

def download(base,plugins):
    print('{:s} {:d}'.format(base,len(plugins)))
    i = 0
    for plugin in plugins:
        i += 1
        path = '{:s}/{:s}'.format(base,plugin['name'])
        if not os.path.exists(path):
            os.makedirs(path)
        progress = '{:d}/{:d} {:s} {:s}'.format(i,len(plugins),plugin['name'],plugin['version'])
        phar = '{:s}/{:s}_v{:s}.phar'.format(path,plugin['name'],plugin['version'])
        if not os.path.exists(phar): 
            print('Getting phar {:s}'.format(progress))
            req = Request(plugin['artifact_url'])
            req.add_header('User-Agent', UA)
            with urlopen(req) as f:
                data = f.read()
            with open(phar,'wb') as f:
                f.write(data)
        desc = phar+'.desc.html'
        if not os.path.exists(desc): 
            print('Getting desc {:s}'.format(progress))
            req = Request(plugin['description_url'])
            req.add_header('User-Agent', UA)
            with urlopen(req) as f:
                data = f.read().decode('utf-8')
            with open(desc,'w', encoding='utf-8') as f:
                f.write(data)
        changelog = phar+'.changelog.html'
        if not os.path.exists(changelog): 
            if plugin['changelog_url'] != 'https://poggit.pmmp.io/r/0': # first release, no changelog
                print('Getting changelog {:s}'.format(progress))
                req = Request(plugin['changelog_url'])
                req.add_header('User-Agent', UA)
                with urlopen(req) as f:
                    data = f.read().decode('utf-8')
                with open(changelog,'w', encoding='utf-8') as f:
                    f.write(data)
        readme = path+'/README.md'
        if not plugin['is_obsolete']:
            # print('Generate readme {:s}'.format(progress))
            data = generateReadme(plugin)
            with open(readme,'w', encoding='utf-8') as f:
                f.write(data)

download('pm4',pm4)
download('pm5',pm5)