@echo off
echo Creating project structure...

mkdir src
mkdir src\environment
mkdir src\agents
mkdir src\training
mkdir src\inference
mkdir src\data
mkdir src\monitoring
mkdir notebooks
mkdir tests
mkdir tests\unit
mkdir tests\integration

echo Creating __init__.py files...
type nul > src\__init__.py
type nul > src\environment\__init__.py
type nul > src\agents\__init__.py
type nul > src\training\__init__.py
type nul > src\inference\__init__.py
type nul > src\data\__init__.py
type nul > src\monitoring\__init__.py
type nul > tests\__init__.py
type nul > tests\unit\__init__.py
type nul > tests\integration\__init__.py

echo Structure created successfully!
pause