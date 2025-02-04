import json
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from requests.auth import HTTPBasicAuth
import urllib3
from datetime import datetime

# Suppress InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration (Update with your details)
url_issues = 'https://sonar.10pearls.com/api/issues/search'
url_projects = 'https://sonar.10pearls.com/api/projects/search?qualifier=TRK?ps=500&p='  # Base URL for projects API
sonar_url = 'https://sonar.10pearls.com/api/measures/component'
myToken = ''  # SonarQube token for authentication
output_file = 'sonarqube_issues_summary.pdf'  # Path for the PDF output
email_sender = 'muhammedhm2002@gmail.com'
email_recipient = 'hasan.misba@10pearls.com'
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'muhammedhm2002@gmail.com'
smtp_password = ''  # Use an app-specific password if needed


# Fetch project details (with pagination for large datasets)
def get_projects():
    projects = []
    page = 1
    while True:
        try:
            response = requests.get(f'{url_projects}{page}', auth=(myToken, ''))
            response.raise_for_status()
            data = response.json()
            project_list = data.get('components', [])
            
            if not project_list:
                break  # No more projects, stop pagination
            
            projects.extend([{'name': project['name'], 'key': project['key']} for project in project_list])
            page += 1
        except requests.exceptions.RequestException as e:
            print(f"Error fetching projects: {e}")
            break
    return projects

# Fetch issue counts for each project with the latest creationDate only
def get_issue_counts(project_key):
    try:
        issues = []
        page = 1
        page_size = 100  # The max page size that SonarQube allows

        while True:
            # Prepare the request URL with pagination
            response = requests.get(f'{url_issues}?componentKeys={project_key}&severities=BLOCKER,CRITICAL&p={page}&ps={page_size}', 
                auth=(myToken, '')
            )
            response.raise_for_status()
            data = response.json()
            page_issues = data.get('issues', [])
            
            if not page_issues:  # If no issues are returned, stop pagination
                break

            issues.extend(page_issues)  # Add the current batch of issues to the list
            print(f"Fetched {len(page_issues)} issues from page {page}")

            # If fewer issues than requested (page_size), we've reached the last page
            if len(page_issues) < page_size:
                break

            page += 1  # Increment page number for the next request
            if page == 101:
                break
        print(f"Total issues fetched: {len(issues)}")

        # Initialize counts and date list

        counts = {'HIGH': 0}
        latest_creation_date = None
        latest_issues = []

        # Process all issues
        for issue in issues:
            # Extract issue creation date (if available) or fallback to N/A
            created_at = issue.get('creationDate', 'N/A')

            if created_at != 'N/A':
                # Use '%z' to handle the timezone offset (e.g., +0000, -0700)
                try:
                    issue_creation_datetime = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S%z')
                    if not latest_creation_date or issue_creation_datetime > latest_creation_date:
                        latest_creation_date = issue_creation_datetime
                        latest_issues = [issue]  # Start a new list for the latest issues
                    elif issue_creation_datetime == latest_creation_date:
                        latest_issues.append(issue)
                except ValueError as ve:
                    print(f"Error parsing date for issue: {created_at}. Error: {ve}")

        # Count severities for the issues
        for issue in issues:
            severity = issue.get('severity', 'UNKNOWN').upper()
            if severity in ['BLOCKER', 'CRITICAL']:
                counts['HIGH'] += 1
        return counts, latest_creation_date

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None, None





def get_metrics(project_key):
    try:
        # Fetch all issues for the project to determine the latest creation date
        response = requests.get(f'{url_issues}?componentKeys={project_key}&severities=BLOCKER,CRITICAL,MAJOR,MINOR,INFO', auth=(myToken, ''))
        response.raise_for_status()
        data = response.json()
        issues = data.get('issues', [])

        latest_creation_date = None
        latest_issues = []

        # Determine the latest issues based on the creation date
        for issue in issues:
            created_at = issue.get('creationDate', 'N/A')
            if created_at != 'N/A':
                # Use '%z' to handle the timezone offset (e.g., +0000, -0700)
                try:
                    issue_creation_datetime = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S%z')
                    if not latest_creation_date or issue_creation_datetime > latest_creation_date:
                        latest_creation_date = issue_creation_datetime
                        latest_issues = [issue]  # Start a new list for the latest issues
                    elif issue_creation_datetime == latest_creation_date:
                        latest_issues.append(issue)
                except ValueError as ve:
                    print(f"Error parsing date for issue: {created_at}. Error: {ve}")

        # Fetch metrics for the project based on the latest issues
        if latest_issues:
            # Only fetch metrics if there are any latest issues
            params = {'component': project_key, 'metricKeys': 'ncloc'}  # ncloc = Lines of Code
            response = requests.get(sonar_url, auth=HTTPBasicAuth(username=myToken, password=""), params=params, verify=False, timeout=30)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            measures = data.get('component', {}).get('measures', [])

            # Extract the 'ncloc' value (lines of code) for the latest issues' project
            ncloc_value = next((measure['value'] for measure in measures if measure['metric'] == 'ncloc'), 'N/A')
            return ncloc_value

        return 'N/A'  # If no latest issues are found, return 'N/A'

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching metrics: {e}")
        return None




# Generate PDF report
def generate_pdf(projects, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    content = []

    # Title
    title = Paragraph("<b>SonarQube Project Issues Summary</b>", styles['Title'])
    content.append(title)
    content.append(Spacer(1, 12))

    # Custom style for issue details
    issue_style = ParagraphStyle(
        name='IssueDetails',
        parent=styles['BodyText'],
        textColor=colors.HexColor('#000000'),  # Black color
        fontSize=10,
        spaceAfter=10
    )
    i=0
    # Add project details
    for project in projects:
        project_name = project.get('name', 'Unknown Project')
        project_key = project.get('key', 'UnknownKey')
        counts,date = get_issue_counts(project_key)
        ncloc = get_metrics(project_key)
        if counts['HIGH'] == 10000:
            project_info = (
                f"<b>Project:</b> {project_name}<br/>"
                f"<b>High Severity Issues:</b> >10000 <br/>"
                f"<b>Lines of Code (ncloc):</b> {ncloc}<br/><br/>"
                f"<b>Date :</b> {date}<br/><br/>"
            )
            content.append(Paragraph(project_info, issue_style))
        else:
            project_info = (
                f"<b>Project:</b> {project_name}<br/>"
                f"<b>High Severity Issues:</b> {counts['HIGH']}<br/>"
                f"<b>Lines of Code (ncloc):</b> {ncloc}<br/><br/>"
                f"<b>Date :</b> {date}<br/><br/>"
            )
            content.append(Paragraph(project_info, issue_style))

    doc.build(content)

# Function to send the email with the PDF attachment
def send_email_with_attachment(subject, body, filename):
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_recipient
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    # Attach the PDF
    with open(filename, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={filename}')
        msg.attach(part)

    # Sending the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(email_sender, email_recipient, msg.as_string())

# Main function
def main():
    projects = get_projects()  # Fetch the projects
    if not projects:
        print("No projects found or there was an error fetching the projects.")
        return

    generate_pdf(projects, output_file)  # Generate the PDF report
    print(f"PDF report has been generated and saved as {output_file}")

    # Sending the email
    send_email_with_attachment(
        subject='SonarQube Project Issues Summary Report',
        body='Please find attached the summary report of issues for all SonarQube projects.',
        filename=output_file
    )
    print(f"Email sent successfully to {email_recipient}")

if __name__ == '__main__':
    main()
