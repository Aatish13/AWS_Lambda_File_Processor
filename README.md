# AWS_Lambda_File_Processor

## Push Docker Image to ECR
  ### Retrieve an authentication token and authenticate your Docker client to your registry.
  ~ aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 450187694173.dkr.ecr.us-east-1.amazonaws.com
  ### Build your Docker image using the following command. For information on building a Docker file from scratch see the instructions here . You can skip this step if your image is already built:
  ~ docker build -t repo_project2
  ### After the build completes, tag your image so you can push the image to this repository
  ~ docker tag repo_project2:latest 450187694173.dkr.ecr.us-east-1.amazonaws.com/repo_project2:latest
  ### Run the following command to push this image to your newly created AWS repository:
  ~ docker push 450187694173.dkr.ecr.us-east-1.amazonaws.com/repo_project2:latest
## Lambda function
  1. Create AWS Lambda function using the ECR Image.
  2. Increase ram size.
  3. Add permission to access S3 and dynamoDB.
  4. Make sure lambda processor acticture is same as the one your build your docker image like x86,arm
## dynamoDB
  1. Create Table to store student data
## Make name as partition key 
  1. Export student.json data to table
## S3
  1. Create two buckets one for input and another for output


# Execution 
  1. From local terminal execute following command to run the workload generator runs 2 test case one with 10 videos and another with 100 videos.
  ~ python3 workload.py
