"""Tests for chart generation."""

import pytest
import json


class TestChartBuilder:
    """Tests for ChartBuilder class."""

    def test_should_create_chart_builder_instance(self):
        """Should create ChartBuilder with RTL support."""
        from src.charts.chart_builder import ChartBuilder
        
        builder = ChartBuilder()
        
        assert builder is not None

    def test_should_have_rtl_configuration(self):
        """Should provide RTL configuration for charts."""
        from src.charts.chart_builder import ChartBuilder
        
        builder = ChartBuilder()
        rtl_config = builder.get_rtl_config()
        
        assert 'font' in rtl_config
        assert rtl_config['font']['family'] == 'Vazir'


class TestStatusDistributionCharts:
    """Tests for status distribution chart generation."""

    def test_should_create_status_pie_chart(self):
        """Should generate pie chart for status distribution."""
        from src.charts.chart_builder import ChartBuilder
        
        builder = ChartBuilder()
        data = {
            "Todo": 10,
            "In Progress": 5,
            "Done": 15
        }
        
        chart_json = builder.create_status_pie_chart(data)
        chart_config = json.loads(chart_json)
        
        assert chart_config['data'][0]['type'] == 'pie'
        assert chart_config['data'][0]['labels'] == ["Todo", "In Progress", "Done"]
        assert chart_config['data'][0]['values'] == [10, 5, 15]

    def test_should_create_status_bar_chart(self):
        """Should generate bar chart for status distribution."""
        from src.charts.chart_builder import ChartBuilder
        
        builder = ChartBuilder()
        data = {
            "Todo": 10,
            "In Progress": 5,
            "Done": 15
        }
        
        chart_json = builder.create_status_bar_chart(data)
        chart_config = json.loads(chart_json)
        
        assert chart_config['data'][0]['type'] == 'bar'
        assert chart_config['data'][0]['x'] == ["Todo", "In Progress", "Done"]
        assert chart_config['data'][0]['y'] == [10, 5, 15]

    def test_should_include_persian_labels_in_status_charts(self):
        """Should use Persian labels in status charts."""
        from src.charts.chart_builder import ChartBuilder
        
        builder = ChartBuilder()
        data = {"Todo": 10}
        
        chart_json = builder.create_status_pie_chart(data)
        chart_config = json.loads(chart_json)
        
        assert 'layout' in chart_config
        assert 'title' in chart_config['layout']

    def test_should_apply_rtl_to_status_charts(self):
        """Should apply RTL configuration to status charts."""
        from src.charts.chart_builder import ChartBuilder
        
        builder = ChartBuilder()
        data = {"Todo": 10}
        
        chart_json = builder.create_status_pie_chart(data)
        chart_config = json.loads(chart_json)
        
        assert chart_config['layout']['font']['family'] == 'Vazir'


class TestPriorityDistributionChart:
    """Tests for priority distribution chart generation."""

    def test_should_create_priority_bar_chart(self):
        """Should generate horizontal bar chart for priority distribution."""
        from src.charts.chart_builder import ChartBuilder
        
        builder = ChartBuilder()
        data = {
            "P🔥": 5,
            "P0": 10,
            "P1": 20,
            "P2": 15
        }
        
        chart_json = builder.create_priority_chart(data)
        chart_config = json.loads(chart_json)
        
        assert chart_config['data'][0]['type'] == 'bar'
        assert chart_config['data'][0]['orientation'] == 'h'

    def test_should_apply_priority_colors(self):
        """Should apply color coding to priority chart."""
        from src.charts.chart_builder import ChartBuilder
        
        builder = ChartBuilder()
        data = {
            "P🔥": 5,
            "P0": 10,
            "P1": 20,
            "P2": 15
        }
        
        chart_json = builder.create_priority_chart(data)
        chart_config = json.loads(chart_json)
        
        assert 'marker' in chart_config['data'][0]
        assert 'color' in chart_config['data'][0]['marker']


class TestPlannedVsUnplannedChart:
    """Tests for planned vs unplanned chart generation."""

    def test_should_create_planned_vs_unplanned_pie_chart(self):
        """Should generate pie chart for planned vs unplanned."""
        from src.charts.chart_builder import ChartBuilder
        
        builder = ChartBuilder()
        planned_count = 50
        unplanned_count = 10
        
        chart_json = builder.create_planned_vs_unplanned_chart(planned_count, unplanned_count)
        chart_config = json.loads(chart_json)
        
        assert chart_config['data'][0]['type'] == 'pie'
        assert chart_config['data'][0]['values'] == [50, 10]

    def test_should_use_green_and_red_colors(self):
        """Should use green for planned and red for unplanned."""
        from src.charts.chart_builder import ChartBuilder
        
        builder = ChartBuilder()
        
        chart_json = builder.create_planned_vs_unplanned_chart(50, 10)
        chart_config = json.loads(chart_json)
        
        colors = chart_config['data'][0]['marker']['colors']
        assert '#22c55e' in colors or 'green' in str(colors).lower()
        assert '#ef4444' in colors or 'red' in str(colors).lower()


class TestTeamWorkloadChart:
    """Tests for team workload chart generation."""

    def test_should_create_team_workload_bar_chart(self):
        """Should generate horizontal bar chart for team workload."""
        from src.charts.chart_builder import ChartBuilder
        
        builder = ChartBuilder()
        data = {
            "user1": 8,
            "user2": 12,
            "user3": 5
        }
        
        chart_json = builder.create_team_workload_chart(data)
        chart_config = json.loads(chart_json)
        
        assert chart_config['data'][0]['type'] == 'bar'
        assert chart_config['data'][0]['orientation'] == 'h'

    def test_should_apply_workload_color_coding(self):
        """Should apply color coding based on workload thresholds."""
        from src.charts.chart_builder import ChartBuilder
        
        builder = ChartBuilder()
        data = {
            "user1": 3,   # Green (< 6)
            "user2": 8,   # Yellow (6-10)
            "user3": 12   # Red (> 10)
        }
        
        chart_json = builder.create_team_workload_chart(data)
        chart_config = json.loads(chart_json)
        
        assert 'marker' in chart_config['data'][0]
        assert 'color' in chart_config['data'][0]['marker']


class TestChartInteractivity:
    """Tests for chart interactivity configuration."""

    def test_should_enable_hover_tooltips(self):
        """Should configure hover tooltips for charts."""
        from src.charts.chart_builder import ChartBuilder
        
        builder = ChartBuilder()
        data = {"Todo": 10}
        
        chart_json = builder.create_status_pie_chart(data)
        chart_config = json.loads(chart_json)
        
        assert 'hoverinfo' in chart_config['data'][0] or 'hovertemplate' in chart_config['data'][0]

    def test_should_enable_legend_interaction(self):
        """Should enable legend click to show/hide data."""
        from src.charts.chart_builder import ChartBuilder
        
        builder = ChartBuilder()
        data = {"Todo": 10}
        
        chart_json = builder.create_status_pie_chart(data)
        chart_config = json.loads(chart_json)
        
        # Plotly enables legend interaction by default
        assert 'showlegend' not in chart_config['layout'] or chart_config['layout']['showlegend'] is True


class TestEmptyDataHandling:
    """Tests for handling empty or invalid data."""

    def test_should_handle_empty_status_data(self):
        """Should handle empty status data gracefully."""
        from src.charts.chart_builder import ChartBuilder
        
        builder = ChartBuilder()
        
        chart_json = builder.create_status_pie_chart({})
        chart_config = json.loads(chart_json)
        
        assert chart_config['data'][0]['labels'] == []
        assert chart_config['data'][0]['values'] == []

    def test_should_handle_zero_planned_and_unplanned(self):
        """Should handle zero values for planned vs unplanned."""
        from src.charts.chart_builder import ChartBuilder
        
        builder = ChartBuilder()
        
        chart_json = builder.create_planned_vs_unplanned_chart(0, 0)
        chart_config = json.loads(chart_json)
        
        assert chart_config['data'][0]['values'] == [0, 0]
