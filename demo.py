#!/usr/bin/env python3
"""
Basic functionality demo for OWASP ZAP integration with Crew AI.

This script demonstrates the basic structure and functionality of the integration
even without OWASP ZAP or Crew AI fully installed.
"""

import json
from crewai_zap import ZAPTool, SecurityAgent, ZAPConfig


def demo_configuration():
    """Demonstrate configuration management."""
    print("🔧 Configuration Demo")
    print("=" * 50)
    
    # Test default configuration
    config = ZAPConfig()
    print(f"Default proxy URL: {config.proxy_url}")
    print(f"Default timeout: {config.timeout} seconds")
    print(f"Default spider depth: {config.spider_max_depth}")
    print(f"Results directory: {config.results_dir}")
    
    # Test custom configuration
    custom_config = ZAPConfig(
        proxy_host="localhost",
        proxy_port=9090,
        timeout=600,
        spider_max_depth=10
    )
    print(f"\nCustom proxy URL: {custom_config.proxy_url}")
    print(f"Custom timeout: {custom_config.timeout} seconds")
    print()


def demo_zap_tool():
    """Demonstrate ZAP tool functionality."""
    print("🔍 ZAP Tool Demo")
    print("=" * 50)
    
    # Initialize ZAP tool
    zap_tool = ZAPTool()
    print(f"Tool name: {zap_tool.name}")
    print(f"Tool description: {zap_tool.description}")
    
    # Demonstrate graceful handling when ZAP is not available
    if not zap_tool.zap:
        print("✅ Tool handles missing ZAP connection gracefully")
        
        # Simulate scan result for demo
        demo_result = {
            "error": "ZAP connection failed",
            "message": "Could not connect to OWASP ZAP. Ensure ZAP is running.",
            "demo_mode": True
        }
        print(f"Demo scan result: {json.dumps(demo_result, indent=2)}")
    else:
        print("✅ ZAP connection established")
    print()


def demo_security_agent():
    """Demonstrate security agent functionality."""
    print("👨‍💻 Security Agent Demo")
    print("=" * 50)
    
    # Create security agent
    security_agent = SecurityAgent()
    agent = security_agent.get_agent()
    
    print(f"Agent role: {agent.role}")
    print(f"Agent tools: {len(agent.tools)} tool(s) available")
    
    # Demonstrate task creation
    target_url = "https://example.com"
    security_task = security_agent.create_security_scan_task(target_url, "full")
    
    print(f"\nSample security scan task for {target_url}:")
    print("-" * 30)
    print(security_task[:200] + "..." if len(security_task) > 200 else security_task)
    
    # Demonstrate compliance task creation
    compliance_task = security_agent.create_compliance_scan_task(target_url, "OWASP")
    
    print(f"\nSample compliance task for {target_url}:")
    print("-" * 30)
    print(compliance_task[:200] + "..." if len(compliance_task) > 200 else compliance_task)
    print()


def demo_workflow_structure():
    """Demonstrate workflow structure."""
    print("🔄 Workflow Structure Demo")
    print("=" * 50)
    
    print("Integration Components:")
    print("1. ✅ ZAPConfig - Configuration management")
    print("2. ✅ ZAPTool - OWASP ZAP integration tool")
    print("3. ✅ SecurityAgent - Specialized Crew AI agent")
    print("4. ✅ Example workflows - Ready-to-use templates")
    
    print("\nSupported Scan Types:")
    print("- 🕷️  Spider: Web crawling and URL discovery")
    print("- 🔍 Active: Vulnerability testing (use with caution)")
    print("- 👁️  Passive: Safe traffic analysis")
    print("- 🎯 Full: Comprehensive security assessment")
    
    print("\nReport Formats:")
    print("- 📄 HTML: Human-readable reports")
    print("- 📋 XML: Structured data format")
    print("- 📊 JSON: API-friendly format")
    
    print("\nKey Features:")
    print("- ⚙️  Modular design for reusability")
    print("- 🔒 Secure configuration management")
    print("- 📁 Automatic result storage")
    print("- 🛡️  Production-safe options")
    print("- 📚 Comprehensive documentation")
    print()


def main():
    """Run the complete demo."""
    print("🚀 OWASP ZAP + Crew AI Integration Demo")
    print("=" * 60)
    print("This demo shows the structure and functionality of the integration")
    print("even without OWASP ZAP or Crew AI fully installed.\n")
    
    try:
        demo_configuration()
        demo_zap_tool() 
        demo_security_agent()
        demo_workflow_structure()
        
        print("✅ Demo completed successfully!")
        print("\nNext Steps:")
        print("1. Install OWASP ZAP: docker run -p 8080:8080 owasp/zap2docker-stable")
        print("2. Install Crew AI: pip install crewai")
        print("3. Install ZAP Python API: pip install python-owasp-zap-v2")
        print("4. Run: python example_workflow.py")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())