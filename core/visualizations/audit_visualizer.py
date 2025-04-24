from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress
from rich.tree import Tree
from rich.text import Text
from rich import box
from typing import List, Dict, Any
import json

class AuditVisualizer:
    def __init__(self):
        self.console = Console()

    def display_severity_distribution(self, issues: List[Dict[str, Any]]):
        """Display a bar chart of issue severity distribution"""
        severity_counts = {
            'high': 0,
            'medium': 0,
            'low': 0
        }
        
        for issue in issues:
            severity = issue.get('severity', 'low').lower()
            severity_counts[severity] += 1
            
        # Create a table for the distribution
        table = Table(title="Issue Severity Distribution", box=box.ROUNDED)
        table.add_column("Severity", style="bold")
        table.add_column("Count", justify="right")
        table.add_column("Visual", justify="left")
        
        # Add rows with visual bars
        for severity, count in severity_counts.items():
            bar = "█" * count
            color = "red" if severity == "high" else "yellow" if severity == "medium" else "blue"
            table.add_row(
                f"[{color}]{severity.upper()}[/{color}]",
                str(count),
                f"[{color}]{bar}[/{color}]"
            )
            
        self.console.print(table)

    def display_issue_categories(self, issues: List[Dict[str, Any]]):
        """Display a tree view of issues by category"""
        # Group issues by category
        categories = {}
        for issue in issues:
            category = issue.get('category', 'Other')
            if category not in categories:
                categories[category] = []
            categories[category].append(issue)
            
        # Create tree
        tree = Tree("📊 Issue Categories")
        
        for category, category_issues in categories.items():
            category_node = tree.add(f"📁 {category}")
            
            # Group by type within category
            types = {}
            for issue in category_issues:
                issue_type = issue.get('type', 'Other')
                if issue_type not in types:
                    types[issue_type] = []
                types[issue_type].append(issue)
                
            for issue_type, type_issues in types.items():
                type_node = category_node.add(f"📄 {issue_type}")
                
                for issue in type_issues:
                    severity = issue.get('severity', 'low').lower()
                    color = "red" if severity == "high" else "yellow" if severity == "medium" else "blue"
                    type_node.add(f"[{color}]• {issue['message']} (Line {issue.get('line', '?')})[/{color}]")
                    
        self.console.print(tree)

    def display_security_score_breakdown(self, score: int, issues: List[Dict[str, Any]]):
        """Display a detailed breakdown of the security score"""
        # Create a panel with score visualization
        score_color = "green" if score >= 80 else "yellow" if score >= 60 else "red"
        score_bar = "█" * (score // 10) + "░" * (10 - (score // 10))
        
        panel = Panel(
            f"[{score_color}]{score_bar}[/{score_color}]\n"
            f"Score: [{score_color}]{score}/100[/{score_color}]",
            title="Security Score Breakdown",
            border_style=score_color
        )
        
        self.console.print(panel)
        
        # Add score factors
        table = Table(title="Score Factors", box=box.ROUNDED)
        table.add_column("Factor", style="bold")
        table.add_column("Impact", justify="right")
        
        # Calculate impact of each issue type
        issue_impacts = {}
        for issue in issues:
            severity = issue.get('severity', 'low').lower()
            issue_type = issue.get('type', 'Other')
            impact = 10 if severity == 'high' else 5 if severity == 'medium' else 2
            
            if issue_type not in issue_impacts:
                issue_impacts[issue_type] = 0
            issue_impacts[issue_type] += impact
            
        for issue_type, impact in issue_impacts.items():
            table.add_row(issue_type, f"-{impact} points")
            
        self.console.print(table)

    def display_recommendations_priority(self, recommendations: List[str]):
        """Display recommendations in a priority-based format"""
        table = Table(title="Recommendations by Priority", box=box.ROUNDED)
        table.add_column("Priority", style="bold")
        table.add_column("Recommendation")
        
        # Group recommendations by keywords
        high_priority = []
        medium_priority = []
        low_priority = []
        
        high_keywords = ['security', 'vulnerability', 'critical', 'validation', 'access control']
        medium_keywords = ['optimization', 'performance', 'documentation', 'testing']
        
        for rec in recommendations:
            rec_lower = rec.lower()
            if any(keyword in rec_lower for keyword in high_keywords):
                high_priority.append(rec)
            elif any(keyword in rec_lower for keyword in medium_keywords):
                medium_priority.append(rec)
            else:
                low_priority.append(rec)
                
        # Add rows with priority indicators
        for rec in high_priority:
            table.add_row("[red]High[/red]", rec)
        for rec in medium_priority:
            table.add_row("[yellow]Medium[/yellow]", rec)
        for rec in low_priority:
            table.add_row("[blue]Low[/blue]", rec)
            
        self.console.print(table)

    def display_code_metrics(self, code: str, issues: List[Dict[str, Any]]):
        """Display code metrics and statistics"""
        # Calculate basic metrics
        lines = code.split('\n')
        total_lines = len(lines)
        non_empty_lines = len([l for l in lines if l.strip()])
        issue_lines = len(set(issue.get('line', 0) for issue in issues))
        
        # Create metrics table
        table = Table(title="Code Metrics", box=box.ROUNDED)
        table.add_column("Metric", style="bold")
        table.add_column("Value", justify="right")
        
        table.add_row("Total Lines", str(total_lines))
        table.add_row("Non-empty Lines", str(non_empty_lines))
        table.add_row("Lines with Issues", str(issue_lines))
        table.add_row("Issue Density", f"{(issue_lines/non_empty_lines)*100:.1f}%")
        
        self.console.print(table)

    def display_full_report(self, analysis_results: Dict[str, Any]):
        """Display a complete visual report"""
        self.console.print("\n[bold]📊 Security Audit Report[/bold]\n")
        
        # Display security score
        self.display_security_score_breakdown(
            analysis_results.get('score', 0),
            analysis_results.get('issues', [])
        )
        
        # Display severity distribution
        self.display_severity_distribution(analysis_results.get('issues', []))
        
        # Display issue categories
        self.display_issue_categories(analysis_results.get('issues', []))
        
        # Display code metrics
        self.display_code_metrics(
            analysis_results.get('code', ''),
            analysis_results.get('issues', [])
        )
        
        # Display recommendations
        self.display_recommendations_priority(analysis_results.get('recommendations', []))
        
        # Display summary
        if 'summary' in analysis_results:
            self.console.print(Panel(
                analysis_results['summary'],
                title="Summary",
                border_style="blue"
            )) 