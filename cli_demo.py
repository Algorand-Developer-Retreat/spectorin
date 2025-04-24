#!/usr/bin/env python3
import argparse
import json
import os
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
from rich.markdown import Markdown
from rich.syntax import Syntax
from datetime import datetime
from core.plugin_manager import PluginManager
from core.ai_agents.manager import AIAgentManager
from core.visualizations.audit_visualizer import AuditVisualizer
from core.analyzers.base_analyzer import Severity

console = Console()

def analyze_contract(file_path: str, language: str, memory_efficient: bool = False, output_format: str = "rich") -> dict:
    """Analyze a smart contract file using the Spectorin core engine"""
    
    # Read the file
    try:
        with open(file_path, 'r') as f:
            code = f.read()
    except Exception as e:
        console.print(f"[bold red]Error reading file: {str(e)}")
        return None
    
    # Show progress
    with Progress() as progress:
        task = progress.add_task(f"[green]Analyzing {os.path.basename(file_path)}...", total=100)
        
        # Initialize components
        progress.update(task, advance=25, description="[green]Initializing analyzer...")
        plugin_manager = PluginManager()
        ai_agent = AIAgentManager(memory_efficient=memory_efficient)
        
        # Analyze code
        progress.update(task, advance=25, description="[green]Analyzing patterns...")
        try:
            analysis_results = plugin_manager.analyze_code(code, language)
            
            # Get AI recommendations
            progress.update(task, advance=25, description="[green]Generating recommendations...")
            recommendations = ai_agent.generate_recommendations(code, language, analysis_results.get('issues', []))
            
            # Calculate final score
            progress.update(task, advance=25, description="[green]Finalizing results...")
            score = analysis_results.get('score', 0)
            
            return {
                'score': score,
                'issues': analysis_results.get('issues', []),
                'recommendations': recommendations,
                'summary': analysis_results.get('summary', ''),
                'code': code,
                'timestamp': datetime.now().isoformat(),
                'file': file_path,
                'language': language
            }
            
        except Exception as e:
            console.print(f"\n[bold red]Error during analysis: {str(e)}")
            return None

def display_results(results: dict, output_format: str = "rich"):
    """Display analysis results in the specified format"""
    
    if not results:
        return
    
    if output_format == "json":
        print(json.dumps(results, indent=2))
        return
    
    # Initialize visualizer
    visualizer = AuditVisualizer()
    
    # Display full visual report
    visualizer.display_full_report(results)
    
    # Display code snippets for issues
    if results.get('issues'):
        console.print("\n[bold]Code Snippets with Issues:[/bold]")
        for issue in results['issues']:
            if issue.get('code_snippet'):
                console.print(Panel(
                    Syntax(issue['code_snippet'], results['language'], theme="monokai"),
                    title=f"[red]{issue['title']}[/red]",
                    subtitle=f"Severity: {issue['severity']}"
                ))

def save_report(results: dict, output_file: str):
    """Save analysis results to a file"""
    try:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        console.print(f"[green]Report saved to {output_file}")
    except Exception as e:
        console.print(f"[bold red]Error saving report: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Spectorin: Smart Contract Analysis CLI")
    parser.add_argument("file", help="Path to smart contract file")
    parser.add_argument("--language", "-l", choices=["solidity", "pyteal", "move", "rust"], 
                        help="Smart contract language (defaults to detecting from file extension)")
    parser.add_argument("--memory-efficient", "-m", action="store_true",
                        help="Run in memory-efficient mode (no LLM analysis)")
    parser.add_argument("--output-format", "-o", choices=["rich", "json"], default="rich",
                        help="Output format (rich or json)")
    parser.add_argument("--save-report", "-s", help="Save report to specified file")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Enable verbose output")
    
    args = parser.parse_args()
    
    # Check if file exists
    if not os.path.isfile(args.file):
        console.print(f"[bold red]Error: File not found: {args.file}")
        return 1
    
    # Determine language from file extension if not specified
    language = args.language
    if not language:
        ext = os.path.splitext(args.file)[1].lower()
        if ext == '.sol':
            language = 'solidity'
        elif ext in ['.py', '.teal']:
            language = 'pyteal'
        elif ext == '.move':
            language = 'move'
        elif ext == '.rs':
            language = 'rust'
        else:
            console.print("[bold red]Error: Could not determine language from file extension.")
            console.print("Please specify the language with --language")
            return 1
    
    console.print(f"[bold]Spectorin Smart Contract Analyzer[/bold]")
    console.print(f"Analyzing [cyan]{args.file}[/cyan] as [yellow]{language}[/yellow]")
    if args.memory_efficient:
        console.print("[yellow]Running in memory-efficient mode[/yellow]")
    
    results = analyze_contract(args.file, language, args.memory_efficient, args.output_format)
    
    if results:
        display_results(results, args.output_format)
        
        if args.save_report:
            save_report(results, args.save_report)
        
        # Exit with status code based on severity of issues
        if any(issue.get('severity') == Severity.CRITICAL.value for issue in results.get('issues', [])):
            return 2  # Critical issues found
        elif any(issue.get('severity') == Severity.HIGH.value for issue in results.get('issues', [])):
            return 1  # High severity issues found
        return 0  # No critical/high issues
    
    return 1

if __name__ == "__main__":
    sys.exit(main()) 