import typer
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from datetime import datetime
from claude_client import ClaudeDevOps

app = typer.Typer()
console = Console()

# File extensions to scan
SCANNABLE = [
    '.py', '.yml', '.yaml', '.tf', '.json',
    '.sh', '.bash', '.dockerfile', '.env.example',
    'Dockerfile', 'docker-compose.yml'
]

@app.command()
def scan(
    path: str = typer.Argument(".", help="File or directory to scan"),
    save_report: bool = typer.Option(False, "--save", "-s")
):
    """🔒 Security scan using Claude AI"""
    
    console.print(Panel.fit(
        "[bold red]🔒 DevOps AI Security Scanner[/bold red]\n[dim]Powered by Claude AI[/dim]",
        border_style="red"
    ))
    
    scan_path = Path(path)
    files_to_scan = []
    
    if scan_path.is_file():
        files_to_scan = [scan_path]
    else:
        for ext in SCANNABLE:
            files_to_scan.extend(scan_path.rglob(f"*{ext}"))
        # Exclude hidden dirs and venv
        files_to_scan = [
            f for f in files_to_scan 
            if '.git' not in str(f) 
            and 'venv' not in str(f)
            and '__pycache__' not in str(f)
        ]
    
    if not files_to_scan:
        console.print("[yellow]No scannable files found[/yellow]")
        return
    
    # Show files table
    table = Table(title="Files to Scan")
    table.add_column("File", style="cyan")
    table.add_column("Size", style="green")
    for f in files_to_scan:
        table.add_row(str(f), f"{f.stat().st_size} bytes")
    console.print(table)
    
    claude = ClaudeDevOps()
    all_results = []
    
    for file_path in files_to_scan:
        console.print(f"\n[yellow]🔍 Scanning:[/yellow] {file_path}")
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            if len(content.strip()) == 0:
                continue
                
            result = claude.scan_security(content, str(file_path))
            all_results.append({"file": str(file_path), "result": result})
            
            console.print(Panel(
                Markdown(result),
                title=f"[bold red]🔒 {file_path.name}[/bold red]",
                border_style="red"
            ))
        except Exception as e:
            console.print(f"[red]Error scanning {file_path}: {e}[/red]")
    
    # Save report
    if save_report and all_results:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"reports/security_report_{timestamp}.md"
        os.makedirs("reports", exist_ok=True)
        with open(report_path, "w") as f:
            f.write(f"# Security Scan Report\nGenerated: {datetime.now()}\n\n")
            for r in all_results:
                f.write(f"## File: {r['file']}\n{r['result']}\n\n---\n\n")
        console.print(f"\n[green]💾 Report saved:[/green] {report_path}")

if __name__ == "__main__":
    app()