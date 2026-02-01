"""GitHub data fetcher v2 using GraphQL API for timestamp support."""

import subprocess
import json
from typing import List, Dict, Optional


class GitHubCLIError(Exception):
    """Raised when GitHub CLI command fails."""
    pass


class GitHubFetcherV2:
    """Fetches data from GitHub Projects using GraphQL API with timestamp support."""
    
    def __init__(self, owner: str, project_number: int):
        """
        Initialize fetcher with project details.
        
        Args:
            owner: GitHub organization or user
            project_number: Project number
        """
        self.owner = owner
        self.project_number = project_number
    
    def _run_gh_command(self, args: List[str]) -> str:
        """
        Execute GitHub CLI command and return output.
        
        Args:
            args: Command arguments for gh CLI
            
        Returns:
            Command stdout as string
            
        Raises:
            GitHubCLIError: If command fails or gh is not installed
        """
        try:
            result = subprocess.run(
                ['gh'] + args,
                capture_output=True,
                text=True,
                check=False,
                encoding='utf-8'
            )
            
            if result.returncode != 0:
                raise GitHubCLIError(
                    f"GitHub CLI command failed: {result.stderr}"
                )
            
            return result.stdout
            
        except FileNotFoundError:
            raise GitHubCLIError(
                "GitHub CLI (gh) is not installed. "
                "Please install from https://cli.github.com/"
            )
    
    def fetch_project_items_with_timestamps(self, limit: int = 100) -> List[Dict]:
        """
        Fetch project items with timestamp data using GraphQL.
        
        Args:
            limit: Maximum number of items to fetch (default 100)
            
        Returns:
            List of project items with timestamp fields
        """
        query = '''
        query($owner: String!, $number: Int!, $limit: Int!) {
          organization(login: $owner) {
            projectV2(number: $number) {
              items(first: $limit) {
                nodes {
                  id
                  createdAt
                  updatedAt
                  fieldValues(first: 20) {
                    nodes {
                      ... on ProjectV2ItemFieldSingleSelectValue {
                        name
                        field {
                          ... on ProjectV2SingleSelectField {
                            name
                          }
                        }
                      }
                      ... on ProjectV2ItemFieldNumberValue {
                        number
                        field {
                          ... on ProjectV2Field {
                            name
                          }
                        }
                      }
                    }
                  }
                  content {
                    ... on Issue {
                      number
                      title
                      url
                      repository {
                        nameWithOwner
                      }
                      createdAt
                      updatedAt
                      closedAt
                      assignees(first: 10) {
                        nodes {
                          login
                        }
                      }
                      labels(first: 10) {
                        nodes {
                          name
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
        '''
        
        output = self._run_gh_command([
            'api', 'graphql',
            '-f', f'query={query}',
            '-F', f'owner={self.owner}',
            '-F', f'number={self.project_number}',
            '-F', f'limit={limit}'
        ])
        
        data = json.loads(output)
        
        # Transform GraphQL response to compatible format
        items = []
        nodes = data.get('data', {}).get('organization', {}).get('projectV2', {}).get('items', {}).get('nodes', [])
        
        for node in nodes:
            content = node.get('content', {})
            if not content:
                continue
            
            # Extract field values
            field_values = {}
            for field_value in node.get('fieldValues', {}).get('nodes', []):
                if not field_value:
                    continue
                
                field = field_value.get('field', {})
                field_name = field.get('name', '')
                
                if 'name' in field_value:  # Single select
                    field_values[field_name] = field_value['name']
                elif 'number' in field_value:  # Number
                    field_values[field_name] = field_value['number']
            
            # Build item with timestamps
            item = {
                'id': node.get('id'),
                'title': content.get('title', ''),
                'status': field_values.get('Status', 'Backlog'),
                'priority': field_values.get('Priority', 'P2'),
                'estimate (Hrs)': field_values.get('estimate (Hrs)'),
                'labels': [label['name'] for label in content.get('labels', {}).get('nodes', [])],
                'assignees': [assignee['login'] for assignee in content.get('assignees', {}).get('nodes', [])],
                'repository': content.get('repository', {}).get('nameWithOwner', ''),
                'content': {
                    'number': content.get('number'),
                    'title': content.get('title', ''),
                    'url': content.get('url', ''),
                    'repository': content.get('repository', {}).get('nameWithOwner', ''),
                    'type': 'Issue'
                },
                # Timestamp fields
                'project_created_at': node.get('createdAt'),
                'project_updated_at': node.get('updatedAt'),
                'issue_created_at': content.get('createdAt'),
                'issue_updated_at': content.get('updatedAt'),
                'issue_closed_at': content.get('closedAt')
            }
            
            items.append(item)
        
        return items
