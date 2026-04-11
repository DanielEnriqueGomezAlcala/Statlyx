from charts.static.call_breakdown import (
    static_chart_bars_breakdown_resume as call_resume_chart,
)
from charts.static.degree_breakdown import static_chart_lines as degree_line_chart
from charts.static.degree_breakdown import static_chart_table as degree_table_chart
from charts.static.mention_breakdown import (
    static_chart_bars_breakdown_resume as mention_resume_chart,
)
from charts.static.shared import static_chart_lines, static_chart_table
from charts.static.subject_breakdown import (
    static_chart_bars_breakdown_resume as subject_resume_chart,
)
from charts.static.tipology_breakdown import (
    static_chart_bars_breakdown_resume as tipology_resume_chart,
)

__all__ = [
    "static_chart_lines",
    "static_chart_table",
    "degree_line_chart",
    "degree_table_chart",
    "subject_resume_chart",
    "tipology_resume_chart",
    "mention_resume_chart",
    "call_resume_chart",
]
