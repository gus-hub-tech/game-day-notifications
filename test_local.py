#!/usr/bin/env python3
"""
Local test script for NBA Game Day Notifications Lambda function.
Run this script to test the function locally before deploying to AWS Lambda.
"""

import os
from dotenv import load_dotenv
from src.gd_notifications import lambda_handler

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Check if required environment variables are set
    required_vars = ['NBA_API_KEY', 'SNS_TOPIC_ARN']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Error: Missing environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file and ensure all variables are set.")
        return
    
    print("Starting local test of NBA Game Day Notifications...")
    print(f"NBA API Key: {'*' * 20}{os.getenv('NBA_API_KEY')[-4:]}")
    print(f"SNS Topic ARN: {os.getenv('SNS_TOPIC_ARN')}")
    print("-" * 50)
    
    # Mock Lambda event and context (empty for this function)
    event = {}
    context = {}
    
    try:
        # Run the Lambda function
        result = lambda_handler(event, context)
        print("-" * 50)
        print("Function execution completed!")
        print(f"Result: {result}")
        
    except Exception as e:
        print(f"Error during execution: {e}")
        print("Check your AWS credentials and environment variables.")

if __name__ == "__main__":
    main()