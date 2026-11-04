\# DevOps Lab Mid Assignment

\## Automated CI Pipeline with Pytest and Local Test Report Delivery



\*\*Course:\*\* DevOps for Cloud Computing (CSC418)  

\*\*University:\*\* COMSATS University Islamabad – Attock Campus  

\*\*Repository:\*\* \[Maybeayan07/DevOps-Lab-Mid](https://github.com/Maybeayan07/DevOps-Lab-Mid)



\---



\## 1. Project Overview



This project implements a Flask-based Assignment Submission Portal with an automated Continuous Integration (CI) pipeline using GitHub Actions.



The application allows students to submit assignment details, validates the required information, and displays valid submissions.



The CI pipeline automatically executes three test cases whenever code is pushed to the `main` branch. Test results are converted into a JSON report and automatically delivered to a local HTTP receiver running on the developer's computer.



\## 2. Features



\- Assignment submission form.

\- Student name, registration number, assignment title, and submission URL fields.

\- Required-field validation.

\- HTTP/HTTPS URL validation.

\- Display of successfully submitted assignments.

\- Automated testing with Pytest.

\- GitHub Actions CI workflow.

\- Self-hosted GitHub Actions runner on Windows.

\- Automatic test report delivery to a local Flask receiver.

\- JSON test report containing repository, branch, commit SHA, pipeline run ID, timestamp, test results, and overall status.

\- Both successful and failed test reports are delivered automatically.



\## 3. Technologies Used



\- Python 3.13

\- Flask

\- Pytest

\- Git and GitHub

\- GitHub Actions

\- Self-hosted Windows Runner

\- JSON

\- PowerShell



\## 4. Project Structure



```text

DevOps-Lab-Mid/

│

├── app.py

├── report\_receiver.py

├── run\_tests.py

├── requirements.txt

├── README.md

├── .gitignore

│

├── templates/

│   └── index.html

│

├── tests/

│   └── test\_app.py

│

└── .github/

&#x20;   └── workflows/

&#x20;       └── ci.yml

```



\## 5. Installation and Setup



\### Step 1: Clone the Repository



```bash

git clone https://github.com/Maybeayan07/DevOps-Lab-Mid.git

cd DevOps-Lab-Mid

```



\### Step 2: Create a Virtual Environment



```powershell

python -m venv venv

```



Activate it:



```powershell

.\\venv\\Scripts\\Activate.ps1

```



\### Step 3: Install Dependencies



```bash

pip install -r requirements.txt

```



\## 6. Run the Application



Start the Flask application:



```bash

python app.py

```



Open the following URL in your browser:



```text

http://127.0.0.1:5000

```



\## 7. Run Automated Tests



Execute the test suite:



```bash

python -m pytest tests/ -v

```



\### Test Cases



1\. \*\*Valid Submission:\*\* Verifies that a valid assignment submission is accepted and displayed.

2\. \*\*Missing Registration Number:\*\* Verifies that submissions with a missing registration number are rejected.

3\. \*\*Invalid Submission URL:\*\* Verifies that an invalid URL is rejected and not saved.



\## 8. Automated CI Pipeline



The GitHub Actions workflow is located at:



```text

.github/workflows/ci.yml

```



The pipeline is triggered automatically on every push to the `main` branch. It can also be started manually using `workflow\_dispatch`.



Pipeline execution steps:



1\. Checkout the repository.

2\. Set up Python 3.13.

3\. Create a CI virtual environment.

4\. Install project dependencies.

5\. Execute automated tests.

6\. Generate test results.

7\. Send the JSON report to the local report receiver.



The workflow uses a self-hosted Windows runner so that the CI job can communicate with the local report receiver.



\## 9. Local Test Report Receiver



Start the local report receiver in a separate PowerShell terminal:



```powershell

python report\_receiver.py

```



The receiver runs at:



```text

http://127.0.0.1:5001

```



Health check endpoint:



```text

http://127.0.0.1:5001/health

```



The report endpoint accepts POST requests at:



```text

http://127.0.0.1:5001/report

```



The receiver automatically saves incoming reports to:



```text

test-report.json

```



The generated report is excluded from Git using `.gitignore`.



\## 10. Automatic Test Report Contents



Each report contains:



\- Repository name

\- Branch name

\- Commit SHA

\- GitHub Actions run ID

\- Timestamp

\- Individual test names

\- Test results

\- Failure messages

\- Total tests

\- Passed tests

\- Failed tests

\- Skipped tests

\- Overall pipeline status



Example report summary:



```json

{

&#x20; "total": 3,

&#x20; "passed": 3,

&#x20; "failed": 0,

&#x20; "skipped": 0,

&#x20; "status": "passed"

}

```



Failed test runs are also reported before the test runner exits with a failure status.



\## 11. Self-Hosted Runner Setup



A Windows self-hosted runner is configured through:



\*\*GitHub Repository → Settings → Actions → Runners\*\*



The runner must remain online while GitHub Actions jobs are executing.



The local report receiver must also remain running so that the pipeline can deliver its report.



\## 12. CI Demonstration and Results



The pipeline was tested through three stages:



\### Stage 1: Successful Execution



All three automated test cases passed, and the JSON report was successfully delivered to the local receiver.



\### Stage 2: Intentional Failure



A temporary URL-validation defect was introduced in the application. The CI pipeline detected the defect:



\- Total tests: 3

\- Passed: 2

\- Failed: 1

\- Overall status: Failed



The failing test report was automatically delivered and saved locally.



\### Stage 3: Bug Fix and Successful Execution



The URL-validation condition was corrected and pushed to GitHub.



The final CI execution confirmed:



\- Total tests: 3

\- Passed: 3

\- Failed: 0

\- Overall status: Passed



The updated successful JSON report was automatically saved on the local computer.



\## 13. Running the Complete System



Keep these three processes available:



\*\*Terminal 1 – Local Report Receiver\*\*



```powershell

python report\_receiver.py

```



\*\*Terminal 2 – Self-Hosted GitHub Runner\*\*



```powershell

cd C:\\actions-runner

.\\run.cmd

```



\*\*Terminal 3 – Project Commands\*\*



Use this terminal to run tests, modify application code, commit changes, and push updates:



```powershell

git add .

git commit -m "Update application"

git push origin main

```



\---



\## 14. Repository



GitHub: https://github.com/Maybeayan07/DevOps-Lab-Mid





