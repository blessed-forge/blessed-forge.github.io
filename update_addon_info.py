
import json
import requests


class GithubInfo:

    def __init__(self, owner):
        self.owner = owner

    def raw_info(self, repo):
        url = "http://api.github.com/repos/" + self.owner + '/' + repo
        r = requests.get(url, headers={'Accept': 'application/vnd.github.v3+json'})
        r.raise_for_status()
        return r.json()

    def info(self, repo):
        raw = self.raw_info(repo)
        result = {
            'homepage_url': raw['html_url'],
        }
        for k in ('name', 'description', 'issues_url'):
            result[k] = raw[k]

        return result


class Addon_Info:

    def __init__(self, filename):
        self.filename = filename
        self.info = None
        self.blessedforge = None

    def load_info(self):
        if self.info is not None: return
        with open(self.filename) as infile:
            self.info = json.load(infile)

    def update(self):
        self.load_info()
        for addon in self.info:
            src = self.info[addon]['src']
            if src == 'blessed-forge':
                self.info[addon]['latest_info'] = self.get_blessed_forge_info(addon)
            else:
                print(f"I don't know how to fetch info from source '{src}'")

    def save(self, filename=None):
        outfilename = filename if filename is not None else self.filename
        with open(outfilename, 'w') as outfile:
            json.dump(self.info, outfile, indent=4, sort_keys=True)

    def get_blessed_forge_info(self, addon):
        if self.blessedforge is None:
            self.blessedforge = GithubInfo("blessed-forge")
        return self.blessedforge.info(addon)

a = Addon_Info('addon_info.json')
a.update()
a.save()

