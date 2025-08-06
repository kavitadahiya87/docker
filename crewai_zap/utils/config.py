"""
Configuration management for OWASP ZAP integration.
"""

import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ZAPConfig(BaseModel):
    """Configuration settings for OWASP ZAP integration."""
    
    # ZAP proxy settings
    proxy_host: str = Field(default="127.0.0.1", description="ZAP proxy host")
    proxy_port: int = Field(default=8080, description="ZAP proxy port")
    api_key: Optional[str] = Field(default=None, description="ZAP API key for authentication")
    
    # ZAP connection settings
    timeout: int = Field(default=300, description="Connection timeout in seconds")
    max_retries: int = Field(default=3, description="Maximum number of retries")
    
    # Scan settings
    spider_max_depth: int = Field(default=5, description="Maximum spider depth")
    active_scan_policy: str = Field(default="Default Policy", description="Active scan policy name")
    passive_scan_enabled: bool = Field(default=True, description="Enable passive scanning")
    
    # Results storage
    results_dir: str = Field(default="./zap_results", description="Directory to store scan results")
    report_format: str = Field(default="html", description="Report format (html, xml, json)")
    
    @classmethod
    def from_env(cls) -> "ZAPConfig":
        """Create configuration from environment variables."""
        return cls(
            proxy_host=os.getenv("ZAP_PROXY_HOST", "127.0.0.1"),
            proxy_port=int(os.getenv("ZAP_PROXY_PORT", "8080")),
            api_key=os.getenv("ZAP_API_KEY"),
            timeout=int(os.getenv("ZAP_TIMEOUT", "300")),
            max_retries=int(os.getenv("ZAP_MAX_RETRIES", "3")),
            spider_max_depth=int(os.getenv("ZAP_SPIDER_MAX_DEPTH", "5")),
            active_scan_policy=os.getenv("ZAP_ACTIVE_SCAN_POLICY", "Default Policy"),
            passive_scan_enabled=os.getenv("ZAP_PASSIVE_SCAN_ENABLED", "true").lower() == "true",
            results_dir=os.getenv("ZAP_RESULTS_DIR", "./zap_results"),
            report_format=os.getenv("ZAP_REPORT_FORMAT", "html"),
        )
    
    @property
    def proxy_url(self) -> str:
        """Get the full proxy URL."""
        return f"http://{self.proxy_host}:{self.proxy_port}"
    
    def ensure_results_dir(self) -> None:
        """Ensure the results directory exists."""
        os.makedirs(self.results_dir, exist_ok=True)