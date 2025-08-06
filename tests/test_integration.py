"""
Basic tests for OWASP ZAP integration with Crew AI.
"""

import os
import sys
import unittest
from unittest.mock import Mock, patch, MagicMock

# Add the parent directory to the path to import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crewai_zap.utils.config import ZAPConfig
from crewai_zap.tools.zap_tool import ZAPTool
from crewai_zap.agents.security_agent import SecurityAgent


class TestZAPConfig(unittest.TestCase):
    """Test ZAPConfig functionality."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = ZAPConfig()
        
        self.assertEqual(config.proxy_host, "127.0.0.1")
        self.assertEqual(config.proxy_port, 8080)
        self.assertEqual(config.timeout, 300)
        self.assertEqual(config.spider_max_depth, 5)
        self.assertTrue(config.passive_scan_enabled)
    
    def test_proxy_url(self):
        """Test proxy URL generation."""
        config = ZAPConfig(proxy_host="localhost", proxy_port=9090)
        self.assertEqual(config.proxy_url, "http://localhost:9090")
    
    def test_from_env(self):
        """Test configuration from environment variables."""
        with patch.dict(os.environ, {
            'ZAP_PROXY_HOST': 'testhost',
            'ZAP_PROXY_PORT': '9000',
            'ZAP_TIMEOUT': '600'
        }):
            config = ZAPConfig.from_env()
            self.assertEqual(config.proxy_host, "testhost")
            self.assertEqual(config.proxy_port, 9000)
            self.assertEqual(config.timeout, 600)


class TestZAPTool(unittest.TestCase):
    """Test ZAPTool functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = ZAPConfig(proxy_host="localhost", proxy_port=8080)
    
    @patch('crewai_zap.tools.zap_tool.ZAPv2')
    def test_zap_tool_initialization(self, mock_zapv2):
        """Test ZAP tool initialization."""
        # Mock ZAP connection
        mock_zap_instance = Mock()
        mock_zap_instance.core.version.return_value = "2.12.0"
        mock_zapv2.return_value = mock_zap_instance
        
        tool = ZAPTool(config=self.config)
        
        # Verify ZAP was initialized
        mock_zapv2.assert_called_once()
        self.assertIsNotNone(tool.zap)
        self.assertEqual(tool.name, "OWASP ZAP Security Scanner")
    
    @patch('crewai_zap.tools.zap_tool.ZAPv2')
    def test_zap_tool_connection_failure(self, mock_zapv2):
        """Test ZAP tool connection failure handling."""
        # Mock connection failure
        mock_zapv2.side_effect = Exception("Connection refused")
        
        tool = ZAPTool(config=self.config)
        
        # Verify graceful failure handling
        self.assertIsNone(tool.zap)
    
    @patch('crewai_zap.tools.zap_tool.ZAPv2')
    def test_get_scan_summary(self, mock_zapv2):
        """Test scan summary functionality."""
        # Mock ZAP responses
        mock_zap_instance = Mock()
        mock_zap_instance.core.version.return_value = "2.12.0"
        mock_zap_instance.core.alerts.return_value = [
            {'risk': 'High', 'name': 'SQL Injection'},
            {'risk': 'Medium', 'name': 'XSS'},
            {'risk': 'Low', 'name': 'Information Disclosure'}
        ]
        mock_zap_instance.core.urls.return_value = ['http://example.com', 'http://example.com/page1']
        mock_zapv2.return_value = mock_zap_instance
        
        tool = ZAPTool(config=self.config)
        summary = tool.get_scan_summary()
        
        # Verify summary structure
        self.assertEqual(summary['total_alerts'], 3)
        self.assertEqual(summary['risk_breakdown']['High'], 1)
        self.assertEqual(summary['risk_breakdown']['Medium'], 1)
        self.assertEqual(summary['risk_breakdown']['Low'], 1)
        self.assertEqual(summary['urls_tested'], 2)
    
    @patch('crewai_zap.tools.zap_tool.ZAPv2')
    def test_get_alerts_filtered(self, mock_zapv2):
        """Test filtered alerts retrieval."""
        # Mock ZAP responses
        mock_zap_instance = Mock()
        mock_zap_instance.core.version.return_value = "2.12.0"
        mock_zap_instance.core.alerts.return_value = [
            {'risk': 'High', 'name': 'SQL Injection'},
            {'risk': 'Medium', 'name': 'XSS'},
            {'risk': 'High', 'name': 'CSRF'}
        ]
        mock_zapv2.return_value = mock_zap_instance
        
        tool = ZAPTool(config=self.config)
        high_alerts = tool.get_alerts(severity="High")
        
        # Verify filtering
        self.assertEqual(len(high_alerts), 2)
        for alert in high_alerts:
            self.assertEqual(alert['risk'], 'High')


class TestSecurityAgent(unittest.TestCase):
    """Test SecurityAgent functionality."""
    
    @patch('crewai_zap.tools.zap_tool.ZAPv2')
    def test_security_agent_creation(self, mock_zapv2):
        """Test security agent creation."""
        # Mock ZAP
        mock_zap_instance = Mock()
        mock_zap_instance.core.version.return_value = "2.12.0"
        mock_zapv2.return_value = mock_zap_instance
        
        agent = SecurityAgent()
        
        # Verify agent configuration
        self.assertIsNotNone(agent.zap_tool)
        self.assertIsNotNone(agent.agent)
        self.assertEqual(agent.agent.role, "Security Testing Specialist")
    
    def test_security_scan_task_creation(self):
        """Test security scan task description creation."""
        with patch('crewai_zap.tools.zap_tool.ZAPv2'):
            agent = SecurityAgent()
            task_desc = agent.create_security_scan_task("https://example.com", "full")
            
            # Verify task description contains key elements
            self.assertIn("https://example.com", task_desc)
            self.assertIn("full security scan", task_desc)
            self.assertIn("OWASP ZAP", task_desc)
            self.assertIn("vulnerability", task_desc)
    
    def test_compliance_scan_task_creation(self):
        """Test compliance scan task description creation."""
        with patch('crewai_zap.tools.zap_tool.ZAPv2'):
            agent = SecurityAgent()
            task_desc = agent.create_compliance_scan_task("https://example.com", "OWASP")
            
            # Verify task description contains compliance elements
            self.assertIn("https://example.com", task_desc)
            self.assertIn("OWASP", task_desc)
            self.assertIn("compliance", task_desc)
            self.assertIn("gap analysis", task_desc)


if __name__ == "__main__":
    """
    Run the test suite.
    
    Usage:
        python -m pytest tests/test_integration.py -v
        # or
        python tests/test_integration.py
    """
    unittest.main(verbosity=2)