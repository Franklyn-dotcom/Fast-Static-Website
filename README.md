# Fast Static Website Deployment Using Pulumi And AWS
This project shows how to deploy a static website using Pulumi and AWS services. It uses Pulumi's AWS SDK with Python to automate the provisioning of AWS cloud resources and hosting a globally distributed static website.

## Features
- Automates AWS cloud resources using Pulumi's AWS SDK with Python.
- Creates an S3 bucket for static website hosting and syncs the local `www` folder (containing `index.html` and `error.html`) to the bucket.
- Configures the S3 bucket for static website hosting with support for an index document (`index.html`) and an error document (`error.html`).
- Creates an AWS Cloudfront to serve as a Content Delivery Network(CDN) for global distribution, caching, and HTTPS support.

## Prerequisites
Before you begin, ensure you have:
- AWS Account
- IAM User Account for access keys and secret keys
- Pulumi Account and Pulumi CLI installed
- Python3.6 or higher
- Basic understanding of python

## How To Run The Project
### 1. Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/Franklyn-dotcom/Fast-Static-Website.git

cd Fast-Static-Website
``` 

### 2. Configure AWS Credential in the CLI:
After installing the AWS CLI, You need to configure your AWS CLI to enable you to connect and access your account. Run the following command to configure your AWS CLI:

```bash
aws configure
```
Enter the following details:
```
AWS_ACCESS_KEY_ID=<your_aws_access_key> # From IAM user security credentials

AWS_SECRET_ACCESS_KEY=<your_aws_secret_access_key> # From IAM user security credentials

DEFAULT_REGION=<aws_region>
```

### 3. Create a virtual environment:
After configuring your AWS CLI, you need to create a virtual environment for Python to enable us to isolate all the packages we’ll use in this project in a separate Python environment.

Run the following command to create a virtual environment:
```bash
python -m venv <name-of-your-virtual-env-folder>

```

After creating your virtual environment, you need to activate your virtual environment before installing or using any packages in your virtual environment.

To activate the virtual environment on Windows(Powershell), run the following command:

```bash
.\venv\Script\Activate.ps1
```

On macOS/Linux:
```bash
source venv/bin/activate
```

### 4. Install Dependencies:
After activating the virtual environment, run the following command to install the packages or library using the requirements.txt file. This file contains a list of tools (also called libraries or packages) you need for this project.

```bash
pip install -r requirements.txt
```


### 5. Configure Pulumi in the CLI:
After installing the Pulumi CLI, You need to configure your Pulumi CLI to enable you to connect and access your account. Run the following command to configure your Pulumi CLI:

```bash
pulumi login
```

You will prompt to either enter your personal access token or hit `<ENTER>` to log in using your browser

![pulumi-login](/Images/step-5.png)

You should see the following output when you have successfully logged in:

![pulumi-login](/Images/step-6.png)


### 6. Initializing a new Pulumi Stack:
Initializing a new stack allows you to manage your environment and deploy the same infrastructure. Run the following command to initialize a new stack:

```bash
pulumi stack init < your-stack-name > # Replace < your-stack-name > with your stack name such as dev or staging or prod. 
```

This command creates a new stack configurations in your project directory.

### 7. Setting Pulumi Configuration:
After initializing your stack, you will need to set your aws region and the path that holds the content of the website. Run the following command to set your configurations:

```bash
pulumi config set aws:region <your-region>
pulumi config set path ./www
```

### 8. Automating the resources:
Run the following command to automates the resources:

```bash
pulumi up
```
![pulumi-up](/Images/step-12.png)

After running the script, you should see the following output:
![success-1](/Images/step-16.png)
![success-2](/Images/step-18-success.png)

**AWS S3 And CloudFront Output**
![success-3](/Images/step-20.png)
![success-4](/Images/step-20.1.png)
![success-5](/Images/step-20.2.png)
![success-6](/Images/step-20.3.png)
![success-7](/Images/step-20.4.png)

**Website Preview**
![success-8](/Images/step-19-page.png)

### 9. Accessing the website:
- After the deployment process is complete, Pulumi will output the CloudFront URL in the terminal. 
- You can access the website using the CloudFront URL in the brower
- Check out my deployed version using this URL: [https://dxxqzfayx1t0f.cloudfront.net](https://dxxqzfayx1t0f.cloudfront.net)

## Resources:
- [Pulumi AWS Documentation](https://www.pulumi.com/docs/iac/get-started/aws/)

- [Hosting a static website using Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html)

- [AWS CloudFront Documentation](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html)
