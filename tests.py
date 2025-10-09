from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file

# dir content test
"""
a = get_files_info("calculator", ".")
b = get_files_info("calculator", "pkg")
c = get_files_info("calculator", "/bin")
d = get_files_info("calculator", "../")
print(a)
print(b)
print(c)
print(d)
"""


# file content test
# print(get_file_content("calculator", "lorem.txt"))

"""
a = get_file_content("calculator", "main.py"),
b = get_file_content("calculator", "pkg/calculator.py"),
c = get_file_content("calculator", "/bin/cat"),  # (this should return an error string)
d = get_file_content("calculator", "pkg/does_not_exist.py") # (this should return an error string)
"""


# Test to write to file
a = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
b = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
c = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")


print(a)
print(b)
print(c)
#  print(d)
