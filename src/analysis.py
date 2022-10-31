
import requests
import os
import json

class GitHubIssues:
  def __init__(self, owner, repo):
    self.owner = owner
    self.repo = repo
    self.query = "https://api.github.com/repos/{}/{}/issues".format(
      self.owner, self.repo
    )
    # self.query = "https://api.github.com/repos/AnandInguva/ghactions-issues/issues"


    self._github_token = os.environ['GITHUB_TOKEN']
    self.headers = {
        "Authorization": 'token {}'.format(self._github_token),
        "Accept": "application/vnd.github+json"
    }
    if not self._github_token:
      raise Exception(
          'A Github Personal Access token is required to create Github Issues.')

  def create_issue(self, title, description, label: str = 'bug'):
    last_created_issue =  self.search_issue_with_title(title, label):
    if last_created_issue['total_count']:
      issue_number = last_created_issue['items']['number']
      comment_query = "/repos/{}/{}/issues/{}/comments".format(
        self.owner, self.repo, issue_number
      )
      _COMMENT = "Creating a comment on already created issue."
      data = {
        'owner': self.owner,
        'repo': self.repo,
        'body': _COMMENT,
        issue_number: issue_number,
      }
      respone = requests.post(
        comment_query, json.dumps(data),
        headers=self.headers
      )
      print(respone.json())

    else:
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
  
  def search_issue_with_title(self, title, label):
    search_query = "repo:{}/{}+{} type:issue is:open label:{}".format(
        self.owner, self.repo, title, label)
    query = "https://api.github.com/search/issues?q={}".format(search_query)

    response = requests.get(url=query, headers=self.headers)
    return response.json()


if __name__ == '__main__':
  my_issues = GitHubIssues(owner='AnandInguva', repo='ghactions-issues')
  my_issues.create_issue(title='Bug creation. Please delete the issue. ',
    description='Testing creating issues with Github rest APIs',
                       label='bug')
