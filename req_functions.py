from google.cloud import storage
import os

def create_bucket(bucket_name, storage_class,location):
    client = storage.Client()
    
    bucket = client.bucket(bucket_name)
    bucket.storage_class = storage_class

    bucket = client.create_bucket(bucket,location)

    return f'Bucket {bucket.name} successfully created'

def create_folder(bucket_name,folder_name):
    client = storage.Client()

    bucket = client.bucket(bucket_name)

    blob = bucket.blob(folder_name+"/")

    blob.upload_from_string("")

def upload_file(bucket_name,source_file_name,destination_file_name):
    client = storage.Client()

    bucket = client.bucket(bucket_name)

    blob = bucket.blob(destination_file_name)
    blob.upload_from_filename(source_file_name)

    return True

def list_files(bucket_name):
    client = storage.Client()

    file_list = client.list_blobs(bucket_name)
    file_list = [file.name for file in file_list]

    return file_list

def donwload_file(bucket_name,file_name,destination_file_name):
    client = storage.Client()

    bucket = client.bucket(bucket_name)

    blob = bucket.blob(file_name)
    blob.download_to_filename(destination_file_name)

    return True

def download_folder(bucket_name, folder_name, destination_folder):


    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    # List the objects in the folder.
    blobs = bucket.list_blobs(prefix=folder_name + '/')

    # Download each object to the destination folder, preserving the directory structure.
    for blob in blobs:
        destination_file_name = blob.name
        if blob.name.endswith('/'):
        # Create the destination directory if it does not exist.
            if not os.path.exists(destination_file_name):
                os.makedirs(destination_file_name)
                os.makedirs('input_files/shipped_loose/')
        else:
            # Download the object to the destination file.
            blob.download_to_filename(destination_file_name)