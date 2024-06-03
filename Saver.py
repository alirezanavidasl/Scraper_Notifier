import csv

class Saver:
    def __init__(self,hashlist_file_name) -> None:
        self.hashlist_file_path = f'result/hashlist_{hashlist_file_name}.csv'
# TODO: save in db
        try:
            with open(self.hashlist_file_path, "x", newline='') as csvfile:  
                csv.writer(csvfile)
        except FileExistsError:
                pass
        except Exception as e:
            print(f"An error occurred: {e}")


    def hash_exists(self, hash_value):
        with open(self.hashlist_file_path, 'r') as file:
            reader = csv.reader(file)
            hashes = [row[0] for row in reader]
        return hash_value in hashes

    def append_hash(self, hash_value):
        with open(self.hashlist_file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([hash_value])