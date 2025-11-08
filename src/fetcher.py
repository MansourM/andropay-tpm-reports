"""GitHub data fetcher using GitHub CLI."""

import subprocess
import json
from typing import List, Dict


class GitHubCLIError(Exception):
    """Raised when GitHub CLI command fails."""
    pass


class GitHubFetcher:
    """Fetches data from GitHub Projects using gh CLI."""
    
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
                encoding='utf-8'  # Force UTF-8 encoding
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

    
    def fetch_project_details(self) -> Dict:
        """
        Fetch project metadata.
        
        Returns:
            Project details as dictionary
        """
        output = self._run_gh_command([
            'project', 'view', str(self.project_number),
            '--owner', self.owner,
            '--format', 'json'
        ])
        return json.loads(output)
    
    def fetch_project_items(self, limit: int = 100) -> List[Dict]:
        """
        Fetch all project items.
        
        Args:
            limit: Maximum number of items to fetch (default 100)
            
        Returns:
            List of project items
        """
        output = self._run_gh_command([
            'project', 'item-list', str(self.project_number),
            '--owner', self.owner,
            '--format', 'json',
            '--limit', str(limit)
        ])
        data = json.loads(output)
        return data.get('items', [])
    
    def fetch_project_fields(self) -> List[Dict]:
        """
        Fetch project field definitions.
        
        Returns:
            List of field definitions
        """
        output = self._run_gh_command([
            'project', 'field-list', str(self.project_number),
            '--owner', self.owner,
            '--format', 'json'
        ])
        data = json.loads(output)
        return data.get('fields', [])
