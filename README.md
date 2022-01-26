A script that

    1. downloads an xlsx file via SFTP (Secure File Transfer Protocol) from an origin remote server using Paramiko,
    2. modifies the contents with Pandas, and
    3. uploads 2 output csv files to a destination remote server.

In order to configure as an AWS Lambda function:

    1. Create an ".env" file in the root folder, fill it with the contents of ".sample.env", and enter the variables.
    2. Upload root folder to Lambda as the code source. Leave the handler configuration as is.
    3. Configure dependency layers for the required Python modules (listed in "requirements.txt").
    4. Configure an event source as a trigger (S3, API Gateway, EventBridge, etc.) that will run the function.

In order to run as a standalone script:

    1. Create an ".env" file in the root folder, fill it with the contents of ".sample.env", and enter the variables.
    2. Run "pip install -r requirements.txt" in your virtual python environment.
    3. Run "run.py".