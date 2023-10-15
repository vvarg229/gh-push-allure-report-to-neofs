import os
import requests
import pytest
from urllib.parse import urljoin


def download_file(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def list_all_files(directory: str) -> list:
    all_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, directory)
            all_files.append(relative_path)

    return all_files


def test_file_content(base_url, report_dir):
    if base_url is None:
        pytest.skip("base_url is not provided. Provide it using --base_url option.")
    print(f"base_url: {base_url}")

    if report_dir is None:
        pytest.skip("report_dir is not provided. Provide it using --report_dir option.")
    print(f"report_dir: {report_dir}")

    all_files = list_all_files(report_dir)

    for file in all_files:
        print(f"file: {file}")
        full_url = urljoin(base_url, file)
        print(f"full_url: {full_url}")
        remote_content = download_file(full_url)

        with open(os.path.join(report_dir, file), "r") as local_file:
            local_content = local_file.read()

        assert (
            remote_content == local_content
        ), f"Contents of {full_url} and {file} do not match."
