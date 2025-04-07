import requests
from bs4 import BeautifulSoup

def decode_secret_message(doc_url):
    response = requests.get(doc_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    tables = soup.find_all('table')
    print(f"Found {len(tables)} tables")

    if not tables:
        print("No tables found in the document.")
        return

    table = tables[0]
    rows = table.find_all('tr')
    print(f"Found {len(rows)} rows in the first table")

    coords = []
    max_x = max_y = 0

    for i, row in enumerate(rows):
        cells = row.find_all(['td', 'th'])
        if len(cells) < 3:
            continue

        raw_x = cells[0].get_text(strip=True)
        raw_char = cells[1].get_text(strip=True)
        raw_y = cells[2].get_text(strip=True)

        print(f"Row {i}: x='{raw_x}', y='{raw_y}', char='{raw_char}'")

        try:
            x = int(raw_x)
            y = int(raw_y)
        except ValueError:
            print(f"Skipping row {i}: x or y not valid integers")
            continue

        coords.append((x, y, raw_char))
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    if not coords:
        print("No valid coordinates found.")
        return

    # Build grid (y rows, x cols)
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    for x, y, char in coords:
        grid[y][x] = char

    print("\nDecoded Message:\n")
    for row in grid:
        print(''.join(row))

# Run the function with the doc link
decode_secret_message("https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub")
