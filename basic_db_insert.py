# import random
# import string

# def generate_id() -> str:
#     return "".join(random.choices(string.ascii_uppercase + "".join([str(i) for i in range(10)]), k=12))

# for i in range(5):
#     print(generate_id())

from basic_database import select_user, insert_user

insert_user("Bob", "bob@example.com")
print(select_user("Bob"))
print(select_user("Noah"))