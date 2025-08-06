"""
Security Agent for Crew AI using OWASP ZAP tool.
"""

from typing import List, Optional

try:
    from crewai import Agent
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False
    # Create a minimal Agent class for testing
    class Agent:
        def __init__(self, role=None, goal=None, backstory=None, tools=None, verbose=True, allow_delegation=False):
            self.role = role
            self.goal = goal
            self.backstory = backstory
            self.tools = tools
            self.verbose = verbose
            self.allow_delegation = allow_delegation

from ..tools.zap_tool import ZAPTool


class SecurityAgent:
    """
    A specialized Crew AI agent for security testing using OWASP ZAP.
    """
    
    def __init__(self, zap_tool: Optional[ZAPTool] = None):
        """
        Initialize SecurityAgent.
        
        Args:
            zap_tool: Optional ZAP tool instance. If None, creates a new one.
        """
        self.zap_tool = zap_tool or ZAPTool()
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create the security agent with ZAP tool."""
        return Agent(
            role="Security Testing Specialist",
            goal="Perform comprehensive security testing using OWASP ZAP to identify vulnerabilities and security issues",
            backstory="""You are an expert security testing specialist with deep knowledge of web application security.
            You use OWASP ZAP to perform thorough security assessments including:
            - Active vulnerability scanning
            - Passive security analysis
            - Web application crawling and discovery
            - Security report generation and analysis
            
            You provide detailed insights about security findings and actionable recommendations.""",
            tools=[self.zap_tool],
            verbose=True,
            allow_delegation=False
        )
    
    def get_agent(self) -> Agent:
        """Get the configured security agent."""
        return self.agent
    
    def create_security_scan_task(self, target_url: str, scan_type: str = "full") -> str:
        """
        Create a task description for security scanning.
        
        Args:
            target_url: URL to scan
            scan_type: Type of scan to perform
        
        Returns:
            Task description string
        """
        return f"""
        Perform a comprehensive security scan of the target URL: {target_url}
        
        Scan requirements:
        1. Execute a {scan_type} security scan using OWASP ZAP
        2. Analyze all discovered vulnerabilities and security issues
        3. Categorize findings by severity (High, Medium, Low, Informational)
        4. Generate a detailed security report
        5. Provide actionable recommendations for each finding
        
        Focus areas:
        - SQL Injection vulnerabilities
        - Cross-Site Scripting (XSS)
        - Authentication and session management issues
        - Security misconfigurations
        - Input validation problems
        - OWASP Top 10 vulnerabilities
        
        Deliverables:
        - Complete vulnerability assessment report
        - Risk-prioritized findings list
        - Remediation recommendations
        - Security posture summary
        """
    
    def create_compliance_scan_task(self, target_url: str, standard: str = "OWASP") -> str:
        """
        Create a task for compliance-focused security scanning.
        
        Args:
            target_url: URL to scan
            standard: Compliance standard to check against
        
        Returns:
            Task description string
        """
        return f"""
        Perform a compliance-focused security assessment of {target_url} against {standard} standards.
        
        Assessment requirements:
        1. Execute comprehensive security scans using OWASP ZAP
        2. Map findings to {standard} compliance requirements
        3. Identify gaps in security controls
        4. Assess overall compliance posture
        
        Focus on {standard} requirements:
        - Security control implementation
        - Vulnerability management
        - Access controls and authentication
        - Data protection measures
        - Security monitoring capabilities
        
        Deliverables:
        - Compliance gap analysis
        - Control effectiveness assessment
        - Remediation roadmap
        - Executive summary of compliance status
        """