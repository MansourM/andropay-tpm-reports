"""Tests for configuration management."""

import pytest
import json
import tempfile
from pathlib import Path
from argparse import Namespace


class TestConfig:
    """Tests for Config data class."""

    def test_should_create_config_with_defaults(self):
        """Should create Config with default values."""
        from src.config import Config
        
        config = Config()
        
        assert config.owner == "TechBurst-Pro"
        assert config.project_number == 2
        assert config.default_format == "html"
        assert config.output_directory == "reports"

    def test_should_create_config_with_custom_values(self):
        """Should create Config with custom values."""
        from src.config import Config
        
        config = Config(
            owner="MyOrg",
            project_number=5,
            default_format="md",
            output_directory="output"
        )
        
        assert config.owner == "MyOrg"
        assert config.project_number == 5
        assert config.default_format == "md"
        assert config.output_directory == "output"

    def test_should_load_config_from_json_file(self, tmp_path):
        """Should load configuration from JSON file."""
        from src.config import Config
        
        # Create temporary config file
        config_file = tmp_path / "config.json"
        config_data = {
            "owner": "TestOrg",
            "project_number": 10,
            "default_format": "csv",
            "output_directory": "test_reports"
        }
        config_file.write_text(json.dumps(config_data), encoding='utf-8')
        
        # Load config
        config = Config.load(str(config_file))
        
        assert config.owner == "TestOrg"
        assert config.project_number == 10
        assert config.default_format == "csv"
        assert config.output_directory == "test_reports"

    def test_should_use_defaults_when_config_file_missing(self):
        """Should use default values when config file doesn't exist."""
        from src.config import Config
        
        config = Config.load("nonexistent.json")
        
        assert config.owner == "TechBurst-Pro"
        assert config.project_number == 2
        assert config.default_format == "html"

    def test_should_merge_with_cli_arguments(self):
        """Should merge config with CLI arguments, args take precedence."""
        from src.config import Config
        
        config = Config(owner="FileOrg", project_number=1)
        args = Namespace(owner="CLIOrg", project_number=5, format="json", output="cli_output")
        
        merged = config.merge_with_args(args)
        
        assert merged.owner == "CLIOrg"
        assert merged.project_number == 5
        assert merged.default_format == "json"
        assert merged.output_directory == "cli_output"

    def test_should_keep_config_values_when_args_are_none(self):
        """Should keep config values when CLI args are None."""
        from src.config import Config
        
        config = Config(owner="FileOrg", project_number=1, default_format="html")
        args = Namespace(owner=None, project_number=None, format=None, output=None)
        
        merged = config.merge_with_args(args)
        
        assert merged.owner == "FileOrg"
        assert merged.project_number == 1
        assert merged.default_format == "html"

    def test_should_handle_partial_json_config(self, tmp_path):
        """Should use defaults for missing fields in JSON config."""
        from src.config import Config
        
        config_file = tmp_path / "partial_config.json"
        config_data = {"owner": "PartialOrg"}
        config_file.write_text(json.dumps(config_data), encoding='utf-8')
        
        config = Config.load(str(config_file))
        
        assert config.owner == "PartialOrg"
        assert config.project_number == 2  # default
        assert config.default_format == "html"  # default



class TestConfigValidation:
    """Tests for configuration validation."""

    def test_should_validate_owner_not_empty(self):
        """Should raise error if owner is empty."""
        from src.config import Config, ConfigValidationError
        
        config = Config(owner="", project_number=2)
        
        with pytest.raises(ConfigValidationError, match="owner cannot be empty"):
            config.validate()

    def test_should_validate_project_number_positive(self):
        """Should raise error if project_number is not positive."""
        from src.config import Config, ConfigValidationError
        
        config = Config(owner="Test", project_number=0)
        
        with pytest.raises(ConfigValidationError, match="project_number must be positive"):
            config.validate()

    def test_should_validate_project_number_negative(self):
        """Should raise error if project_number is negative."""
        from src.config import Config, ConfigValidationError
        
        config = Config(owner="Test", project_number=-1)
        
        with pytest.raises(ConfigValidationError, match="project_number must be positive"):
            config.validate()

    def test_should_validate_format_choices(self):
        """Should raise error if format is not valid."""
        from src.config import Config, ConfigValidationError
        
        config = Config(owner="Test", project_number=2, default_format="invalid")
        
        with pytest.raises(ConfigValidationError, match="format must be one of"):
            config.validate()

    def test_should_accept_valid_formats(self):
        """Should accept html, md, csv, json formats."""
        from src.config import Config
        
        for fmt in ["html", "md", "csv", "json"]:
            config = Config(owner="Test", project_number=2, default_format=fmt)
            config.validate()  # Should not raise

    def test_should_pass_validation_with_valid_config(self):
        """Should pass validation with all valid values."""
        from src.config import Config
        
        config = Config(owner="TestOrg", project_number=5, default_format="html")
        config.validate()  # Should not raise

    def test_should_validate_output_directory_not_empty(self):
        """Should raise error if output_directory is empty."""
        from src.config import Config, ConfigValidationError
        
        config = Config(owner="Test", project_number=2, output_directory="")
        
        with pytest.raises(ConfigValidationError, match="output_directory cannot be empty"):
            config.validate()
