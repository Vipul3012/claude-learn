import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
import anthropic
import os
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
console = Console()

class ClaudeDevOps:
    """Claude AI Client for DevOps Operations"""
    
    def __init__(self):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("❌ ANTHROPIC_API_KEY not set!")
        
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-6"
    
    def ask(self, prompt: str, system: str = None, max_tokens: int = 2048) -> str:
        """Send a prompt to Claude and get response"""
        
        messages = [{"role": "user", "content": prompt}]
        
        kwargs = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": messages
        }
        
        if system:
            kwargs["system"] = system
        
        response = self.client.messages.create(**kwargs)
        return response.content[0].text
    
    def analyze_logs(self, log_content: str) -> str:
        system = """You are a Senior DevOps Engineer with 10+ years experience.
        Analyze logs and provide actionable insights in structured format.
        Always be specific, concise and provide actual commands to fix issues."""
        
        prompt = f"""Analyze these logs and provide DevOps report:

{log_content}

Format your response as:
## 🔴 Critical Issues
## ⚠️ Warnings  
## 🔍 Root Cause
## 🛠️ Fix Commands
## 📋 Prevention
## 📊 Health Score: X/10
"""
        return self.ask(prompt, system)
    
    def review_code(self, code: str, filename: str) -> str:
        system = """You are a DevOps/Platform Engineer expert in:
        - Infrastructure as Code (Terraform, Ansible, Helm)
        - Docker, Kubernetes, CI/CD
        - Security best practices
        - Python DevOps tooling
        Be specific and provide corrected code snippets."""
        
        prompt = f"""Review this file: {filename}

{code}

Provide:
## 🔒 Security Issues
## 🐛 Bugs Found
## ⚡ Performance Issues
## 📏 Best Practices Violations
## ✅ What's Good
## 🛠️ Improved Version (if needed)
## 📊 Code Quality Score: X/10
"""
        return self.ask(prompt, system)
    
    def scan_security(self, file_content: str, filename: str) -> str:
        system = """You are a DevSecOps expert specializing in:
        - OWASP Top 10
        - CIS Benchmarks
        - Cloud security (AWS/Azure/GCP)
        - Container security
        - Secrets detection
        Provide CVE references where applicable."""
        
        prompt = f"""Perform security scan on: {filename}

{file_content}

Report:
## 🚨 Critical Vulnerabilities
## ⚠️ Medium Risk Issues
## ℹ️ Low Risk / Info
## 🔑 Secrets/Credentials Detected
## 🛡️ Hardening Recommendations
## 📊 Security Score: X/10
"""
        return self.ask(prompt, system)
    
    def generate_runbook(self, service: str, issue: str) -> str:
        system = """You are a Site Reliability Engineer.
        Create detailed, production-ready runbooks with exact commands."""
        
        prompt = f"""Create a runbook for:
Service: {service}
Issue: {issue}

Include:
## 📋 Overview
## 🔍 Detection & Symptoms
## 🚨 Immediate Actions (first 5 minutes)
## 🔧 Step-by-Step Resolution
## ✅ Verification Steps
## 📈 Monitoring & Alerts Setup
## 🔄 Prevention
"""
        return self.ask(prompt, system)
    
