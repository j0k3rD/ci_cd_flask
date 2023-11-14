<h1 align="center"> CI/CD FLASKAPP </h1>

The application is a simple web application developed in Flask with a robust Continuous Integration and Continuous Deployment workflow managed by GitHub Actions. Hosted in Azure Cloud, the application displays a JSON 'Hello World!' message and has been configured for traces and logs using the OpenTelemetry library, making it easy to trace and troubleshoot in a production environment.

## Repository Structure

- **app.py:** The main file of the Flask application.
- **.github/workflows/BuildAndPushACR.yml:** GitHub Actions workflow configuration.
- **requirements.txt:** List of Python dependencies required to run the application.
- **deploy.sh:** Deployment script for Azure Cloud.

## Use and Deployment

1. **Repository Cloning:**
   ```bash
   git clone https://github.com/j0k3rD/ci_cd_flask.git
   cd ci_cd_flask
   ```

2. **Installation of Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Local Execution:**
   ```bash
   python app.py
   ```
   Access the application in your web browser: `http://localhost:5000`.

4. **CI/CD flow:**
   - GitHub Actions checks syntax and runs tests automatically on every commit to the main branch.
   - Automatic deployment to Azure Cloud after successful commit to master branch.

## About

Technologies and tools used in the development of this project:

<div align="center">

![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white) ![Azure](https://img.shields.io/badge/Azure-0089D6?style=for-the-badge&logo=microsoft-azure&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) ![OpenTelemetry](https://img.shields.io/badge/OpenTelemetry-4A154B?style=for-the-badge&logo=opentelemetry&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) ![Shell Script](https://img.shields.io/badge/Shell_Script-121011?style=for-the-badge&logo=gnu-bash&logoColor=white) ![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white) 

</div>
