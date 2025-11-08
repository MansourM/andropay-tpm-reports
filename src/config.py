"""Configuration management for GitHub Projects Reporter."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from argparse import Namespace


class ConfigValidationError(Exception):
    """Raised when configuration validation fails."""
    pass


@dataclass
class Config:
    """Configuration for the report generator."""
    
    owner: str = "TechBurst-Pro"
    project_number: int = 2
    default_format: str = "html"
    output_directory: str = "reports"
    
    @classmethod
    def load(cls, config_path: Optional[str] = None) -> 'Config':
        """
        Load configuration from file or use defaults.
        
        Args:
            config_path: Path to config.json file
            
        Returns:
            Config instance with loaded or default values
        """
        if config_path is None:
            config_path = "config.json"
        
        config_file = Path(config_path)
        
        # Use defaults if file doesn't exist
        if not config_file.exists():
            return cls()
        
        # Load from file
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return cls(
                owner=data.get('owner', cls.owner),
                project_number=data.get('project_number', cls.project_number),
                default_format=data.get('default_format', cls.default_format),
                output_directory=data.get('output_directory', cls.output_directory)
            )
        except (json.JSONDecodeError, IOError):
            # Return defaults if file is invalid
            return cls()
    
    def merge_with_args(self, args: Namespace) -> 'Config':
        """
        Merge config with CLI arguments (args take precedence).
        
        Args:
            args: Parsed command-line arguments
            
        Returns:
            New Config instance with merged values
        """
        return Config(
            owner=args.owner if args.owner is not None else self.owner,
            project_number=args.project_number if args.project_number is not None else self.project_number,
            default_format=args.format if hasattr(args, 'format') and args.format is not None else self.default_format,
            output_directory=args.output if hasattr(args, 'output') and args.output is not None else self.output_directory
        )
    
    def validate(self) -> None:
        """
        Validate configuration values.
        
        Raises:
            ConfigValidationError: If any validation fails
        """
        # Validate owner
        if not self.owner or not self.owner.strip():
            raise ConfigValidationError("owner cannot be empty")
        
        # Validate project_number
        if self.project_number <= 0:
            raise ConfigValidationError("project_number must be positive")
        
        # Validate format
        valid_formats = ["html", "md", "csv", "json"]
        if self.default_format not in valid_formats:
            raise ConfigValidationError(f"format must be one of: {', '.join(valid_formats)}")
        
        # Validate output_directory
        if not self.output_directory or not self.output_directory.strip():
            raise ConfigValidationError("output_directory cannot be empty")
