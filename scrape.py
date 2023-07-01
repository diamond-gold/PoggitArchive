from urllib.request import Request, urlopen
import json
import os.path

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
            if plugin['changelog_url'] == 'https://poggit.pmmp.io/r/0': # first release, no changelog
                continue
            print('Getting changelog {:s}'.format(progress))
            req = Request(plugin['changelog_url'])
            req.add_header('User-Agent', UA)
            with urlopen(req) as f:
                data = f.read().decode('utf-8')
            with open(changelog,'w', encoding='utf-8') as f:
                f.write(data)

download('pm4',pm4)
download('pm5',pm5)