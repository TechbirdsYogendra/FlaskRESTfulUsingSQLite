users = [
    {
        "name": "Yogendra",
        "age": 29,
        "address": "D-71 Sector 52 Noida"
    },
    {
        "name": "Kavita",
        "age": 30,
        "address": "D-71 Sector 52 Noida"
    },
    {
        "name": "Yash",
        "age": 7,
        "address": "D-71 Sector 52 Noida"
    }
]

users_mapping = {user.get("name"): user for user in users}
print(users_mapping)