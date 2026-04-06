import typer
import sys
import os

# Fix Windows encoding issue
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from datetime import datetime
from claude_client import ClaudeDevOps

app = typer.Typer()
console = Console()

SAMPLE_LOGS = """
2024-01-15 10:23:01 ERROR Connection refused to database host db-prod-01:5432
2024-01-15 10:23:01 ERROR Failed to connect after 3 retries
2024-01-15 10:23:02 WARN  Memory usage at 87% on node worker-03
2024-01-15 10:23:05 ERROR OOMKilled: container app-server on pod app-7d9f8b-xkp2q
2024-01-15 10:23:06 INFO  Pod app-7d9f8b-xkp2q restarting (restart count: 5)
2024-01-15 10:23:10 ERROR Disk usage 95% on /var/log partition
2024-01-15 10:23:15 WARN  High latency detected: API response 8500ms (threshold: 2000ms)
2024-01-15 10:23:20 ERROR SSL Certificate expires in 3 days for api.example.com
2024-01-15 10:23:25 FATAL Kubernetes node worker-03 NotReady
"""

@app.command()
def analyze(
    log_file: str = typer.Argument(None, help="Path to log file"),
    save_report: bool = typer.Option(False, "--save", "-s", help="Save report to file")
):
    """🔍 Analyze logs using Claude AI"""
    
    console.print(Panel.fit(
        "[bold cyan]🤖 DevOps AI Log Analyzer[/bold cyan]\n[dim]Powered by Claude AI[/dim]",
        border_style="cyan"
    ))
    
    # Get log content
    if log_file:
        path = Path(log_file)
        if not path.exists():
            console.print(f"[red]❌ File not found: {log_file}[/red]")
            raise typer.Exit(1)
        log_content = path.read_text()
        console.print(f"[green]📂 Loaded:[/green] {log_file}")
    elif not sys.stdin.isatty():
        log_content = sys.stdin.read()
        console.print("[green]📥 Reading from stdin...[/green]")
    else:
        log_content = SAMPLE_LOGS
        console.print("[yellow]⚠️  Using sample logs (pass a file or pipe logs)[/yellow]")
    
    console.print("\n[bold yellow]🧠 Claude is analyzing...[/bold yellow]\n")
    
    try:
        claude = ClaudeDevOps()
        result = claude.analyze_logs(log_content)
        
        # Display result
        console.print(Panel(
            Markdown(result),
            title="[bold green]📊 Analysis Report[/bold green]",
            border_style="green"
        ))
        
        # Save report
        if save_report:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = f"reports/log_report_{timestamp}.md"
            os.makedirs("reports", exist_ok=True)
            with open(report_path, "w") as f:
                f.write(f"# Log Analysis Report\nGenerated: {datetime.now()}\n\n{result}")
            console.print(f"\n[green]💾 Report saved:[/green] {report_path}")
            
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()