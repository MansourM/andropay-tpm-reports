"""Tests for GitHub data fetcher."""

import pytest
import json
from unittest.mock import patch, MagicMock


class TestGitHubFetcher:
    """Tests for GitHubFetcher class."""

    def test_should_initialize_with_owner_and_project_number(self):
        """Should create GitHubFetcher with owner and project number."""
        from src.fetcher import GitHubFetcher
        
        fetcher = GitHubFetcher("TestOrg", 5)
        
        assert fetcher.owner == "TestOrg"
        assert fetcher.project_number == 5

    @patch('subprocess.run')
    def test_should_run_gh_command_successfully(self, mock_run):
        """Should execute gh CLI command and return output."""
        from src.fetcher import GitHubFetcher
        
        # Mock successful command
        mock_run.return_value = MagicMock(
            stdout='{"test": "data"}',
            returncode=0
        )
        
        fetcher = GitHubFetcher("TestOrg", 5)
        result = fetcher._run_gh_command(['project', 'view', '5'])
        
        assert result == '{"test": "data"}'
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_should_raise_error_when_gh_command_fails(self, mock_run):
        """Should raise error when gh command fails."""
        from src.fetcher import GitHubFetcher, GitHubCLIError
        
        # Mock failed command
        mock_run.return_value = MagicMock(
            stderr='Error: not found',
            returncode=1
        )
        
        fetcher = GitHubFetcher("TestOrg", 5)
        
        with pytest.raises(GitHubCLIError, match="GitHub CLI command failed"):
            fetcher._run_gh_command(['project', 'view', '5'])

    @patch('subprocess.run')
    def test_should_raise_error_when_gh_not_installed(self, mock_run):
        """Should raise error when gh CLI is not installed."""
        from src.fetcher import GitHubFetcher, GitHubCLIError
        
        # Mock FileNotFoundError (gh not found)
        mock_run.side_effect = FileNotFoundError()
        
        fetcher = GitHubFetcher("TestOrg", 5)
        
        with pytest.raises(GitHubCLIError, match="GitHub CLI.*not installed"):
            fetcher._run_gh_command(['project', 'view', '5'])



class TestGitHubFetcherDataMethods:
    """Tests for data fetching methods."""

    @patch('subprocess.run')
    def test_should_fetch_project_details(self, mock_run):
        """Should fetch project metadata."""
        from src.fetcher import GitHubFetcher
        
        project_data = {
            "id": "PVT_test",
            "title": "Test Project",
            "number": 5
        }
        mock_run.return_value = MagicMock(
            stdout=json.dumps(project_data),
            returncode=0
        )
        
        fetcher = GitHubFetcher("TestOrg", 5)
        result = fetcher.fetch_project_details()
        
        assert result == project_data
        # Verify correct command was called
        call_args = mock_run.call_args[0][0]
        assert 'gh' in call_args
        assert 'project' in call_args
        assert 'view' in call_args

    @patch('subprocess.run')
    def test_should_fetch_project_items(self, mock_run):
        """Should fetch all project items with limit 100."""
        from src.fetcher import GitHubFetcher
        
        items_data = {
            "items": [
                {"id": "1", "title": "Item 1"},
                {"id": "2", "title": "Item 2"}
            ]
        }
        mock_run.return_value = MagicMock(
            stdout=json.dumps(items_data),
            returncode=0
        )
        
        fetcher = GitHubFetcher("TestOrg", 5)
        result = fetcher.fetch_project_items()
        
        assert result == items_data["items"]
        # Verify limit 100 was used
        call_args = mock_run.call_args[0][0]
        assert '--limit' in call_args
        assert '100' in call_args

    @patch('subprocess.run')
    def test_should_fetch_project_fields(self, mock_run):
        """Should fetch project field definitions."""
        from src.fetcher import GitHubFetcher
        
        fields_data = {
            "fields": [
                {"id": "f1", "name": "Status"},
                {"id": "f2", "name": "Priority"}
            ]
        }
        mock_run.return_value = MagicMock(
            stdout=json.dumps(fields_data),
            returncode=0
        )
        
        fetcher = GitHubFetcher("TestOrg", 5)
        result = fetcher.fetch_project_fields()
        
        assert result == fields_data["fields"]
        # Verify correct command
        call_args = mock_run.call_args[0][0]
        assert 'field-list' in call_args

    @patch('subprocess.run')
    def test_should_use_owner_and_project_number_in_commands(self, mock_run):
        """Should include owner and project number in gh commands."""
        from src.fetcher import GitHubFetcher
        
        mock_run.return_value = MagicMock(
            stdout='{"id": "test"}',
            returncode=0
        )
        
        fetcher = GitHubFetcher("MyOrg", 10)
        fetcher.fetch_project_details()
        
        call_args = mock_run.call_args[0][0]
        assert '--owner' in call_args
        assert 'MyOrg' in call_args
        assert '10' in call_args

    @patch('subprocess.run')
    def test_should_request_json_format(self, mock_run):
        """Should request JSON format from gh CLI."""
        from src.fetcher import GitHubFetcher
        
        mock_run.return_value = MagicMock(
            stdout='{"test": "data"}',
            returncode=0
        )
        
        fetcher = GitHubFetcher("TestOrg", 5)
        fetcher.fetch_project_details()
        
        call_args = mock_run.call_args[0][0]
        assert '--format' in call_args
        assert 'json' in call_args



class TestGitHubFetcherErrorHandling:
    """Tests for error handling."""

    @patch('subprocess.run')
    def test_should_handle_invalid_json_response(self, mock_run):
        """Should raise error when response is not valid JSON."""
        from src.fetcher import GitHubFetcher
        
        mock_run.return_value = MagicMock(
            stdout='invalid json{',
            returncode=0
        )
        
        fetcher = GitHubFetcher("TestOrg", 5)
        
        with pytest.raises(json.JSONDecodeError):
            fetcher.fetch_project_details()

    @patch('subprocess.run')
    def test_should_handle_authentication_error(self, mock_run):
        """Should raise error with authentication message."""
        from src.fetcher import GitHubFetcher, GitHubCLIError
        
        mock_run.return_value = MagicMock(
            stderr='Error: authentication required',
            returncode=1
        )
        
        fetcher = GitHubFetcher("TestOrg", 5)
        
        with pytest.raises(GitHubCLIError, match="authentication"):
            fetcher.fetch_project_details()

    @patch('subprocess.run')
    def test_should_handle_project_not_found(self, mock_run):
        """Should raise error when project doesn't exist."""
        from src.fetcher import GitHubFetcher, GitHubCLIError
        
        mock_run.return_value = MagicMock(
            stderr='Error: project not found',
            returncode=1
        )
        
        fetcher = GitHubFetcher("TestOrg", 999)
        
        with pytest.raises(GitHubCLIError, match="not found"):
            fetcher.fetch_project_details()
