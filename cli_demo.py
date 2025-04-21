#!/usr/bin/env python3
import argparse
import json
import os
import requests
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress

console = Console()

def analyze_contract(file_path, language):
    """Analyze a smart contract file using the Spectorin API"""
    
    # Read the file
    with open(file_path, 'r') as f:
        code = f.read()
    
    # Show progress
    with Progress() as progress:
        task = progress.add_task(f"[green]Analyzing {os.path.basename(file_path)}...", total=100)
        
        # Simulate analysis steps
        progress.update(task, advance=25, description="[green]Reading code...")
        progress.update(task, advance=25, description="[green]Analyzing patterns...")
        
        try:
            # Send to API
            response = requests.post(
                "http://localhost:8000/api/analyze",
                json={"code": code, "language": language},
                timeout=10
            )
            
            # Process the response
            progress.update(task, advance=25, description="[green]Generating recommendations...")
            
            if response.status_code != 200:
                console.print(f"\n[bold red]Error: API returned status code {response.status_code}")
                return None
                
            progress.update(task, advance=25, description="[green]Finalizing results...")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            console.print(f"\n[bold red]Error connecting to API: {str(e)}")
            console.print("[yellow]Make sure the API server is running with: poetry run uvicorn api.main:app --port 8000")
            return None

def display_results(results):
    """Display analysis results in a nice format"""
    
    if not results:
        return
    
    # Show security score
    score = results.get("score", 0)
    score_color = "green" if score >= 80 else "yellow" if score >= 60 else "red"
    
    console.print("\n")
    console.print(Panel(f"[bold white]Security Score: [bold {score_color}]{score}/100", 
                       title="Analysis Results", 
                       border_style=score_color))
    
    # List issues found
    if "issues" in results and results["issues"]:
        console.print("\n[bold white]Issues Found:")
        
        table = Table(show_header=True)
        table.add_column("Severity", style="bold")
        table.add_column("Line")
        table.add_column("Description")
        
        for issue in results["issues"]:
            severity = issue.get("severity", "").lower()
            severity_color = "red" if severity == "high" else "yellow" if severity == "medium" else "blue"
            
            table.add_row(
                f"[{severity_color}]{severity.upper()}",
                str(issue.get("line", "?")),
                issue.get("message", "Unknown issue")
            )
        
        console.print(table)
    else:
        console.print("\n[green]✓ No issues found")
    
    # Show recommendations
    if "recommendations" in results and results["recommendations"]:
        console.print("\n[bold white]Recommendations:")
        for i, rec in enumerate(results["recommendations"], 1):
            console.print(f"  [cyan]{i}.[/cyan] {rec}")
    
    # Show summary
    if "summary" in results:
        console.print(f"\n[italic]{results['summary']}[/italic]")

def main():
    parser = argparse.ArgumentParser(description="Spectorin: Smart Contract Analysis CLI")
    parser.add_argument("file", help="Path to smart contract file")
    parser.add_argument("--language", "-l", choices=["solidity", "pyteal", "move", "rust"], 
                        help="Smart contract language (defaults to detecting from file extension)")
    
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
    
    results = analyze_contract(args.file, language)
    display_results(results)
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 