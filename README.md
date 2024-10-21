# Python Sitemap Generator

This Python project generates or updates XML sitemaps for a list of websites. It scrapes the provided websites, collecting all internal links and outputs the results into a well-structured sitemap. The sitemap files are saved in a directory named after each site's domain. This project can be used to automate the generation of sitemaps for SEO purposes.

## Features

- **Scrapes URLs**: Crawls internal URLs of the provided websites.
- **Sitemap Generation**: Creates or updates the XML sitemap in a folder named after the domain.
- **User-Agent Rotation**: Uses a list of different user-agents to bypass basic anti-scraping measures. If a request is blocked (HTTP 403), it retries up to 2 times with a different user-agent.
- **Depth Control**: Allows you to control how deep to crawl through each website.
- **Pretty-Printed XML**: The sitemap is saved with indentation and proper formatting for better readability.

---

## Prerequisites

To run this project, you will need:

- **Python 3.x**: You can download Python from [here](https://www.python.org/downloads/).
- **`pip` package manager**: Python's package manager to install required libraries.

### Required Libraries

The following libraries need to be installed:

- `requests` – To handle HTTP requests.
- `beautifulsoup4` – To parse HTML content.
- `lxml` – XML parser to handle the HTML/XML parsing reliably.

You can install all the dependencies using `pip` with the following instructions.

---

## Installation

### Step 1: Install Python

1. Download and install Python from the official website: [Download Python](https://www.python.org/downloads/).
2. Make sure Python is added to your system's `PATH` during installation (check the option during setup).

You can check if Python is installed by running:

```bash
python --version
```

or 

```bash
python3 --version
```

### Step 2: Install Required Python Libraries

Install the required Libraries:

```bash
pip install requests
pip install beautifulsoup4
pip install lxml
```

### Step 3: Create a `websites.txt` File

Add the domains to the `websites.txt` file as follows:

```
https://example.com/
https://another-example.com/
```

### Step 4: Running the Sitemap Generator

When you have installed Python and the required libraries and added the required domains to the `websites.txt` file, you can run the script with the following command:

```bash
python generate.py
```

This will:

- Load the URLs from `websites.txt`.
- Crawl each website to scrape all internal URLs up to the specified depth (default depth is 3).
- Save the sitemap in a folder named after the domain (e.g., `example.com/sitemap.xml`).
- Retry up to two times if a `403 Forbidden` error is encountered, using different user-agents.

### How It Works

The script reads URLs from the `websites.txt` file, validates them, and scrapes each website for internal links. It then generates an XML sitemap in the following format:

```xml
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2023-10-20</lastmod>
  </url>
  <url>
    <loc>https://example.com/page1</loc>
    <lastmod>2023-10-20</lastmod>
  </url>
  <!-- More URLs -->
</urlset>
```

### Key Components

- **User-Agent Rotation**: The script rotates through a list of user-agent strings to make requests appear as if they are coming from different browsers. This helps avoid basic anti-scraping measures.

- **Retry Mechanism**: If a request fails due to a `403 Forbidden` error, the script retries with a different user-agent up to 2 times before moving on to the next URL.

- **Depth Control**: The script will crawl links up to the specified depth (default is 3). For example, if depth is set to 3, it will collect URLs linked from the homepage, then URLs linked from those URLs, and one more level deeper.

- **Saving Sitemaps**: The sitemaps are saved as formatted XML files in a folder named after each domain. If the folder or sitemap already exists, it will update the sitemap with new URLs.
