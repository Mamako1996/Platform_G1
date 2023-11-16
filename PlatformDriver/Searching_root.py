import os


def get_root_address():
    current_dir_path = os.path.dirname(os.path.abspath(__file__))
    current_dir_path = os.path.dirname(current_dir_path)
    current_dir_path = os.path.dirname(current_dir_path)
    return current_dir_path


class Searching_root:
    def __init__(self):
        self.name = get_root_address()

    def print_root(self):
        return self.name


if __name__ == "__main__":
    print(Searching_root().print_root())
