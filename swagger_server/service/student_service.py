import os
from pymongo import MongoClient

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["students_db"]
student_collection = db["students"]


def add(student=None):
    existing = student_collection.find_one({
        "first_name": student.first_name,
        "last_name": student.last_name
    })
    if existing:
        return 'already exists', 409

    student_dict = student.to_dict()
    result = student_collection.insert_one(student_dict)
    student_id = str(result.inserted_id)
    student.student_id = student_id
    return student.student_id


def get_by_id(student_id=None, subject=None):
    from bson import ObjectId
    try:
        student = student_collection.find_one({"_id": ObjectId(student_id)})
    except Exception:
        return 'invalid id', 400
    if not student:
        return 'not found', 404
    student['student_id'] = str(student['_id'])
    del student['_id']
    print(student)
    return student


def delete(student_id=None):
    from bson import ObjectId
    try:
        student = student_collection.find_one({"_id": ObjectId(student_id)})
    except Exception:
        return 'invalid id', 400
    if not student:
        return 'not found', 404
    student_collection.delete_one({"_id": ObjectId(student_id)})
    return student_id