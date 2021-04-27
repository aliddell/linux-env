#!/usr/bin/env python3.8

import logging
from pathlib import Path
import re
import tarfile
from tempfile import mkdtemp

import requests
from bs4 import BeautifulSoup as Soup

from envutils.files import compute_file_checksum
from envutils.misc import err_exit


class JuliaInstaller:
    def __init__(self):
        self.tmpdir = Path(mkdtemp())
        self.major = self.minor = self.patch = ""

    def fetch_version(self):
        url = "https://julialang.org/downloads/"
        html = requests.get(url).content
        soup = Soup(html, "html.parser")

        csr_el = soup.select_one("#current_stable_release")

        ver_re = re.compile(r"v(\d+)\.(\d+)\.(\d+)")
        self.major, self.minor, self.patch = ver_re.search(csr_el.text).groups()

    def fetch_md5sum_file(self):
        filename = f"julia-{self.ver}.md5"
        url = f"https://julialang-s3.julialang.org/bin/checksums/{filename}"
        res = requests.get(url)

        with open(self.tmpdir / filename, "w") as fh:
            print(res.content.decode(), file=fh)

    def get_checksum_from_file(self) -> str:
        checksum = ""
        with open(self.tmpdir / self.checksum_filename, "r") as fh:
            while line := fh.readline():
                if str(self.tarball_filename) in line:
                    checksum = line.split()[0]
                    break

        if not checksum:
            raise ValueError

        return checksum

    def fetch_tarball(self):
        url = f"https://julialang-s3.julialang.org/bin/linux/x64/{self.major}.{self.minor}/{self.tarball_filename}"

        res = requests.get(url)
        with open(self.tmpdir / self.tarball_filename, "wb") as fh:
            fh.write(res.content)

    def validate_tarball(self) -> bool:
        checksum_actual = compute_file_checksum(self.tmpdir / self.tarball_filename, alg="md5")

        return self.get_checksum_from_file() == checksum_actual

    def extract_tarball(self):
        tar = tarfile.open(self.tmpdir / self.tarball_filename)
        tar.extractall("/opt")
        tar.close()

    def update_symlinks(self):
        if self.install_link.is_symlink():
            self.install_link.unlink()

        self.install_link.symlink_to(self.install_dir)

        if not self.bin_link.exists():
            self.bin_link.symlink_to(self.install_link / "bin" / "julia")

    def update_julia(self):
        try:
            self.fetch_version()
        except Exception as e:
            logging.error(e)
            return False

        if self.install_dir.is_dir():
            self.update_symlinks()
            return True

        try:
            self.fetch_md5sum_file()
            self.get_checksum_from_file()
            self.fetch_tarball()
            self.validate_tarball()
            self.extract_tarball()
            self.update_symlinks()
        except Exception as e:
            logging.error(e)
            return False

        return True

    @property
    def ver(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    @property
    def tarball_filename(self):
        return Path(f"julia-{self.ver}-linux-x86_64.tar.gz")

    @property
    def checksum_filename(self):
        return Path(f"julia-{self.ver}.md5")

    @property
    def install_dir(self):
        return Path(f"/opt/julia-{self.ver}")

    @property
    def install_link(self):
        return Path("/opt/julia")

    @property
    def bin_link(self):
        return Path("/usr/local/bin/julia")


def main():
    installer = JuliaInstaller()
    if not installer.update_julia():
        err_exit("Failed to update Julia.")


if __name__ == "__main__":
    main()
