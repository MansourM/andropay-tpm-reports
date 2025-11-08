"""Main CLI entry point for GitHub Projects Reporter."""

import sys
import argparse
from pathlib import Path

from src.config import Config, ConfigValidationError
from src.fetcher import GitHubFetcher, GitHubCLIError
from src.processor import parse_items, calculate_metrics
from src.snapshot import save_snapshot, load_latest_snapshot, compare_snapshots
from src.renderers.html_renderer import HTMLRenderer
from src.renderers.md_renderer import MarkdownRenderer
from src.renderers.csv_renderer import CSVRenderer
from src.renderers.json_renderer import JSONRenderer


def create_argument_parser() -> argparse.ArgumentParser:
    """
    Create and configure argument parser.
    
    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        description='Generate reports from GitHub Projects',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate HTML report with defaults
  python -m src.main

  # Generate Markdown report
  python -m src.main --format md

  # Specify custom project
  python -m src.main --owner MyOrg --project 5

  # Custom output location
  python -m src.main --output reports/my-report.html
        """
    )
    
    parser.add_argument(
        '--format',
        choices=['html', 'md', 'csv', 'json'],
        help='Output format (default: from config or html)'
    )
    
    parser.add_argument(
        '--output',
        help='Output file path (default: reports/report.<format>)'
    )
    
    parser.add_argument(
        '--owner',
        help='GitHub organization or user (default: from config)'
    )
    
    parser.add_argument(
        '--project',
        type=int,
        dest='project_number',
        help='Project number (default: from config)'
    )
    
    parser.add_argument(
        '--config',
        default='config.json',
        help='Path to config file (default: config.json)'
    )
    
    parser.add_argument(
        '--no-snapshot',
        action='store_true',
        help='Skip saving snapshot for weekly tracking'
    )
    
    return parser


def get_renderer(format_type: str):
    """
    Get renderer instance for specified format.
    
    Args:
        format_type: Output format (html, md, csv, json)
        
    Returns:
        Renderer instance
    """
    renderers = {
        'html': HTMLRenderer,
        'md': MarkdownRenderer,
        'csv': CSVRenderer,
        'json': JSONRenderer
    }
    
    renderer_class = renderers.get(format_type)
    if not renderer_class:
        raise ValueError(f"Unknown format: {format_type}")
    
    return renderer_class()


def main():
    """Main entry point for the CLI."""
    # Parse arguments
    parser = create_argument_parser()
    args = parser.parse_args()
    
    try:
        # Load configuration
        print("📋 Loading configuration...")
        config = Config.load(args.config)
        config = config.merge_with_args(args)
        config.validate()
        
        # Determine output format and path
        output_format = args.format or config.default_format
        if args.output:
            output_path = args.output
        else:
            output_dir = Path(config.output_directory)
            output_dir.mkdir(parents=True, exist_ok=True)
            # Add timestamp to filename
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            output_path = str(output_dir / f"report-{timestamp}.{output_format}")
        
        # Fetch data from GitHub
        print(f"🔍 Fetching project data from GitHub...")
        print(f"   Owner: {config.owner}")
        print(f"   Project: #{config.project_number}")
        
        fetcher = GitHubFetcher(config.owner, config.project_number)
        
        # Fetch project details
        project_details = fetcher.fetch_project_details()
        project_name = project_details.get('title', f'Project {config.project_number}')
        
        # Fetch project items
        raw_items = fetcher.fetch_project_items()
        print(f"   Found {len(raw_items)} items")
        
        # Process data
        print("⚙️  Processing data...")
        items = parse_items(raw_items)
        metrics = calculate_metrics(items)
        
        print(f"   Total items: {metrics.total_items}")
        print(f"   Completion: {metrics.completion_percentage:.1f}%")
        print(f"   Unplanned: {metrics.unplanned_percentage:.1f}%")
        
        # Save snapshot for weekly tracking
        if not args.no_snapshot:
            print("💾 Saving snapshot...")
            snapshot_path = save_snapshot(items)
            print(f"   Saved to: {snapshot_path}")
            
            # Load and compare with previous snapshot
            previous_items = load_latest_snapshot()
            if previous_items and len(previous_items) > 0:
                # Filter out the current snapshot we just saved
                import os
                snapshots_dir = Path("snapshots")
                snapshot_files = sorted(snapshots_dir.glob("snapshot-*.json"))
                if len(snapshot_files) > 1:
                    # Load the second most recent
                    from src.snapshot import _deserialize_item
                    import json
                    with open(snapshot_files[-2], 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    previous_items = [_deserialize_item(item_data) for item_data in data["items"]]
                    
                    comparison = compare_snapshots(items, previous_items)
                    print(f"   📊 Changes since last snapshot:")
                    print(f"      Items completed: {comparison['items_completed']}")
                    print(f"      Items added: {comparison['items_added']}")
                    print(f"      Status changes: {len(comparison['status_changes'])}")
        
        # Generate report
        print(f"📝 Generating {output_format.upper()} report...")
        renderer = get_renderer(output_format)
        renderer.render(
            items=items,
            metrics=metrics,
            output_path=output_path,
            project_name=project_name,
            owner=config.owner,
            project_number=config.project_number
        )
        
        print(f"✅ Report generated successfully!")
        print(f"   Output: {output_path}")
        
        return 0
        
    except GitHubCLIError as e:
        print(f"❌ GitHub CLI Error: {e}", file=sys.stderr)
        print("\n💡 Make sure GitHub CLI is installed and authenticated:", file=sys.stderr)
        print("   Install: https://cli.github.com/", file=sys.stderr)
        print("   Authenticate: gh auth login", file=sys.stderr)
        return 1
        
    except ConfigValidationError as e:
        print(f"❌ Configuration Error: {e}", file=sys.stderr)
        print("\n💡 Check your config.json or command-line arguments", file=sys.stderr)
        return 1
        
    except FileNotFoundError as e:
        print(f"❌ File Error: {e}", file=sys.stderr)
        return 1
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
