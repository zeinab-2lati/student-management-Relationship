from schemas import StudentSchema

schema = StudentSchema()

data = {
    "first_name": "Zeinab",
    "last_name": "Dolati",
    "email": "zeinab@gmail.com",
    "age": 22
}

result = schema.load(data)

print(result)