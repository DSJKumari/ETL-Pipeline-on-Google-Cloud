import csv
import random
from faker import Faker
import string
from google.cloud import storage

# Initialize Faker
fake = Faker()

# Number of records to generate
num_records = 1000

# Define the character set for the password
password_characters = string.ascii_letters + string.digits + 'm'

# Specify the fields for the employee data
fields = ['Employee ID', 'First Name', 'Last Name', 'Email', 'Phone Number', 'Address', 'Job Title', 'Department', 'Hire Date', 'Salary', 'Password']

# Function to generate a single employee record
def generate_employee_data():
    return {
        'Employee ID': fake.unique.random_int(min=1000, max=9999),
        'First Name': fake.first_name(),
        'Last Name': fake.last_name(),
        'Email': fake.email(),
        'Phone Number': fake.phone_number(),
        'Address': fake.city(),
        'Job Title': fake.random_element(elements=('Software Engineer', 'Data Scientist', 'Marketing Manager', 'Financial Analyst', 'Graphic Designer', 'Product Manager', 'UX Designer', 'Sales Representative', 'Project Coordinator', 'IT Specialist')),
        'Department': fake.random_element(elements=('Sales', 'Marketing', 'HR', 'Engineering', 'Finance', 'IT')),
        'Hire Date': fake.date_this_decade().strftime('%Y-%m-%d'),
        'Salary': fake.random_int(min=40000, max=120000),
        "Password": ''.join(random.choice(password_characters) for _ in range(8))
    }

# Generate the initial employee data
employee_data = [generate_employee_data() for _ in range(num_records)]

csv_filename = 'employee_data.csv'
# Write the data to a CSV file
with open(csv_filename, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    writer.writerows(employee_data)

print(f"Generated {num_records} dummy employee records, saved to 'employee_data.csv'")

# Upload the CSV file to Google Cloud Storage
def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name} in bucket {bucket_name}.")

# Define your GCS bucket name and the destination blob name
bucket_name = 'emp_dat'
destination_blob_name = 'employee_data.csv'

# Call the upload function
upload_to_gcs(bucket_name, csv_filename, destination_blob_name)