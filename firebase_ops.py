#import csv
import firebase_admin
from firebase_admin import credentials, firestore


def get_data_from_firebase():
    # Initialize Firebase app
    if not firebase_admin._apps:
        cred = credentials.Certificate("./creds/rfpdata2-firebase-adminsdk-u9for-9183c1949f.json")  # Replace with your service account key file
        firebase_admin.initialize_app(cred)

    # Path to the CSV file you want to write
    #csv_file_path = "./sample_data/rfpTest.csv"

    # Read CSV file and write to Firestore
    db = firestore.client()

    # Replace 'your-collection-name' with the actual name of your collection
    collection_name = "test"
    collection_ref = db.collection(collection_name)
    try:
        collection_ref.get()
    except firestore.NotFoundError:
        collection_ref.add()

    documents = collection_ref.stream()
    data_dict = {}

    for doc in documents:
        print(f'Document ID: {doc.id}')
        print(f'Document Data: {doc.to_dict()}')
        data_dict[doc.id] = doc.to_dict()

    return data_dict
    #print (len(data_dict), type(data_dict) )
    #print("Firebase Collections data read into local handle.")