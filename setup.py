from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="smart-contract-cfg",
    version="1.0.0",
    author="NT547 Team",
    description="Control Flow Graph (CFG) Visualization Tool for Smart Contracts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "solidity-parser>=0.1.1",
        "graphviz>=0.20",
        "networkx>=2.8",
        "py-solc-x>=1.1.1",
        "slither-analyzer>=0.9.0",
    ],
    entry_points={
        "console_scripts": [
            "cfg-visualizer=cfg_visualizer.cli:main",
        ],
    },
)
