import concurrent.futures
import requests
import time


def check_status(url):
    try:
        response = requests.get(url, timeout=10)
        return url, response.status_code
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
        return url, str(e)


def main():
    with open('links.txt') as f:
        urls = f.readlines()

    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(check_status, url.strip()) for url in urls]

        total_links = len(urls)
        links_checked = 0
        results = []
        errors = []
        for future in concurrent.futures.as_completed(futures):
            url, status = future.result()
            if isinstance(status, int) and status == 200:
                results.append(url)
            else:
                errors.append((url, status))
            links_checked += 1
            print(f"\rChecked {links_checked}/{total_links} links. "
                  f"Progress: {100 * links_checked / total_links:.2f}%", end="")

        print("\nResults:")
        for url in results:
            print(url)

        print("\nErrors:")
        for url, error in errors:
            print(f"{url} - {error}")


if __name__ == '__main__':
    main()
