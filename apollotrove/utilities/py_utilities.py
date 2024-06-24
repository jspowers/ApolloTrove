import urllib.parse

# --------------------------------- #
# VALUE MASK:
# for hiding sensitive data
# --------------------------------- #
def get_value_mask(raw_value: str) -> str:
    if raw_value == None or len(raw_value) <= 1:
        return None
    elif len(raw_value) > 20:
        return raw_value[:4] + '.' * 8 + raw_value[-10:]
    elif len(raw_value) < 10:
        return 'x' * 4 + raw_value[-1:]
    else:
        return raw_value[:2] + '.' * 4 + raw_value[-4:]


# --------------------------------- #
# Parse the URL: Split the URL into its components (scheme, netloc, path, and query).
# Encode the query parameters: Properly encode the query parameters to ensure they are formatted correctly for a URL.
# Rebuild the URL: Combine the encoded components back into a full URL.
# --------------------------------- #
def encode_url_request(raw_url):
        # Parse the URL into components
        parsed_url = urllib.parse.urlparse(raw_url)
        # Encode the query parameters
        encoded_query = urllib.parse.quote(parsed_url.query, safe='=&+')
        # Rebuild the full URL
        encoded_url = urllib.parse.urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, encoded_query, parsed_url.fragment))

        return encoded_url
        