# OWASP ZAP Integration with Crew AI Agent Workflow

This project provides a comprehensive integration of the OWASP ZAP (Zed Attack Proxy) security testing tool with Crew AI agent workflows, enabling automated security testing and vulnerability assessment as part of agent-driven processes.

## Features

- **Modular ZAP Tool**: Reusable OWASP ZAP tool that can be integrated into any Crew AI agent workflow
- **Comprehensive Scanning**: Supports active scanning, passive scanning, spidering/crawling, and report generation
- **Flexible Configuration**: Environment-based configuration with sensible defaults
- **Result Storage**: Automatic storage and organization of scan results and reports
- **Security Agent**: Pre-built security specialist agent optimized for ZAP tool usage
- **Multiple Scan Types**: Support for different types of security assessments (full, targeted, compliance)
- **Report Generation**: Multiple report formats (HTML, XML, JSON) with detailed findings

## Installation

### Prerequisites

1. **OWASP ZAP**: Install and run OWASP ZAP proxy
   ```bash
   # Using Docker (recommended)
   docker run -u zap -p 8080:8080 -i owasp/zap2docker-stable zap.sh -daemon -host 0.0.0.0 -port 8080 -config api.addrs.addr.name=.* -config api.addrs.addr.regex=true
   
   # Or download from https://www.zaproxy.org/download/
   ```

2. **Python 3.8+**: Ensure you have Python 3.8 or higher installed

### Install Dependencies

```bash
# Clone the repository
git clone <repository-url>
cd docker

# Install Python dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

### Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Configure your ZAP settings in `.env`:
   ```bash
   # OWASP ZAP Configuration
   ZAP_PROXY_HOST=127.0.0.1
   ZAP_PROXY_PORT=8080
   ZAP_API_KEY=your_api_key_here
   
   # Optional: ZAP Docker configuration
   ZAP_DOCKER_IMAGE=owasp/zap2docker-stable
   ZAP_DOCKER_PORT=8080
   ```

## Usage

### Quick Start

```python
from crewai_zap import ZAPTool, SecurityAgent, ZAPConfig

# Initialize ZAP tool
zap_tool = ZAPTool()

# Create security agent
security_agent = SecurityAgent(zap_tool=zap_tool)

# Use in your Crew AI workflow
agent = security_agent.get_agent()
```

### Basic Security Scan

```python
from crewai import Crew, Task
from crewai_zap import ZAPTool, SecurityAgent

# Create security testing setup
zap_tool = ZAPTool()
security_agent = SecurityAgent(zap_tool=zap_tool)

# Define security scan task
task = Task(
    description=security_agent.create_security_scan_task("https://example.com", "full"),
    agent=security_agent.get_agent(),
    expected_output="Comprehensive security assessment report"
)

# Create and run crew
crew = Crew(agents=[security_agent.get_agent()], tasks=[task])
result = crew.kickoff()
```

### Direct Tool Usage

```python
from crewai_zap import ZAPTool

# Initialize tool
zap_tool = ZAPTool()

# Perform different types of scans
spider_result = zap_tool._run("https://example.com", scan_type="spider")
active_scan_result = zap_tool._run("https://example.com", scan_type="active") 
full_scan_result = zap_tool._run("https://example.com", scan_type="full")

# Get scan summary
summary = zap_tool.get_scan_summary()
print(f"Total alerts: {summary['total_alerts']}")

# Get specific alerts
high_risk_alerts = zap_tool.get_alerts(severity="High")
```

### Running the Example Workflow

```bash
# Make sure ZAP is running first
docker run -u zap -p 8080:8080 -i owasp/zap2docker-stable zap.sh -daemon -host 0.0.0.0 -port 8080

# Run the example
python example_workflow.py
```

## Architecture

### Components

1. **ZAPTool (`crewai_zap.tools.zap_tool.ZAPTool`)**
   - Core integration tool for OWASP ZAP
   - Handles connection management, scanning, and result processing
   - Implements Crew AI BaseTool interface for seamless integration

2. **SecurityAgent (`crewai_zap.agents.security_agent.SecurityAgent`)**
   - Specialized Crew AI agent for security testing
   - Pre-configured with security expertise and ZAP tool
   - Provides task templates for different types of assessments

3. **ZAPConfig (`crewai_zap.utils.config.ZAPConfig`)**
   - Configuration management using Pydantic models
   - Environment variable support with defaults
   - Validation and type checking

### Integration Flow

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Crew AI       │───▶│   Security       │───▶│   OWASP ZAP     │
│   Workflow      │    │   Agent          │    │   Tool          │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │                          │
                              ▼                          ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │   Task           │    │   ZAP Proxy     │
                       │   Execution      │    │   & Scanner     │
                       └──────────────────┘    └─────────────────┘
                              │                          │
                              ▼                          ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │   Results &      │    │   Reports &     │
                       │   Analysis       │    │   Storage       │
                       └──────────────────┘    └─────────────────┘
```

## Scan Types

### 1. Spider Scan
- Crawls and discovers URLs on the target website
- Maps the application structure
- Identifies entry points for further testing

### 2. Active Scan
- Performs active vulnerability testing
- Tests for common security issues (OWASP Top 10)
- May modify application state (use with caution)

### 3. Passive Scan
- Analyzes traffic without sending additional requests
- Safe for production environments
- Identifies security issues in observed traffic

### 4. Full Scan
- Combines spider, active, and passive scanning
- Comprehensive security assessment
- Recommended for thorough testing

## Configuration Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `proxy_host` | 127.0.0.1 | ZAP proxy host address |
| `proxy_port` | 8080 | ZAP proxy port |
| `api_key` | None | ZAP API key for authentication |
| `timeout` | 300 | Connection timeout in seconds |
| `max_retries` | 3 | Maximum number of connection retries |
| `spider_max_depth` | 5 | Maximum spider crawling depth |
| `active_scan_policy` | Default Policy | Active scan policy name |
| `passive_scan_enabled` | True | Enable passive scanning |
| `results_dir` | ./zap_results | Directory for storing results |
| `report_format` | html | Report format (html/xml/json) |

## Security Considerations

1. **Production Usage**: Be cautious when running active scans against production systems
2. **API Key**: Use ZAP API key for secure communication in production environments
3. **Network Security**: Ensure ZAP proxy is properly secured and not exposed externally
4. **Scan Policies**: Configure appropriate scan policies based on your environment

## Troubleshooting

### Common Issues

1. **ZAP Connection Failed**
   ```
   ❌ Failed to connect to ZAP: Connection refused
   ```
   - Ensure ZAP is running at the configured host:port
   - Check firewall settings
   - Verify API key if authentication is enabled

2. **Scan Timeout**
   ```
   Scan execution failed: timeout
   ```
   - Increase timeout value in configuration
   - Check target URL accessibility
   - Verify ZAP proxy is responding

3. **Permission Denied**
   ```
   Permission denied: cannot write to results directory
   ```
   - Check write permissions for results directory
   - Ensure directory exists or can be created

### Debug Mode

Enable verbose logging by setting the agent to verbose mode:

```python
security_agent = SecurityAgent(zap_tool=zap_tool)
agent = security_agent.get_agent()
agent.verbose = True
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## References

- [OWASP ZAP Documentation](https://www.zaproxy.org/docs/)
- [Crew AI Documentation](https://docs.crewai.com/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [ZAP Python API](https://pypi.org/project/python-owasp-zap-v2/)