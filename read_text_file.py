### Class to read data from a large text file in chunks

class ReadTextFile:
    number_of_chunks_to_read = None

    sentence_length = 300

    def __init__(self, file_name):
        self.file_name = file_name
        self.file_object = open(file_name, encoding = 'utf-8')

    def read_in_chunks(self, chunk_size=10000, number_of_chunks_to_read=None):
        k = 0
        """Lazy function (generator) to read a file piece by piece.
        Default chunk size: 1k."""
        while True: 
            k += 1
            data = self.file_object.read(chunk_size)
            if not data:
                break
            yield data
            if number_of_chunks_to_read is not None:
                if k > number_of_chunks_to_read:
                    break
