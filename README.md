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
Clone the repository and install dependencies:
```bash
git clone https://github.com/ebubekiryilmaz0/insider_project.git
cd insider_project
pip install -r requirements.txt
```

### 3. Running Tests
Run all tests:
```bash
pytest
```

Run with HTML report:
```bash
pytest --html=reports/report.html --self-contained-html
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
