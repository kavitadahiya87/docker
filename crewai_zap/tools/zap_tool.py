"""
OWASP ZAP tool for Crew AI agent workflows.
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

try:
    from zapv2 import ZAPv2
    ZAP_AVAILABLE = True
except ImportError:
    ZAP_AVAILABLE = False
    ZAPv2 = None

try:
    from crewai_tools import BaseTool
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False
    # Create a minimal BaseTool for testing
    class BaseTool:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

from pydantic import Field

from ..utils.config import ZAPConfig


class ZAPTool(BaseTool):
    """
    OWASP ZAP tool for security scanning in Crew AI agent workflows.
    
    This tool provides comprehensive security scanning capabilities including:
    - Active scanning for vulnerabilities
    - Passive scanning during crawling
    - Spider/crawling functionality
    - Report generation and result storage
    """
    
    name: str = "OWASP ZAP Security Scanner"
    description: str = "Performs security scanning using OWASP ZAP including active/passive scans, spidering, and vulnerability reporting"
    
    config: ZAPConfig = Field(default_factory=ZAPConfig.from_env)
    zap: Optional[ZAPv2] = Field(default=None, exclude=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._initialize_zap()
    
    def _initialize_zap(self) -> None:
        """Initialize ZAP connection."""
        if not ZAP_AVAILABLE:
            print("❌ ZAP library not available. Install python-owasp-zap-v2 package.")
            self.zap = None
            return
            
        try:
            self.zap = ZAPv2(
                proxies={
                    'http': self.config.proxy_url,
                    'https': self.config.proxy_url
                },
                apikey=self.config.api_key
            )
            # Test connection
            self.zap.core.version()
            print(f"✅ Connected to ZAP at {self.config.proxy_url}")
        except Exception as e:
            print(f"❌ Failed to connect to ZAP: {e}")
            print(f"Make sure ZAP is running at {self.config.proxy_url}")
            self.zap = None
    
    def _ensure_zap_connected(self) -> bool:
        """Ensure ZAP is connected and ready."""
        if self.zap is None:
            self._initialize_zap()
        return self.zap is not None
    
    def _run(self, target_url: str, scan_type: str = "full", **kwargs) -> str:
        """
        Execute ZAP security scan.
        
        Args:
            target_url: URL to scan
            scan_type: Type of scan ('spider', 'active', 'passive', 'full')
            **kwargs: Additional scan parameters
        
        Returns:
            Scan results as JSON string
        """
        if not self._ensure_zap_connected():
            return json.dumps({
                "error": "ZAP connection failed",
                "message": "Could not connect to OWASP ZAP. Ensure ZAP is running."
            })
        
        self.config.ensure_results_dir()
        
        try:
            result = {}
            scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if scan_type in ["spider", "full"]:
                result["spider"] = self._spider_scan(target_url, scan_id)
            
            if scan_type in ["active", "full"]:
                result["active_scan"] = self._active_scan(target_url, scan_id)
            
            if scan_type in ["passive", "full"]:
                result["passive_scan"] = self._get_passive_scan_results(target_url)
            
            # Generate report
            report_path = self._generate_report(target_url, scan_id)
            result["report_path"] = report_path
            result["scan_id"] = scan_id
            result["timestamp"] = datetime.now().isoformat()
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return json.dumps({
                "error": str(e),
                "message": "Scan execution failed"
            })
    
    def _spider_scan(self, target_url: str, scan_id: str) -> Dict[str, Any]:
        """Perform spider/crawling scan."""
        print(f"🕷️  Starting spider scan for {target_url}")
        
        # Start spider
        spider_id = self.zap.spider.scan(target_url, maxchildren=self.config.spider_max_depth)
        
        # Wait for spider to complete
        while int(self.zap.spider.status(spider_id)) < 100:
            print(f"Spider progress: {self.zap.spider.status(spider_id)}%")
            time.sleep(2)
        
        print("✅ Spider scan completed")
        
        # Get spider results
        urls_found = self.zap.spider.results(spider_id)
        
        return {
            "spider_id": spider_id,
            "urls_found": len(urls_found),
            "urls": urls_found[:10],  # First 10 URLs for summary
            "status": "completed"
        }
    
    def _active_scan(self, target_url: str, scan_id: str) -> Dict[str, Any]:
        """Perform active vulnerability scan."""
        print(f"🔍 Starting active scan for {target_url}")
        
        # Start active scan
        active_scan_id = self.zap.ascan.scan(target_url, policy=self.config.active_scan_policy)
        
        # Wait for active scan to complete
        while int(self.zap.ascan.status(active_scan_id)) < 100:
            print(f"Active scan progress: {self.zap.ascan.status(active_scan_id)}%")
            time.sleep(5)
        
        print("✅ Active scan completed")
        
        return {
            "scan_id": active_scan_id,
            "status": "completed"
        }
    
    def _get_passive_scan_results(self, target_url: str) -> Dict[str, Any]:
        """Get passive scan results."""
        # Wait for passive scan to complete
        while int(self.zap.pscan.records_to_scan()) > 0:
            print(f"Passive scan remaining: {self.zap.pscan.records_to_scan()} records")
            time.sleep(2)
        
        return {
            "status": "completed",
            "records_scanned": "all"
        }
    
    def _generate_report(self, target_url: str, scan_id: str) -> str:
        """Generate scan report."""
        print(f"📄 Generating {self.config.report_format} report")
        
        # Generate report based on format
        if self.config.report_format.lower() == "html":
            report_content = self.zap.core.htmlreport()
            extension = "html"
        elif self.config.report_format.lower() == "xml":
            report_content = self.zap.core.xmlreport()
            extension = "xml"
        else:  # json
            alerts = self.zap.core.alerts()
            report_content = json.dumps(alerts, indent=2)
            extension = "json"
        
        # Save report
        report_filename = f"zap_report_{scan_id}.{extension}"
        report_path = Path(self.config.results_dir) / report_filename
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✅ Report saved to {report_path}")
        return str(report_path)
    
    def get_alerts(self, severity: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get security alerts from ZAP.
        
        Args:
            severity: Filter by severity (High, Medium, Low, Informational)
        
        Returns:
            List of security alerts
        """
        if not self._ensure_zap_connected():
            return []
        
        try:
            all_alerts = self.zap.core.alerts()
            
            if severity:
                filtered_alerts = [
                    alert for alert in all_alerts 
                    if alert.get('risk', '').lower() == severity.lower()
                ]
                return filtered_alerts
            
            return all_alerts
        except Exception as e:
            print(f"Error getting alerts: {e}")
            return []
    
    def get_scan_summary(self) -> Dict[str, Any]:
        """Get summary of scan results."""
        if not self._ensure_zap_connected():
            return {"error": "ZAP not connected"}
        
        try:
            alerts = self.zap.core.alerts()
            
            # Categorize by risk level
            risk_summary = {"High": 0, "Medium": 0, "Low": 0, "Informational": 0}
            
            for alert in alerts:
                risk_level = alert.get('risk', 'Informational')
                if risk_level in risk_summary:
                    risk_summary[risk_level] += 1
            
            return {
                "total_alerts": len(alerts),
                "risk_breakdown": risk_summary,
                "urls_tested": len(self.zap.core.urls())
            }
        except Exception as e:
            return {"error": str(e)}