# NBA Game Day Notifications / Sports Alerts System

## **Project Overview**

NBA Game Day Notifications is a fully serverless cloud-native alert system that delivers real-time NBA game scores and updates to subscribers via SMS and email. The system automatically fetches live game data from the SportsData.io API and distributes formatted notifications using AWS managed services.

The system demonstrates modern serverless patterns with automated scheduling, external API integration, and multi-channel notification delivery, making it cost-effective and maintenance-free for sports fans wanting real-time NBA updates


---

## **Features**
- Fetches live NBA game scores using an external API.
- Sends formatted score updates to subscribers via SMS/Email using Amazon SNS.
- Scheduled automation for regular updates using Amazon EventBridge.
- Designed with security in mind, following the principle of least privilege for IAM roles.

## **Prerequisites**
- Free account with subscription and API Key at [sportsdata.io](https://sportsdata.io/)
- Personal AWS account with basic understanding of AWS and Python

---

## **Technical Architecture**
![nba_API](https://github.com/user-attachments/assets/5e19635e-0685-4c07-9601-330f7d1231f9)

---


## **Technologies**
- **Cloud Provider**: AWS
- **Core Services**: SNS, Lambda, EventBridge
- **External API**: NBA Game API (SportsData.io)
- **Programming Language**: Python 3.x
- **IAM Security**:
  - Least privilege policies for Lambda, SNS, and EventBridge.

---

## **Project Structure**
```bash
game-day-notifications/
├── src/
│   └── gd_notifications.py          # Main Lambda function code
├── policies/
│   └── gd_sns_policy.json           # SNS publishing permissions
├── .env                             # Environment variables (not committed)
├── requirements.txt                 # Python dependencies for local development
├── test_local.py                    # Local testing script
├── .gitignore
└── README.md                        # Project documentation
```

## **Setup Instructions**

### **Clone the Repository**
```bash
git clone https://github.com/gus-hub-tech/game-day-notifications.git
cd game-day-notifications
```

### **Configure Environment Variables**
1. Copy the `.env` file and update with your actual values:
   - `NBA_API_KEY`: Your SportsData.io API key
   - `SNS_TOPIC_ARN`: Your AWS SNS topic ARN
   - `AWS_DEFAULT_REGION`: Your AWS region
2. The `.env` file is for reference only and not committed to version control for security.

### **Set Up Local Development Environment (Optional)**

**Why Use a Virtual Environment:**
- **Isolates dependencies** - Prevents conflicts with other Python projects
- **Clean environment** - Only installs required packages
- **Reproducible setup** - Ensures consistent dependency versions
- **Safe testing** - Won't affect your system Python installation

**Understanding Dependencies:**
- **boto3** - AWS SDK for Python (required for SNS operations)
- **python-dotenv** - Loads environment variables from .env file
- **Note:** boto3 is pre-installed in AWS Lambda but needed for local testing

**Create and Activate Virtual Environment:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac/WSL
# or
venv\Scripts\activate     # Windows

# Install dependencies from requirements.txt
pip install -r requirements.txt

# When done, deactivate
deactivate
```

**What's in requirements.txt:**
```txt
# AWS SDK for Python - required for SNS client
boto3>=1.26.0

# Python-dotenv for loading .env file in local development
python-dotenv>=1.0.0
```

### **Create an SNS Topic**
1. Open the AWS Management Console.
2. Navigate to the SNS service.
3. Click Create Topic and select Standard as the topic type.
4. Name the topic (e.g., gd_topic) and note the ARN.
5. Click Create Topic.

### **Add Subscriptions to the SNS Topic**
1. After creating the topic, click on the topic name from the list.
2. Navigate to the Subscriptions tab and click Create subscription.
3. Select a Protocol:
- For Email:
  - Choose Email.
  - Enter a valid email address.
- For SMS (phone number):
  - Choose SMS.
  - Enter a valid phone number in international format (e.g., +1234567890).

4. Click Create Subscription.
5. If you added an Email subscription:
- Check the inbox of the provided email address.
- Confirm the subscription by clicking the confirmation link in the email.
6. For SMS, the subscription will be immediately active after creation.

### **Create the SNS Publish Policy**
1. Open the IAM service in the AWS Management Console.
2. Navigate to Policies → Create Policy.
3. Click JSON and paste the JSON policy from `policies/gd_sns_policy.json` file
4. Replace REGION and ACCOUNT_ID with your AWS region and account ID.
5. Click Next: Tags (you can skip adding tags).
6. Click Next: Review.
7. Enter a name for the policy (e.g., gd_sns_policy).
8. Review and click Create Policy.

### **Create an IAM Role for Lambda**
1. Open the IAM service in the AWS Management Console.
2. Click Roles → Create Role.
3. Select AWS Service and choose Lambda.
4. Attach the following policies:
   - SNS Publish Policy (gd_sns_policy) (created in the previous step)
   - AWSLambdaBasicExecutionRole (AWS managed policy for CloudWatch Logs)
5. Click Next: Tags (you can skip adding tags).
6. Click Next: Review.
7. Enter a name for the role (e.g., gd_role).
8. Review and click Create Role.
9. Copy and save the ARN of the role for use in the Lambda function.

### **Deploy the Lambda Function**
1. Open the AWS Management Console and navigate to the Lambda service.
2. Click Create Function.
3. Select Author from Scratch.
4. Enter a function name (e.g., gd_notifications).
5. Choose Python 3.x as the runtime.
6. Assign the IAM role created earlier (gd_role) to the function.
7. Under the Function Code section:
   - Copy the content of the `src/gd_notifications.py` file from the repository
   - Paste it into the inline code editor
8. Under the Environment Variables section, add the following:
   - `NBA_API_KEY`: your NBA API key from sportsdata.io
   - `SNS_TOPIC_ARN`: the ARN of the SNS topic created earlier
9. Click Create Function.


### **Set Up Automation with EventBridge**
1. Navigate to the EventBridge service in the AWS Management Console.
2. Go to Rules → Create Rule.
3. Select Event Source: Schedule.
4. Set the cron schedule for when you want updates (e.g., `rate(1 hour)` for hourly updates).
5. Under Targets, select the Lambda function (gd_notifications).
6. Create an IAM role for EventBridge to invoke Lambda (or use an existing one).
7. Save the rule.


### **Test the System**
1. Open the Lambda function in the AWS Management Console.
2. Create a test event to simulate execution.
3. Run the function and check CloudWatch Logs for errors.
4. Verify that SMS/Email notifications are sent to the subscribed users.
5. Check the function output for successful API calls and SNS publishing.

### **Local Testing (Optional)**

**Test the Lambda function locally before deploying:**

1. **Set up AWS credentials** (required for SNS access):
```bash
# Option 1: AWS CLI (recommended)
aws configure

# Option 2: Environment variables
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
```

2. **Run the local test script**:
```bash
# Activate virtual environment
source venv/bin/activate

# Run local test
python test_local.py
```

**What the local test does:**
- Loads environment variables from `.env` file
- Validates required configuration
- Executes the Lambda function locally
- **Sends real notifications** to your SNS topic subscribers
- Displays execution results and any errors

**Note:** Local testing will send actual emails/SMS to your subscribers, just like the deployed Lambda function.

### **Troubleshooting**

**Common Reasons You Might Not Be Getting Notifications:**

1. **No Games Today** - NBA season runs October-June, no games during off-season
2. **EventBridge Not Triggered** - Check if your scheduled rule has actually fired
3. **Email Subscription Not Confirmed** - Must click confirmation link in initial SNS email
4. **Lambda Errors** - Check CloudWatch Logs for API or permission issues
5. **Wrong Environment Variables** - Verify `NBA_API_KEY` and `SNS_TOPIC_ARN` are correct in Lambda
6. **API Key Issues** - Ensure your SportsData.io API key is valid and not expired
7. **SNS Topic Permissions** - Verify Lambda has permission to publish to your SNS topic
8. **boto3 Module Not Found** - For local testing, install dependencies with `pip install -r requirements.txt`

**Quick Troubleshooting Steps:**

1. **Manual Test** - Run the Lambda function manually with a test event to bypass EventBridge
2. **Check CloudWatch Logs** - Look for errors, API responses, or successful SNS publishing
3. **Verify SNS Subscription** - Ensure email subscription shows "Confirmed" status in SNS console
4. **Check NBA Schedule** - Verify there are actually games scheduled for today
5. **Test SNS Directly** - Send a test message from SNS console to confirm email delivery works
6. **Run Local Test** - Use `python test_local.py` to test the function locally with your actual AWS resources


### **What We Learned**
1. Designing a notification system with AWS SNS and Lambda.
2. Securing AWS services with least privilege IAM policies.
3. Automating workflows using EventBridge.
4. Integrating external APIs into cloud-based workflows.

### **Demo Images**

<img width="1317" height="268" alt="sns-topic" src="https://github.com/user-attachments/assets/1ee3be16-4ebb-4207-8ddf-5964a1a978ee" />
<img width="1303" height="397" alt="sub" src="https://github.com/user-attachments/assets/1924179b-c4c1-4d3d-9e86-5b631e041a0e" />
<img width="1308" height="257" alt="sns-policy" src="https://github.com/user-attachments/assets/03bf1f4c-99a7-4d6e-83ad-ee487238ae39" />
<img width="1302" height="285" alt="gd-lambda-role" src="https://github.com/user-attachments/assets/45c92854-6ae7-4ba4-910c-f4e0fe797fa6" />
<img width="1297" height="471" alt="function" src="https://github.com/user-attachments/assets/7fdc5795-80b3-443e-8d42-d099cd3b84c5" />
<img width="1317" height="382" alt="event-bridge" src="https://github.com/user-attachments/assets/9b998741-d378-4e02-ac85-80e856b7205a" />
<img width="1163" height="167" alt="venv-local" src="https://github.com/user-attachments/assets/3e4e1a0e-311d-440e-b37d-485d42366347" />
<img width="1132" height="232" alt="published" src="https://github.com/user-attachments/assets/8f06402b-9ada-4ae1-8044-a5e58d8ff603" />
<img width="1848" height="849" alt="email" src="https://github.com/user-attachments/assets/b5fe1db0-4356-42b9-889c-f8b90528564b" />






### **Future Enhancements**
1. Add NFL score alerts for extended functionality.
2. Store user preferences (teams, game types) in DynamoDB for personalized alerts.
3. Implement a web UI for subscription management.
4. Refactor Lambda function to use `NBA_API_BASE_URL` environment variable for improved configurability and easier API endpoint management.
