class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    def __init__(self):
        print("Connecting to database...")

    def query(self, sql):
        print(f"Executing query: {sql}")


if __name__ == "__main__":
    db1 = Database()  # "Connecting to database..."
    db2 = Database()  # Не буде виведено "Connecting to database..." знову

    print(db1 is db2)  # True
