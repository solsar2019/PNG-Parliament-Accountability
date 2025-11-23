# PNG-Parliament-Accountability

This repository houses the code and documentation for a civic tech initiative designed to enhance political accountability in Papua New Guinea through Natural Language Processing (NLP) analysis of parliamentary transcripts.

# 🇵🇬 PNG Parliament Accountability NLP Tracker

## 🎯 I. Project Vision & Goals

* **Vision:** To create a transparent, data-driven platform that monitors the legislative actions, policy focus, and public commitments of all Members of the PNG National Parliament.
* **Mission:** To transform complex, unstructured parliamentary data (Hansard) into accessible, structured metrics that empower citizens, journalists, and civil society organizations (CSOs) to hold representatives accountable.
* **Primary Goal (MVP):** Systematically scrape, clean, and analyze **Hansard** transcripts to create a structured database of *who said what, when, and on what policy topic*.

---

## ⚖️ II. Governance, Legality & Ethics

### A. Legal Compliance & Ethics
1.  **Non-Profit & Open Data:** This project is strictly **non-profit**, educational, and committed to **Open Data Commons Public Domain Dedication and License (PDDL)** for all derived data.
2.  **PNG Law Adherence:** We are committed to adhering to the PNG Constitution (Section 51 - Right of Reasonable Access to Official Documents) and all applicable laws, including those regarding defamation and data privacy.
3.  **Open Source:** All code is released under the **MIT License**.

### B. Disclaimer (Crucial for Legal Safety)
The analysis generated (topic modeling scores, sentiment scores, commitment lists) is **data-driven** and **not the opinion of the project team or its members**. Users are responsible for their own interpretation and application of the data. We commit to citing the original Hansard source for all extracted quotes.

### C. Formalization Path
The project will be managed by the core contributors. Formalizing the project (e.g., establishing a Board or registering as a Society/NGO) will be considered when the project exceeds **5-7 dedicated core contributors** OR when the project receives **external grants/funding**.

---

## 🛠️ III. Technical Stack & Methodology

### A. Data Sources
* **Phase 1 Focus:** PNG National Parliament **Hansard** (Record of Proceedings).
* **Future Sources:** PNG News Media, Official Parliamentary Video Streams (YouTube), Ministerial Statements, and Budget Documents.

### B. Technical Stack
| Category | Tool/Library | Rationale |
| :--- | :--- | :--- |
| **Language** | Python | Standard for data science and NLP. |
| **Data Engineering** | `requests`, `BeautifulSoup`, `pypdf`/`PyMuPDF`, `pandas` | Required for scraping HTML, downloading PDFs, extracting text, and structuring data. |
| **Database** | **PostgreSQL/PostGIS** (Recommended) or **SQLite** (MVP) | Essential for storing structured, segmented data and enabling **GIS Integration**. |
| **GIS** | **QGIS** (Open Source) | For visualizing policy discussions spatially (linking extracted place names to maps). |

### C. Machine Learning Approach (NLP)
* **Methodology:** **Hybrid ML/DL.** We start with traditional ML (`scikit-learn`) for a quick MVP and will transition to **Deep Learning (Transformers)** for higher accuracy on large datasets.
* **DL Resource Strategy:** All intensive Deep Learning model training will utilize **Google Colab's free GPU/TPU resources** to eliminate hardware costs for volunteers.

### D. Key ML Tasks
1.  **Speaker Segmentation:** (The Hardest Step) Using **Regular Expressions (RegEx)** to separate each speaker's name, date, and their exact speech text.
2.  **Topic Modeling:** (Unsupervised) To automatically identify recurring policy themes (e.g., Fisheries, Land Reform).
3.  **Named Entity Recognition (NER):** To extract all **PNG Place Names** (Provinces, Districts) for QGIS mapping.
4.  **Text Classification:** To categorize speeches (e.g., 'Commitment,' 'Critique,' 'Procedural').

---

## 🤝 IV. Collaboration & Dissemination

### A. Collaboration Platforms
* **Code & Project Management:** **GitHub** (This repository; Issues for task tracking).
* **Local Communication:** **WhatsApp** (For rapid, accessible communication within PNG).
* **Online Meetings:** **Jitsi Meet** or **BigBlueButton** (Free, open-source alternatives for video conferencing).

### B. Volunteer Workflow
Volunteers are encouraged to select tasks labeled with appropriate skill tags (e.g., `skill:python-scraper`, `skill:nlp-beginner`, `skill:qgis-mapper`). The path includes training in data engineering, NLP, and documentation.

### C. Publishing & Deployment
1.  **Primary Host:** **GitHub** (Code and raw data files).
2.  **Interactive Dashboard:** **GitHub Pages** or **Netlify** (Free services for hosting the final web application/Commitment Tracker).
3.  **Social Media:** Regular updates on platforms like **Facebook/X** will drive public traffic to the main project dashboard.

---

## 🗺️ V. Project Roadmap (MVP)

| Phase | Goal | Key Deliverable |
| :--- | :--- | :--- |
| **Phase 1: Data Acquisition** | Obtain and structure all raw data. | **`hansard_archive.csv`**: A single, structured dataset ready for analysis. |
| **Phase 2: Core Analysis** | Run initial ML models. | **Commitment Dashboard:** Visualization of MP speeches, top topics, and initial sentiment scores. |
| **Phase 3: Spatial Integration** | Link text data to geography. | **QGIS Map Layer:** Showing policy discussion frequency mapped to PNG Provinces/Districts. |

---
## 🚀 Getting Started

Follow these steps to set up the project environment and run the Hansard scraper.

### Prerequisites
* **Python 3.10+**
* **Google Chrome/Chromium** (Required for the Selenium scraper to function in headless mode).

### Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/solsar2019/PNG-Parliament-Accountability.git](https://github.com/solsar2019/PNG-Parliament-Accountability.git)
    cd PNG-Parliament-Accountability
    ```
2.  **Create and Activate Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install Required Libraries:**
    ```bash
    pip install -r requirements.txt
    ```

### Execution

Run the main scraper script from the root directory:

```bash
(venv) python data_acquisition/hansard_scraper.py
