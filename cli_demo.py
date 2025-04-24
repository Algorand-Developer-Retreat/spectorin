#!/usr/bin/env python3
import argparse
import json
import os
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
from core.plugin_manager import PluginManager
from core.ai_agents.manager import AIAgentManager
from core.visualizations.audit_visualizer import AuditVisualizer

console = Console()

def analyze_contract(file_path, language, memory_efficient=False):
    """Analyze a smart contract file using the Spectorin core engine"""
    
    # Read the file
    with open(file_path, 'r') as f:
        code = f.read()
    
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
                'code': code  # Include code for metrics
            }
            
        except Exception as e:
            console.print(f"\n[bold red]Error during analysis: {str(e)}")
            return None

def display_results(results):
    """Display analysis results in a nice format"""
    
    if not results:
        return
    
    # Initialize visualizer
    visualizer = AuditVisualizer()
    
    # Display full visual report
    visualizer.display_full_report(results)

def main():
    parser = argparse.ArgumentParser(description="Spectorin: Smart Contract Analysis CLI")
    parser.add_argument("file", help="Path to smart contract file")
    parser.add_argument("--language", "-l", choices=["solidity", "pyteal", "move", "rust"], 
                        help="Smart contract language (defaults to detecting from file extension)")
    parser.add_argument("--memory-efficient", "-m", action="store_true",
                        help="Run in memory-efficient mode (no LLM analysis)")
    
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
    
    results = analyze_contract(args.file, language, args.memory_efficient)
    display_results(results)
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 