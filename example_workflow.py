"""
Example Crew AI workflow using OWASP ZAP integration.

This example demonstrates how to use the ZAP tool in a Crew AI agent workflow
for security testing and vulnerability assessment.
"""

import os
from crewai import Crew, Task
from crewai_zap import ZAPTool, SecurityAgent, ZAPConfig


def create_security_testing_crew(target_url: str) -> Crew:
    """
    Create a security testing crew with OWASP ZAP integration.
    
    Args:
        target_url: Target URL to scan for security vulnerabilities
    
    Returns:
        Configured Crew instance
    """
    
    # Initialize ZAP tool with configuration
    zap_config = ZAPConfig.from_env()
    zap_tool = ZAPTool(config=zap_config)
    
    # Create security agent
    security_agent = SecurityAgent(zap_tool=zap_tool)
    
    # Define security scanning task
    security_scan_task = Task(
        description=security_agent.create_security_scan_task(target_url, "full"),
        agent=security_agent.get_agent(),
        expected_output="""
        A comprehensive security assessment report containing:
        1. Executive summary of security posture
        2. Detailed vulnerability findings with severity ratings
        3. Technical details for each security issue
        4. Prioritized remediation recommendations
        5. Security best practices guidance
        """
    )
    
    # Create and return the crew
    return Crew(
        agents=[security_agent.get_agent()],
        tasks=[security_scan_task],
        verbose=True
    )


def create_compliance_testing_crew(target_url: str, compliance_standard: str = "OWASP") -> Crew:
    """
    Create a compliance-focused security testing crew.
    
    Args:
        target_url: Target URL to assess for compliance
        compliance_standard: Compliance standard to check against
    
    Returns:
        Configured Crew instance for compliance testing
    """
    
    # Initialize components
    zap_config = ZAPConfig.from_env()
    zap_tool = ZAPTool(config=zap_config)
    security_agent = SecurityAgent(zap_tool=zap_tool)
    
    # Define compliance assessment task
    compliance_task = Task(
        description=security_agent.create_compliance_scan_task(target_url, compliance_standard),
        agent=security_agent.get_agent(),
        expected_output=f"""
        A detailed compliance assessment report including:
        1. {compliance_standard} compliance status overview
        2. Gap analysis against {compliance_standard} requirements
        3. Security control effectiveness evaluation
        4. Risk assessment and prioritization
        5. Compliance roadmap and timeline
        6. Implementation recommendations
        """
    )
    
    return Crew(
        agents=[security_agent.get_agent()],
        tasks=[compliance_task],
        verbose=True
    )


def run_security_assessment(target_url: str) -> str:
    """
    Run a complete security assessment workflow.
    
    Args:
        target_url: URL to assess
    
    Returns:
        Assessment results
    """
    print(f"🔒 Starting security assessment for: {target_url}")
    print("=" * 60)
    
    try:
        # Create security testing crew
        crew = create_security_testing_crew(target_url)
        
        # Execute the security assessment
        result = crew.kickoff()
        
        print("\n" + "=" * 60)
        print("✅ Security assessment completed successfully!")
        print("=" * 60)
        
        return str(result)
        
    except Exception as e:
        error_msg = f"❌ Security assessment failed: {str(e)}"
        print(error_msg)
        return error_msg


def run_compliance_assessment(target_url: str, standard: str = "OWASP") -> str:
    """
    Run a compliance-focused assessment workflow.
    
    Args:
        target_url: URL to assess
        standard: Compliance standard
    
    Returns:
        Compliance assessment results
    """
    print(f"📋 Starting {standard} compliance assessment for: {target_url}")
    print("=" * 60)
    
    try:
        # Create compliance testing crew
        crew = create_compliance_testing_crew(target_url, standard)
        
        # Execute the compliance assessment
        result = crew.kickoff()
        
        print("\n" + "=" * 60)
        print(f"✅ {standard} compliance assessment completed!")
        print("=" * 60)
        
        return str(result)
        
    except Exception as e:
        error_msg = f"❌ Compliance assessment failed: {str(e)}"
        print(error_msg)
        return error_msg


if __name__ == "__main__":
    """
    Example usage of the OWASP ZAP integration.
    
    Make sure to:
    1. Start OWASP ZAP proxy (default: http://127.0.0.1:8080)
    2. Set environment variables in .env file
    3. Install required dependencies: pip install -r requirements.txt
    """
    
    # Example target URL (use a test application)
    target_url = "http://testphp.vulnweb.com/"
    
    print("🚀 OWASP ZAP + Crew AI Security Assessment Demo")
    print("=" * 60)
    
    # Test ZAP tool directly
    print("\n1. Testing ZAP tool connection...")
    zap_tool = ZAPTool()
    if zap_tool.zap:
        print("✅ ZAP tool initialized successfully")
        
        # Get current scan summary
        summary = zap_tool.get_scan_summary()
        print(f"📊 Current ZAP status: {summary}")
    else:
        print("❌ ZAP tool initialization failed")
        print("Please ensure OWASP ZAP is running at the configured address")
        exit(1)
    
    # Run security assessment
    print("\n2. Running security assessment workflow...")
    security_results = run_security_assessment(target_url)
    
    # Run compliance assessment
    print("\n3. Running compliance assessment workflow...")
    compliance_results = run_compliance_assessment(target_url, "OWASP")
    
    print("\n🎯 Assessment workflows completed!")
    print("Check the generated reports in the configured results directory.")