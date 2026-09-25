import requests

BASE_URL = "https://api.kickbase.com/v4"

# Maximum time to wait for a Kickbase API response.
REQUEST_TIMEOUT = 15


def get_json_with_token(url, token):
    """Fetch JSON data from a given URL using token for authorization."""

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:
        raise RuntimeError(
            f"Kickbase API request timed out after "
            f"{REQUEST_TIMEOUT} seconds: {url}"
        )

    except requests.exceptions.HTTPError as error:
        raise RuntimeError(
            f"Kickbase API returned HTTP {response.status_code}: "
            f"{url}"
        ) from error

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"Kickbase API request failed: {url}"
        ) from error

    except ValueError as error:
        raise RuntimeError(
            f"Kickbase API returned invalid JSON: {url}"
        ) from error
