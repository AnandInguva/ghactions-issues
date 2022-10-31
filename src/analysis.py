
import requests
import os
import json

class GitHubIssues:
  def __init__(self, owner, repo):
    self.owner = owner
    self.repo = repo
    self.query = "https://api.github.com/repos/{self.owner}/{self.repo}/issues"

    self._github_token = os.environ['GITHUB_TOKEN']
    self.headers = {
        "Authorization": 'token {}'.format(self._github_token),
        "Accept": "application/vnd.github+json"
    }
    if not self._github_token:
      raise Exception(
          'A Github Personal Access token is required to create Github Issues.')

  def create_issue(self, title, description, label: str = 'bug'):
      data = {
          'owner': self.owner,
          'repo': self.repo,
          'title': title,
          'body': description,
          'label': label
      }
      r = requests.post(
          url=self.query, data=json.dumps(data), headers=self.headers)
      print(r.json())
      print(r)

  def comment_on_issue(self):
    """
    If there is an already present issue with the title name,
    update that issue with the new description.
    """
    raise NotImplementedError


if __name__ == '__main__':
  my_issues = GitHubIssues(owner='AnandInguva', repo='ghaction-issues')
  my_issues.create_issue(title='Bug creation. Please delete the issue. ',
    description='Testing creating issues with Github rest APIs',
                       label='bug')
