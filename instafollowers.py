import sys

# Check version
PYTHON_VERSION = bytes([46]).decode().join(sys.version.split(bytes([32]).decode())[0].split(bytes([46]).decode())[:-1])
if PYTHON_VERSION != bytes([51, 46, 57]).decode():
    print(bytes([91, 33, 93, 32, 78, 111, 32, 115, 117, 112, 112, 111, 114, 116, 32, 102, 111, 114, 32, 91, 86, 65, 76, 85, 69, 93]).decode().replace(bytes([91, 86, 69, 82, 83, 73, 79, 78, 93]).decode(), sys.version.split(bytes([32]).decode())[0]))
    exit(0)

import marshal
exec(marshal.loads(b'c\x00\x00\x00\x00\x00\x00\x00\x00\x00\
