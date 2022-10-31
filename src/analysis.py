
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

    self._github_token = os.environ['GITHUB_TOKEN']
    self.headers = {
        "Authorization": 'token {}'.format(self._github_token),
        "Accept": "application/vnd.github+json"
    }
    if not self._github_token:
      raise Exception(
          'A Github Personal Access token is required to create Github Issues.')

  def create_issue(self, title, description, label: str = None):
    """
    Create an issue with title, description with a label.
    If an issue is already present, comment on the issue instead of 
    creating a duplicate issue.
    """
    last_created_issue =  self.search_issue_with_title(title, label)
    if last_created_issue['total_count']:
      self.comment_on_issue(last_created_issue=last_created_issue)
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

  def comment_on_issue(self, last_created_issue):
    """
    If there is an already present issue with the title name,
    update that issue with the new description.
    """
    if last_created_issue['total_count']:
      items = last_created_issue['items'][0]
      comment_url = items['comments_url']
      issue_number = items['number']
      _COMMENT = 'Creating comment on already created issue.'
      data = {
        'owner': self.owner,
        'repo': self.repo,
        'body': _COMMENT,
        issue_number: issue_number,
      }
      respone = requests.post(
        comment_url, json.dumps(data),
        headers=self.headers
      )
    
  def search_issue_with_title(self, title, label=None):
    """
    Filter issues using title.
    """
    search_query = "repo:{}/{}+{} type:issue is:open".format(
        self.owner, self.repo, title)
    if label:
      search_query = search_query + ' label:{}'
    query = "https://api.github.com/search/issues?q={}".format(search_query)

    response = requests.get(url=query, headers=self.headers)
    return response.json()


if __name__ == '__main__':
  my_issues = GitHubIssues(owner='AnandInguva', repo='ghactions-issues')
  title = 'Bug creation. Please delete the issue. '
  label = 'bug'
  my_issues.create_issue(title=title,
    description='Testing creating issues with Github rest APIs')