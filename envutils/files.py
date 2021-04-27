import hashlib


def compute_file_checksum(filename, alg="md5") -> str:
    """see https://stackoverflow.com/a/59056837/993881"""
    if alg not in hashlib.algorithms_available:
        raise ValueError(f"Unrecognized or unavailable algorithm: {alg}")

    chunk_size = 8192

    with open(filename, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(chunk_size):
            file_hash.update(chunk)

    return file_hash.hexdigest()