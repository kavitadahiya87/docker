from setuptools import setup, find_packages

setup(
    name="crewai-zap-integration",
    version="0.1.0",
    description="OWASP ZAP tool integration for Crew AI agent workflows",
    packages=find_packages(),
    install_requires=[
        "crewai>=0.22.0",
        "python-owasp-zap-v2>=0.0.21",
        "requests>=2.31.0",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8+",
    ],
)