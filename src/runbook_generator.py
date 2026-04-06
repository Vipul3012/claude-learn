import typer
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
import os
from datetime import datetime
from claude_client import ClaudeDevOps

app = typer.Typer()
console = Console()

@app.command()
def generate(
    service: str = typer.Option(..., "--service", "-svc", prompt="Service name"),
    issue: str = typer.Option(..., "--issue", "-i", prompt="Describe the issue"),
    save: bool = typer.Option(True, "--save", "-s", help="Save runbook")
):
    """📋 Generate runbooks using Claude AI"""
    
    console.print(Panel.fit(
        "[bold magenta]📋 AI Runbook Generator[/bold magenta]\n[dim]Powered by Claude AI[/dim]",
        border_style="magenta"
    ))
    
    console.print(f"\n[yellow]🧠 Generating runbook for:[/yellow] {service} - {issue}\n")
    
    try:
        claude = ClaudeDevOps()
        result = claude.generate_runbook(service, issue)
        
        console.print(Panel(
            Markdown(result),
            title=f"[bold magenta]📋 Runbook: {service}[/bold magenta]",
            border_style="magenta"
        ))
        
        if save:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            service_slug = service.lower().replace(" ", "_")
            runbook_path = f"../docs/runbook_{service_slug}_{timestamp}.md"
            os.makedirs("../docs", exist_ok=True)
            
            with open(runbook_path, "w") as f:
                f.write(f"# Runbook: {service}\n")
                f.write(f"**Issue:** {issue}\n")
                f.write(f"**Generated:** {datetime.now()}\n\n")
                f.write(result)
            
            console.print(f"\n[green]💾 Runbook saved:[/green] {runbook_path}")
            
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")

if __name__ == "__main__":
    app()