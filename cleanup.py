#!/usr/bin/env python3
"""
Cleanup script to remove all AWS resources
"""

import boto3
import os
import sys
from dotenv import load_dotenv

load_dotenv()

class UmrahTripCleaner:
    def __init__(self):
        self.region = os.getenv('AWS_REGION', 'us-west-2')
        self.account_id = os.getenv('AWS_ACCOUNT_ID')
        self.project_name = 'umrah-trip-creator'
        
        self.cfn = boto3.client('cloudformation', region_name=self.region)
        self.s3 = boto3.client('s3', region_name=self.region)
        
        print("🗑️  Umrah Trip Creator Cleanup")
        print("="*60)
    
    def confirm_deletion(self):
        """Ask for confirmation"""
        print("\n⚠️  WARNING: This will delete ALL resources!")
        print("Resources to be deleted:")
        print("  - CloudFormation stack")
        print("  - S3 buckets and contents")
        print("  - DynamoDB tables and data")
        print("  - AgentCore agents")
        print("  - All configurations")
        
        response = input("\nType 'DELETE' to confirm: ")
        return response == 'DELETE'
    
    def empty_s3_bucket(self, bucket_name):
        """Empty S3 bucket before deletion"""
        try:
            print(f"  Emptying bucket: {bucket_name}")
            
            # List and delete all objects
            paginator = self.s3.get_paginator('list_objects_v2')
            for page in paginator.paginate(Bucket=bucket_name):
                if 'Contents' in page:
                    objects = [{'Key': obj['Key']} for obj in page['Contents']]
                    self.s3.delete_objects(
                        Bucket=bucket_name,
                        Delete={'Objects': objects}
                    )
            
            # Delete all versions
            paginator = self.s3.get_paginator('list_object_versions')
            for page in paginator.paginate(Bucket=bucket_name):
                if 'Versions' in page:
                    versions = [{'Key': v['Key'], 'VersionId': v['VersionId']} 
                               for v in page['Versions']]
                    self.s3.delete_objects(
                        Bucket=bucket_name,
                        Delete={'Objects': versions}
                    )
            
            print(f"  ✅ Bucket emptied: {bucket_name}")
            return True
            
        except Exception as e:
            print(f"  ❌ Failed to empty bucket: {e}")
            return False
    
    def delete_stack(self):
        """Delete CloudFormation stack"""
        stack_name = f"{self.project_name}-stack"
        
        try:
            print(f"\n🗑️  Deleting stack: {stack_name}")
            
            # Empty S3 buckets first
            bucket_name = f"{self.project_name}-documents-{self.account_id}"
            self.empty_s3_bucket(bucket_name)
            
            # Delete stack
            self.cfn.delete_stack(StackName=stack_name)
            
            print("⏳ Waiting for stack deletion (this may take 5-10 minutes)...")
            waiter = self.cfn.get_waiter('stack_delete_complete')
            waiter.wait(StackName=stack_name)
            
            print("✅ Stack deleted successfully")
            return True
            
        except Exception as e:
            print(f"❌ Stack deletion failed: {e}")
            return False
    
    def run(self):
        """Run cleanup"""
        if not self.confirm_deletion():
            print("\n❌ Cleanup cancelled")
            sys.exit(0)
        
        print("\n🗑️  Starting cleanup...")
        
        if self.delete_stack():
            print("\n✅ Cleanup complete!")
            print("All AWS resources have been removed.")
        else:
            print("\n⚠️  Cleanup completed with errors")
            print("Please check AWS Console for any remaining resources")

if __name__ == '__main__':
    cleaner = UmrahTripCleaner()
    cleaner.run()
