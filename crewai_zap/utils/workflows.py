"""
Workflow configurations for different security testing scenarios.
"""

from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class WorkflowConfig:
    """Configuration for security testing workflows."""
    
    name: str
    scan_type: str
    targets: List[str]
    parameters: Dict[str, Any]
    

# Predefined workflow configurations
WORKFLOW_CONFIGS = {
    "quick_security_check": WorkflowConfig(
        name="Quick Security Check",
        scan_type="spider",
        targets=["https://example.com"],
        parameters={
            "spider_max_depth": 3,
            "timeout": 120,
            "report_format": "json"
        }
    ),
    
    "comprehensive_security_audit": WorkflowConfig(
        name="Comprehensive Security Audit",
        scan_type="full",
        targets=["https://example.com"],
        parameters={
            "spider_max_depth": 10,
            "timeout": 1800,
            "active_scan_policy": "Full attacks",
            "report_format": "html"
        }
    ),
    
    "api_security_test": WorkflowConfig(
        name="API Security Testing",
        scan_type="active",
        targets=["https://api.example.com"],
        parameters={
            "spider_max_depth": 5,
            "timeout": 900,
            "active_scan_policy": "API scan",
            "report_format": "xml"
        }
    ),
    
    "production_safe_scan": WorkflowConfig(
        name="Production Safe Scan",
        scan_type="passive",
        targets=["https://production.example.com"],
        parameters={
            "timeout": 300,
            "passive_scan_enabled": True,
            "report_format": "json"
        }
    ),
    
    "compliance_scan_owasp": WorkflowConfig(
        name="OWASP Compliance Scan",
        scan_type="full",
        targets=["https://webapp.example.com"],
        parameters={
            "spider_max_depth": 8,
            "timeout": 1200,
            "active_scan_policy": "OWASP compliance",
            "report_format": "html"
        }
    )
}


def get_workflow_config(workflow_name: str) -> WorkflowConfig:
    """
    Get a predefined workflow configuration.
    
    Args:
        workflow_name: Name of the workflow configuration
    
    Returns:
        WorkflowConfig object
    
    Raises:
        ValueError: If workflow name is not found
    """
    if workflow_name not in WORKFLOW_CONFIGS:
        available = ", ".join(WORKFLOW_CONFIGS.keys())
        raise ValueError(f"Workflow '{workflow_name}' not found. Available: {available}")
    
    return WORKFLOW_CONFIGS[workflow_name]


def list_available_workflows() -> List[str]:
    """
    List all available workflow configurations.
    
    Returns:
        List of workflow names
    """
    return list(WORKFLOW_CONFIGS.keys())


def create_custom_workflow(
    name: str,
    scan_type: str,
    targets: List[str],
    **parameters
) -> WorkflowConfig:
    """
    Create a custom workflow configuration.
    
    Args:
        name: Workflow name
        scan_type: Type of scan (spider, active, passive, full)
        targets: List of target URLs
        **parameters: Additional parameters
    
    Returns:
        Custom WorkflowConfig object
    """
    return WorkflowConfig(
        name=name,
        scan_type=scan_type,
        targets=targets,
        parameters=parameters
    )