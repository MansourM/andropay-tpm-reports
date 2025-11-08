"""Chart generation using Plotly."""

import json
from typing import Dict


class ChartBuilder:
    """Builder for creating Plotly charts with RTL support."""
    
    def __init__(self):
        """Initialize ChartBuilder with default configuration."""
        self.rtl_config = {
            'font': {
                'family': 'Vazir',
                'size': 14
            }
        }
    
    def get_rtl_config(self) -> dict:
        """
        Get RTL configuration for charts.
        
        Returns:
            Dictionary with RTL font configuration
        """
        return self.rtl_config
    
    def create_status_pie_chart(self, data: Dict[str, int]) -> str:
        """
        Generate pie chart for status distribution.
        
        Args:
            data: Dictionary mapping status names to counts
            
        Returns:
            JSON string of Plotly chart configuration
        """
        chart_config = {
            'data': [{
                'type': 'pie',
                'labels': list(data.keys()),
                'values': list(data.values()),
                'textinfo': 'label+percent',
                'hoverinfo': 'label+value+percent',
                'direction': 'clockwise'
            }],
            'layout': {
                'title': {
                    'text': 'توزیع وضعیت',
                    'font': self.rtl_config['font']
                },
                'font': self.rtl_config['font'],
                'showlegend': True
            }
        }
        return json.dumps(chart_config, ensure_ascii=False)
    
    def create_status_bar_chart(self, data: Dict[str, int]) -> str:
        """
        Generate bar chart for status distribution.
        
        Args:
            data: Dictionary mapping status names to counts
            
        Returns:
            JSON string of Plotly chart configuration
        """
        chart_config = {
            'data': [{
                'type': 'bar',
                'x': list(data.keys()),
                'y': list(data.values()),
                'hoverinfo': 'x+y'
            }],
            'layout': {
                'title': {
                    'text': 'توزیع وضعیت (نمودار میله‌ای)',
                    'font': self.rtl_config['font']
                },
                'font': self.rtl_config['font'],
                'xaxis': {'title': 'وضعیت'},
                'yaxis': {'title': 'تعداد'}
            }
        }
        return json.dumps(chart_config, ensure_ascii=False)
    
    def create_priority_chart(self, data: Dict[str, int]) -> str:
        """
        Generate horizontal bar chart for priority distribution.
        
        Args:
            data: Dictionary mapping priority levels to counts
            
        Returns:
            JSON string of Plotly chart configuration
        """
        # Define priority colors
        priority_colors = {
            'P🔥': '#ef4444',  # Red
            'P0': '#f97316',   # Orange
            'P1': '#eab308',   # Yellow
            'P2': '#3b82f6'    # Blue
        }
        
        labels = list(data.keys())
        values = list(data.values())
        colors = [priority_colors.get(label, '#6b7280') for label in labels]
        
        chart_config = {
            'data': [{
                'type': 'bar',
                'orientation': 'h',
                'y': labels,
                'x': values,
                'marker': {
                    'color': colors
                },
                'hoverinfo': 'y+x'
            }],
            'layout': {
                'title': {
                    'text': 'توزیع اولویت',
                    'font': self.rtl_config['font']
                },
                'font': self.rtl_config['font'],
                'xaxis': {'title': 'تعداد'},
                'yaxis': {'title': 'اولویت'}
            }
        }
        return json.dumps(chart_config, ensure_ascii=False)
    
    def create_planned_vs_unplanned_chart(self, planned_count: int, unplanned_count: int) -> str:
        """
        Generate pie chart for planned vs unplanned items.
        
        Args:
            planned_count: Number of planned items
            unplanned_count: Number of unplanned items
            
        Returns:
            JSON string of Plotly chart configuration
        """
        chart_config = {
            'data': [{
                'type': 'pie',
                'labels': ['برنامه‌ریزی شده', 'برنامه‌ریزی نشده'],
                'values': [planned_count, unplanned_count],
                'marker': {
                    'colors': ['#22c55e', '#ef4444']  # Green, Red
                },
                'textinfo': 'label+percent',
                'hoverinfo': 'label+value+percent'
            }],
            'layout': {
                'title': {
                    'text': 'برنامه‌ریزی شده در مقابل برنامه‌ریزی نشده',
                    'font': self.rtl_config['font']
                },
                'font': self.rtl_config['font'],
                'showlegend': True
            }
        }
        return json.dumps(chart_config, ensure_ascii=False)
    
    def create_team_workload_chart(self, data: Dict[str, int]) -> str:
        """
        Generate horizontal bar chart for team workload.
        
        Args:
            data: Dictionary mapping team member names to item counts
            
        Returns:
            JSON string of Plotly chart configuration
        """
        # Apply color coding based on workload
        labels = list(data.keys())
        values = list(data.values())
        colors = []
        
        for count in values:
            if count > 10:
                colors.append('#ef4444')  # Red
            elif count >= 6:
                colors.append('#eab308')  # Yellow
            else:
                colors.append('#22c55e')  # Green
        
        chart_config = {
            'data': [{
                'type': 'bar',
                'orientation': 'h',
                'y': labels,
                'x': values,
                'marker': {
                    'color': colors
                },
                'hoverinfo': 'y+x'
            }],
            'layout': {
                'title': {
                    'text': 'بار کاری تیم',
                    'font': self.rtl_config['font']
                },
                'font': self.rtl_config['font'],
                'xaxis': {'title': 'تعداد آیتم‌های فعال'},
                'yaxis': {'title': 'عضو تیم'}
            }
        }
        return json.dumps(chart_config, ensure_ascii=False)
