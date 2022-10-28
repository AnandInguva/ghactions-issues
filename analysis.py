
import requests
import os
import json

class GitHubIssues:
  def __init__(self, owner, repo):
    self.owner = owner
    self.repo = repo
    self.query = 'https://api.github.com/repos/AnandInguva/{}/issues'.format(
         self.repo)
    self._github_token = os.environ['GITHUB_TOKEN']
    self.headers = {
        "Authorization": 'token {}'.format(self._github_token),
        "Accept": "application/vnd.github+json"
    }
    if not self._github_token:
      raise Exception(
          'A Github Personal Access token is required to create Github Issues.')

  def create_issue(self, title, description, label: str = 'bug'):
    # current_issue = self.search_issue_with_title(title, label)
    # if current_issue['total_count']:
    #   issue_number = current_issue['items']['number']
    #   print(issue_number)
    #   raise NotImplementedError
    # else:
      data = {
          'owner': self.owner,
          'repo': self.repo,
          'title': title,
          'body': description,
          'label': label
      }
      r = requests.post(
          url=self.query, data=json.dumps(data), headers=self.headers)
      # assert r.status_code == 201

  def search_issue_with_title(self, title, label):
    search_query = "repo:{}/{}+{} type:issue is:open label:{}".format(
        self.owner, self.repo, title, label)
    query = "https://api.github.com/search/issues?q={}".format(search_query)

    response = requests.get(url=query, headers=self.headers)
    print(response.json())
    print(response.json()['total_count'])
    return response.json()

  def comment_on_issue(self):
    """
    If there is an already present issue with the title name,
    update that issue with the new description.
    """
    raise NotImplementedError




if __name__ == '__main__':
  my_issues = GitHubIssues(owner='github-actions', repo='beam')
  my_issues.create_issue(title='Found a bug, trying with Github Actions bot ',
    description='Testing creating issues with Github rest APIs',
                       label='bug')
