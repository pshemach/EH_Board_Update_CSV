import os


# Function to remove brackets from the prediction output
def remove_brackets(value):
    if isinstance(value, list):
        return (
            ", ".join(f"{item[0]} {item[1]:.2f}" for item in value) if value else "none"
        )
    return value


# Function to make a directory
def make_dir(path):
    os.makedirs(path, exist_ok=True)
