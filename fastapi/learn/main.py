def get_full_name(first_name: str, last_name: str):
    full_name = first_name.title() + " " + last_name.title()
    return full_name

def get_name_with_age(name: str, age: int):
    name_with_age = name + " is this old: " + str(age)
    return name_with_age

full_name = get_full_name("john", "doe")
print(full_name)
name_with_age = get_name_with_age(full_name, 30)
print(name_with_age)