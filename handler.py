import boto3
import face_recognition
import pickle
import os
from boto3.dynamodb.conditions import Key
import csv
INPUT_BUCKET_NAME = "cse546project3input"
OUTPUT_BUCKET_NAME = "cse546project3output"
session = boto3.Session()
s3 = session.client('s3')

# Function to read the 'encoding' file
def open_encoding(filename):
	file = open(filename, "rb")
	data = pickle.load(file)
	file.close()
	return data

# Function to process video and extract frames 
def process_video_object(file_name):
    s3.download_file(
    Bucket=INPUT_BUCKET_NAME, Key=file_name, Filename=f"/tmp/{file_name}")
    video_file_path =  f"/tmp/{file_name}"
    path = "/tmp/"
    os.system("ffmpeg -i " + str(video_file_path) + " -r 1 " + str(path) + "image-%3d.jpeg")

# Function to print temp folder contents
def print_temp_folder_contents():
    temp_folder_path = '/tmp'
    contents = os.listdir(temp_folder_path)
    print(f"Contents of {temp_folder_path}:")
    for item in contents:
        print(item)

# Function to process image using face recognition lib and get face data
def process_image():
    contents = os.listdir('/tmp')
    encoding_data = open_encoding("/home/app/encoding")
    names = encoding_data['name']
    encoding = encoding_data['encoding']
    resultant_names = []
    
    for item in contents:
        if item.startswith("image"):
            image = face_recognition.load_image_file(f"/tmp/{item}")
            new_encoding = face_recognition.face_encodings(image)[0]
            results = face_recognition.compare_faces(encoding, new_encoding)
            for i in range(len(results)):
                 if results[i]:
                      resultant_names.append(names[i])
    
    return resultant_names

# Function to search student name in dynamodb and get info
def get_data_from_dynamodb(names):
	dynamodb = session.resource('dynamodb')
	student_data = dynamodb.Table("student")
	response = student_data.get_item(Key={"name":names[0]})
	return response['Item']

# Function to create CSV of student info and put in output S3 bucket
def store_into_s3(file_name, content):
	file_name= file_name.replace(".mp4",".csv")
	with open(f'/tmp/{file_name}', 'w',  encoding='UTF8') as file:
		csv.writer(file).writerow([content['name'], content["major"], content["year"]])
    
	s3.upload_file(f'/tmp/{file_name}', OUTPUT_BUCKET_NAME, file_name)

      
# Handler Function 
def face_recognition_handler(event, context):	
    print(event)

    record = event.get("Records")[0]["s3"]
    # Check if event has video object name
    if record.get("bucket") is None or record.get("bucket").get("name") != INPUT_BUCKET_NAME:
        print("Failed")
        return
    file_name = record['object']['key']
        
    # testing and debugging
    # print_temp_folder_contents()

    # Process Video and store frames in /tmp/ folder
    process_video_object(file_name)

    # Process the Image, recognize the face and get the name of the student 
    result = process_image()

    # Retrive the student's details from dynamoDB
    response = get_data_from_dynamodb(result)

    # Store response to output S3 bucket
    store_into_s3(file_name, response)