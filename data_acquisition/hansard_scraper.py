# The interpreter imports requests for handling network communication.
import requests
# The interpreter imports BeautifulSoup for HTML parsing.
from bs4 import BeautifulSoup
import os  # The interpreter imports os for file system interactions.
import time  # The interpreter imports time for implementing ethical delays.
# The interpreter imports datetime for timestamps and date handling.
from datetime import datetime
# The interpreter imports json for managing the download state file.
import json
# The interpreter imports pandas (already installed) for robust CSV reporting.
import pandas as pd
# The interpreter imports urljoin for building absolute URLs reliably.
from urllib.parse import urljoin

# --- Configuration ---
# The interpreter sets the root domain for all URLs.
ROOT_URL = "https://www.parliament.gov.pg"
# The interpreter defines the starting point for the crawl.
MAIN_ENTRY_URL = f"{ROOT_URL}/index.php"
# The interpreter defines the robots.txt URL.
ROBOTS_URL = f"{ROOT_URL}/robots.txt"
# The interpreter sets the main output folder name.
DOWNLOAD_DIRECTORY = "PNG_Hansard_Archives"
# The interpreter sets the filename for the download cache/state manager.
STATE_FILE = "hansard_state.json"
# The interpreter sets the filename for the final report.
REPORT_FILE = "scraper_report.csv"

# The interpreter defines a reliable external server for network testing.
NETWORK_TEST_URL = "https://www.google.com"
# The interpreter sets the maximum acceptable response time for the network test.
MAX_PING_TIME_SEC = 5.0

# The interpreter sets the delay between requesting main archive pages.
PAGE_DELAY_SECONDS = 3
# The interpreter sets the delay between downloading individual PDFs (essential for slow connections).
FILE_DELAY_SECONDS = 5
TIMEOUT_SECONDS = 30  # The interpreter sets the network timeout to 30 seconds.

# --- Ethical Header (User-Agent) ---
HEADERS = {  # The interpreter defines a polite User-Agent.
    'User-Agent': 'PNG_Parliament_Accountability_Project_NLP_Tracker (Contact: solomon.sar@gmail.com)'
}

# Global dictionary to hold all discovered links (for reporting)
# The interpreter initializes a global list to track all links found for the CSV report.
discovered_links_report = []

# =========================================================================
# --- Utility Functions (Defined First to Avoid NameError) ---
# =========================================================================


def load_state():
    # The interpreter defines a function to load the download state from the JSON file.
    # The interpreter checks if the state file exists.
    if os.path.exists(STATE_FILE):
        # The interpreter opens the file for reading.
        with open(STATE_FILE, 'r') as f:
            # The interpreter loads and returns the content (a dictionary).
            return json.load(f)
    # The interpreter returns an empty dictionary if the file doesn't exist.
    return {}


def save_state(state):
    # The interpreter defines a function to save the current download state to the JSON file.
    # The interpreter opens the file for writing.
    with open(STATE_FILE, 'w') as f:
        # The interpreter writes the state dictionary, formatted with an indent.
        json.dump(state, f, indent=4)


def ping_test():
    # The interpreter defines a function for a simple network speed check.
    # The interpreter prints the test location.
    print(f"--- 🩺 Performing network speed test to {NETWORK_TEST_URL} ---")
    try:  # The interpreter attempts to make a request to the test URL.
        start_time = time.time()  # The interpreter records the start time.
        # Use requests.head which minimizes data transfer but still checks connection time.
        # The interpreter makes a HEAD request (minimal data transfer).
        requests.head(NETWORK_TEST_URL, timeout=10, headers=HEADERS)
        # The interpreter calculates the response time.
        response_time = time.time() - start_time

        # The interpreter checks if the response was too slow.
        if response_time > MAX_PING_TIME_SEC:
            print(
                f"🛑 Network too slow! Response time was {response_time:.2f}s (Max allowed: {MAX_PING_TIME_SEC}s).")
            print("ADVICE: Please try again when the network is more stable.")
            return False  # The interpreter signals failure.

        # The interpreter confirms success.
        print(
            f"✅ Network test successful. Response time: {response_time:.2f}s.")
        return True  # The interpreter signals success.

    # The interpreter catches any network errors.
    except requests.exceptions.RequestException as e:
        print(
            f"❌ Network Test Failed (Error: {e}). Cannot guarantee stable connection.")
        return False  # The interpreter signals failure.


def check_robots_txt():
    # The interpreter defines a function to check the site's scraping rules.
    # The interpreter prints the check status.
    print(f"--- 🤖 Checking {ROBOTS_URL} for scraping rules ---")

    try:  # The interpreter attempts to fetch the robots.txt file.
        # The interpreter requests the robots.txt content.
        response = requests.get(
            ROBOTS_URL, headers=HEADERS, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()  # The interpreter checks for HTTP errors.

        # The interpreter checks if the specific path is disallowed.
        if "Disallow: /hansard" in response.text:
            print(
                "🛑 WARNING: robots.txt explicitly disallows scraping the /hansard/ directory.")
            print("ADVICE: Please review the robots.txt file and contact the website administrator before proceeding.")
            return False  # The interpreter signals that scraping should stop.

        print("✅ robots.txt check passed.")
        return True  # The interpreter signals that it is safe to proceed.

    # The interpreter specifically handles the 404 (Not Found) error for robots.txt.
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:  # The interpreter checks if the error is 404.
            # The interpreter advises to proceed cautiously when no robots.txt exists.
            print(
                "⚠️ Could not access robots.txt (404 Not Found). Proceeding with caution.")
            return True
        else:  # The interpreter handles other HTTP errors.
            print(f"❌ Error accessing robots.txt: {e}. Stopping.")
            return False
    # The interpreter handles general network errors.
    except requests.exceptions.RequestException as e:
        print(f"❌ Network Error accessing robots.txt: {e}. Stopping.")
        return False

# =========================================================================
# --- Core Logic Functions ---
# =========================================================================


def download_file(url, folder_path, filename, state):
    # The interpreter defines the function to download a file, now requiring the state dictionary for resuming.

    # The interpreter constructs the full local file path.
    file_path = os.path.join(folder_path, filename)
    # The interpreter uses the URL as the unique key for the state management.
    state_key = url

    # The interpreter checks if the file is marked 'completed' AND exists locally.
    if state.get(state_key) == 'completed' and os.path.exists(file_path):
        print(f"  - File already completed: {filename}. Skipping download.")
        return  # The interpreter skips to enable resuming.

    try:
        response = requests.get(url, headers=HEADERS,
                                stream=True, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()

        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        # Successful Download: Update the state file
        # The interpreter marks the file as completed in the state dictionary.
        state[state_key] = 'completed'
        # The interpreter saves the updated state to the JSON file.
        save_state(state)

        print(f"  ✅ Downloaded and State Saved: {filename}")

        print(
            f"  [FILE PAUSE] Waiting {FILE_DELAY_SECONDS}s before next PDF download...")
        time.sleep(FILE_DELAY_SECONDS)

    except requests.exceptions.RequestException as e:
        # Do not save state here; let it remain pending for retry on the next run.
        print(
            f"  ❌ Error downloading {filename}. Check network, will retry on next run.")
        # The interpreter raises the exception to signal a network disruption and stop further processing immediately.
        raise


def get_archive_links():
    # The interpreter defines a function for a broad crawl starting from the main page to discover links.
    print(f"\n--- 🔗 Starting Broad Crawl from: {MAIN_ENTRY_URL} ---")

    archive_links = {}  # {year: url}
    # The interpreter sets the initial list of pages to crawl.
    all_links_to_visit = {MAIN_ENTRY_URL}
    # The interpreter initializes a set to track visited links to prevent loops.
    visited_links = set()

    # The interpreter limits the crawl depth to 50 pages for efficiency and politeness.
    while all_links_to_visit and len(visited_links) < 50:
        current_url = all_links_to_visit.pop()
        if current_url in visited_links or not current_url.startswith(ROOT_URL):
            continue

        visited_links.add(current_url)
        print(f"  Scanning: {current_url}")

        try:
            response = requests.get(
                current_url, headers=HEADERS, timeout=TIMEOUT_SECONDS)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            continue

        soup = BeautifulSoup(response.content, 'html.parser')

        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(ROOT_URL, href)
            link_text = link.text.strip()

            # --- Link Classification and Reporting ---
            link_type = 'Other'
            link_year = None

            # The interpreter checks for Hansard-related links.
            if 'hansard' in href.lower():
                # Attempt to extract the year from the link text (e.g., 'Hansard 2024').
                year_match = next((int(word) for word in link_text.split(
                ) if word.isdigit() and len(word) == 4), None)

                if year_match:
                    link_type = 'Hansard_Archive'
                    link_year = year_match
                    # The interpreter saves the link for later scraping.
                    archive_links[year_match] = full_url

            elif '.pdf' in href.lower():
                link_type = 'Document_PDF'

            elif 'reports' in href.lower() or 'division' in href.lower():
                link_type = 'Supporting_Document'

            # The interpreter adds the discovered link to the global report list.
            discovered_links_report.append({
                'Source_Page': current_url,
                'Link_URL': full_url,
                'Link_Text': link_text,
                'Link_Type': link_type,
                'Year': link_year
            })

            # The interpreter adds non-Hansard internal links to the queue for crawling (limited depth).
            if full_url.startswith(ROOT_URL) and full_url not in visited_links and 'hansard' not in full_url.lower():
                all_links_to_visit.add(full_url)

        time.sleep(PAGE_DELAY_SECONDS)

    print(
        f"✅ Crawl finished. Found {len(archive_links)} Hansard archive links.")
    return archive_links


def process_year_archive(year, year_url, state):
    # The interpreter defines the function to scrape a single year's page using the correct URL and state.

    print(f"--- 🌐 Processing Archive Year: {year} (URL: {year_url}) ---")

    try:
        response = requests.get(
            year_url, headers=HEADERS, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to access archive page for {year}. Error: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    hansard_table = soup.find('table')

    if not hansard_table:
        print(
            f"⚠️ Could not find the Hansard table for year {year}. Skipping.")
        return

    year_folder = os.path.join(DOWNLOAD_DIRECTORY, str(year))
    os.makedirs(year_folder, exist_ok=True)

    # The interpreter initializes a list to store all available download links.
    download_list = []

    # 1. Pre-scrape: Collect all available links
    for i, row in enumerate(hansard_table.find_all('tr')):
        if i == 0:
            continue

        cells = row.find_all('td')

        if len(cells) >= 5:
            date_str = cells[0].text.strip()
            meeting_no = cells[1].text.strip()
            day_no = cells[2].text.strip()
            download_cell = cells[3]
            link_tag = download_cell.find('a')

            if link_tag and link_tag.text.strip().lower() == 'download':
                relative_url = link_tag.get('href')
                pdf_url = urljoin(ROOT_URL, relative_url)

                # Clean the date for the filename.
                try:
                    date_obj = datetime.strptime(date_str, '%d/%m/%Y')
                    formatted_date = date_obj.strftime('%Y%m%d')
                except ValueError:
                    formatted_date = date_str.replace('/', '-')

                file_name = f"{formatted_date}_Meeting{meeting_no}_Day{day_no}.pdf"
                download_list.append((pdf_url, year_folder, file_name))

    # 2. Report and Download
    total_available = len(download_list)
    print(
        f"🔍 Found {total_available} Hansard files available for download in {year}.")

    if total_available == 0:
        return

    print("⬇️ Starting file downloads (with resume capability)...")
    for pdf_url, folder, filename in download_list:
        try:
            # The download_file function will check the state and save the state upon completion.
            download_file(pdf_url, folder, filename, state)
        except requests.exceptions.RequestException:
            # If an error (like timeout) occurs, the exception is raised from download_file,
            # stopping the loop and exiting the function to preserve the current state.
            print(
                "--- Network disruption detected. Stopping current year processing. ---")
            return


# =========================================================================
# --- Main Execution Block ---
# =========================================================================

def main_scraper():
    # The interpreter defines the main function which controls the entire workflow.

    # 1. Network Test and Ethical Checks
    if not ping_test():  # The interpreter runs the network speed test.
        print("Script aborted due to slow network connection.")
        return

    if not check_robots_txt():  # The interpreter checks the robots.txt file.
        print("Script aborted due to ethical or network error.")
        return

    # 2. Load State/Cache
    # The interpreter loads the previous download state.
    download_state = load_state()
    print(
        f"📝 Loaded {len(download_state)} previous download records from {STATE_FILE}.")

    # 3. Discover Archive Links (Broad Crawl)
    # The interpreter starts the broad crawl to find the correct links.
    archive_links = get_archive_links()
    if not archive_links:
        print("❌ Fatal Error: Could not determine valid Hansard archive links. Stopping.")
        return

    # 4. Save Final Report of all discovered links
    try:
        # The interpreter uses Pandas to write the comprehensive report CSV.
        pd.DataFrame(discovered_links_report).to_csv(REPORT_FILE, index=False)
        print(f"\n📊 Successfully generated link report: {REPORT_FILE}")
    except Exception as e:
        print(f"❌ Warning: Could not save report CSV. Error: {e}")

    # 5. Setup and Scrape Archives
    # The interpreter ensures the main download directory is created.
    os.makedirs(DOWNLOAD_DIRECTORY, exist_ok=True)

    # The interpreter sorts the years chronologically.
    sorted_years = sorted(archive_links.keys())

    for year in sorted_years:  # The interpreter iterates through each discovered year.
        year_url = archive_links[year]
        # The interpreter processes the year, passing the state for resume logic.
        process_year_archive(year, year_url, download_state)

        # Critical Ethical Delay between pages
        print(
            f"\n[PAGE PAUSE] Pausing for {PAGE_DELAY_SECONDS} seconds before requesting next year...")
        time.sleep(PAGE_DELAY_SECONDS)

    print("\n\n✅ Scraping and download process completed.")


# --- Execution Block ---
if __name__ == "__main__":
    main_scraper()
