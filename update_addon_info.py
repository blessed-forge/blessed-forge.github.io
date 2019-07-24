
import os
import json

import requests
from packaging import version

class GithubInfo:

    def __init__(self, owner):
        self.owner = owner

    def _getj(self, url):
        auth_env = os.environ.get('GITHUB_BASIC_AUTH')
        auth = tuple(auth_env.split(':', 1)) if auth_env is not None else None
        r = requests.get(url, headers={'Accept': 'application/vnd.github.v3+json'}, auth=auth)
        r.raise_for_status()
        return r.json()

    def repo_info(self, repo):
        return self._getj("http://api.github.com/repos/" + self.owner + '/' + repo)

    def release_info(self, repo):
        return self._getj("http://api.github.com/repos/" + self.owner + '/' + repo + '/tags')

    def latest_release_info(self, repo):
        rels = self.release_info(repo)
        return max(rels, key=lambda k: version.parse(k['name']))

    def info(self, repo):
        repoj = self.repo_info(repo)
        result = {
            'homepage_url': repoj['html_url'],
        }
        for k in ('name', 'description', 'issues_url'):
            result[k] = repoj[k]

        try:
            relj = self.latest_release_info(repo)
            result.update(**{
                'release_name': relj['name'],
                'release_zip': relj['zipball_url'],
                'release_tar': relj['tarball_url']
            })
        except Exception as e:
            print(f"Problem getting release for repo {repo}: {e!r}")
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

