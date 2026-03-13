import os
import sys

# load env
from dotenv import load_dotenv
load_dotenv()


class KeyValueStore:
    def __init__(self, file_path):
        self.file_path = file_path
        self.index = []  
        self.load()

    
    # write command to in file
    def append(self, key, value):
        with open(self.file_path, "a") as f:
            f.write(f"SET {key} {value}\n")
            f.flush()
            os.fsync(f.fileno())

    # storre key value pair in memory and write to file
    def set(self, key, value):
        self.append(key, value)

       
        for i in range(len(self.index)):
            if self.index[i][0] == key:
                self.index[i] = (key, value)
                return

       
        self.index.append((key, value))

    # retrieve value based on key
    
    def get(self, key):
        for k, v in reversed(self.index):
            if k == key:
                return v
        return None
    
    # load database (persistance after restarting)

    
    def load(self):
        if not os.path.exists(self.file_path):
            return

        with open(self.file_path, "r") as f:
            for line in f:
                parts = line.strip().split(" ", 2)

                if len(parts) == 3 and parts[0] == "SET":
                    key = parts[1]
                    value = parts[2]

                    found = False
                    for i in range(len(self.index)):
                        if self.index[i][0] == key:
                            self.index[i] = (key, value)
                            found = True
                            break

                    if not found:
                        self.index.append((key, value))


def main():
   
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except AttributeError:
        pass

    store = KeyValueStore("data.db")

    for line in sys.stdin:
        command = line.strip().split(" ", 2)

        if not command:
            continue

        if command[0] == "SET" and len(command) == 3:
            store.set(command[1], command[2])

        elif command[0] == "GET" and len(command) == 2:
            value = store.get(command[1])
            if value is None:
                print("")
            else:
                print(value)

        elif command[0] == "EXIT":
            break


if __name__ == "__main__":
    main()
