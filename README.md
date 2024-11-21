
## Medical Note Summarization API incorporating ChatML Custom Dataset Processing

This project provides a **Flask-based API** to process medical notes, extract meaningful sections, and generate summaries using **OpenAI's GPT-3.5-turbo** model. It also formats the extracted information and summaries into a structured ChatML format.

---

## Features

1. **Medical Note Summarization**:
   - Extracts and summarizes key sections (e.g., chief complaint, assessment, investigations, plan/treatment) from medical notes.
   
2. **ChatML Formatting**:
   - Organizes the extracted information and generated summaries into a structured format for seamless integration with conversational agents.

3. **CSV File Support**:
   - Processes medical notes from uploaded CSV files. Handles rows with a `TEXT` column containing the notes.

4. **Error Handling**:
   - Skips invalid rows in the uploaded file.
   - Returns meaningful error messages for missing or invalid inputs.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Create a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   - Create a `.env` file in the project root.
   - Add your **OpenAI API key**:
     ```
     OPENAI_API_KEY=your_openai_api_key
     ```

5. **Run the Application**:
   ```bash
   python3 app.py
   ```

---

## Usage

### API Endpoint
**POST** `/process`

#### Request
- **File Upload**: Upload a CSV file with a `TEXT` column containing medical notes.

#### Example CURL Request
```bash
curl -X POST -F "file=@path/to/medical_notes.csv" http://127.0.0.1:5000/process
```

#### Response
- `summaries`: A list of extracted and summarized content.
- `chatml_format`: A structured representation of extracted information in ChatML format.

#### Response Example
```json
{
    "summaries": [
        {
            "EXTRACTED": {
                "chief_complaint": "Patient reports chest pain and shortness of breath...",
                "assessment": "Likely myocardial infarction...",
                "investigations": "EKG shows ST elevation...",
                "plan_treatment": "Administer aspirin and prepare for cath lab..."
            },
            "SUMMARY": {
                "chief_complaint": "The patient complains of chest pain and shortness of breath.",
                "assessment": "The patient is assessed to have a myocardial infarction.",
                "investigations": "EKG indicates ST elevation consistent with MI.",
                "plan_treatment": "Administer aspirin and prepare the patient for the cath lab."
            }
        }
    ],
    "chatml_format": [
        {
            "role": "user",
            "content": "Chief Complaint:\n\nPatient reports chest pain and shortness of breath..."
        },
        {
            "role": "assistant",
            "content": "Summary of Chief Complaint:\n\nThe patient complains of chest pain and shortness of breath."
        }
    ]
}
```

---

## File Format Requirements
- **CSV**:
  - Must contain a `TEXT` column with medical notes.

---

## Key Components

### `generate_summary(prompt)`
- Sends a request to the OpenAI GPT-3.5-turbo API to generate a summary.
- Returns a concise summary or error message.

### `format_chatml(extracted_info, summaries)`
- Converts extracted and summarized information into a structured ChatML format for conversational agents.

### `is_meaningful(text)`
- Filters out non-meaningful text based on word count.

### `/process` Endpoint
- Upload a CSV file containing medical notes.
- Extracts sections such as:
  - `chief_complaint`
  - `assessment`
  - `investigations`
  - `plan_treatment`
- Generates concise summaries for each section.
- Returns structured data in JSON format.

---

## Requirements
- Python 3.8 or later
- Flask
- pandas
- tqdm
- OpenAI Python SDK (`openai`)

---

## Future Enhancements
- Add support for other file formats (e.g., JSON, Excel).
- Improve error handling and logging.
- Extend the extraction logic for more granular medical note details.
- Include authentication and rate-limiting for secure API access.

---

## License
This project is licensed under the MIT License. 

---

## Author
Developed by **[Solomon Amaning Odum]**.
