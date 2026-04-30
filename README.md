# InsiderOne QA Automation Framework

A production-ready test automation framework for the [InsiderOne](https://insiderone.com/) website, built with **Python**, **Selenium**, and **Pytest**.

## 🚀 Features

- **Page Object Model (POM)**: Modular and maintainable architecture.
- **Resilient Locators**: Multi-fallback strategy for dynamic web elements.
- **Robust BasePage**: Automatic cookie banner dismissal and optimized synchronization (explicit waits).
- **Comprehensive Reporting**: Self-contained HTML reports with embedded failure screenshots.
- **CI/CD Integrated**: 
  - **GitHub Actions**: Automated PR validation.
  - **Jenkins**: Pipeline support with artifact archiving and HTML publishing.
- **Headless Mode Support**: Optimized for execution in server environments.

## 🛠️ Tech Stack

- **Language**: Python 3.12+
- **Framework**: Pytest
- **Browser Automation**: Selenium WebDriver
- **Reporting**: pytest-html
- **Manager**: webdriver-manager

## 📂 Project Structure

```text
├── .github/workflows/   # GitHub Actions CI configurations
├── pages/               # Page Object classes
│   ├── base_page.py     # Universal setup & cookie dismissal
│   ├── home_page.py     # Homepage interactions
│   └── careers_page.py  # Advanced QA jobs filtering
├── tests/               # Test suites
│   └── test_qa_jobs.py  # E2E test scenarios
├── utils/               # Utilities
│   └── driver_factory.py # Robust browser initialization
├── reports/             # Test results (logs, screenshots, HTML)
├── Jenkinsfile          # Jenkins Pipeline configuration
├── pytest.ini           # Pytest settings
└── requirements.txt     # Python dependencies
```

## 🏁 Getting Started

### 1. Prerequisites
- Python installed on your system.
- Chrome browser installed.

### 2. Installation
Clone the repository and run the setup script (Windows):
```bash
# Clone the repository
git clone https://github.com/ebubekiryilmaz0/insider_project.git
cd insider_project

# Automatic setup (creates .venv and installs requirements)
./setup.bat
```

### 3. Running Tests (Terminal)
You can run tests using the provided `run_tests.py` CLI wrapper:

| Command | Description |
| :--- | :--- |
| `python run_tests.py` | Run all tests (Chrome, UI mode) |
| `python run_tests.py --headless` | Run in headless mode (no UI) |
| `python run_tests.py --browser firefox` | Run with Firefox |
| `python run_tests.py --smoke` | Run only smoke tests |
| `python run_tests.py --parallel` | Run tests in parallel (faster) |
| `python run_tests.py --help` | Show all available options |

#### Standard Pytest Commands:
Alternatively, you can use `pytest` directly:
```bash
# Basic run
pytest

# With specific browser and report
pytest --browser=firefox --html=reports/report.html
```

## 🏗️ CI/CD Integration

### GitHub Actions
The project includes a workflow that triggers on every PR and push to `main`. It also signals Jenkins upon successful merge to `main`.

### Jenkins
A `Jenkinsfile` is provided for professional pipeline management.
- Ensure the **HTML Publisher Plugin** is installed in Jenkins.
- Configure `JENKINS_URL`, `JENKINS_USER`, and `JENKINS_TOKEN` in GitHub Secrets for automatic triggers.

---
**Author**: ebubekiryilmaz0
