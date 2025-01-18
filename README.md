# SmartClaimAI

SmartClaimAI is an AI-driven solution designed to streamline and automate the refund claims process. By leveraging AI Agents, it enhances efficiency, accuracy, and customer satisfaction in claims management.

## Features

- **Automated Claim Processing**: Utilizes AI to assess and process claims swiftly, reducing manual intervention and processing time.
- **Image Analysis**: Employs Vision Language Models (VLMs) to evaluate uploaded images for damage assessment, ensuring accurate claim evaluations.
- **Natural Language Processing (Sentiment Analysis)**: Analyzes customer-submitted reviews/complaints to extract relevant information pertinent to the claim.
- **Fraud Detection**: Incorporates algorithms to identify and flag potentially fraudulent claims, safeguarding against losses.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yasho191/SmartClaimAI.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd SmartClaimAI
   ```

3. **Install Dependencies**:

   Ensure you To continue with the installation process for SmartClaimAI, please ensure you have the following prerequisites installed on your system:

### Prerequisites

- **Python 3.10 or higher**: SmartClaimAI is built using Python, so you'll need Python 3.10 or a later version installed.
- **Virtual Environment (optional but recommended)**: It's advisable to create a virtual environment to manage dependencies and avoid conflicts.

### Installation Steps

1. **Clone the Repository**:

   Open your terminal or command prompt and execute:

   ```bash
   git clone https://github.com/yasho191/SmartClaimAI.git
   ```

2. **Navigate to the Project Directory**:

    ```bash
    cd SmartClaimAI
    ```

3. **Set Up a Virtual Environment (Optional but Recommended)**:

    Create aand activate Virtual Environment:

    ```bash
    python -m venv smart_claim_env
    source smart_claim_env/bin/activate
    ```

4. **Install Dependencies**:

    Ensure you have `pip` installed, then run:

    ```bash
    pip install -r requirements.txt
    ```

    This command installs all necessary packages listed in the `requirements.txt` file.

5. **Set Up Environment Variables**:

   Create a `.env` file in the project root directory to store environment-specific variables, such as API keys and database credentials.

   Populate the `.env` file with the required variables as specified in the `.env.example` file.

## Supported Models

Currently, you can use `gpt-4o, gpt-4o-mini` or open-source model `microsoft/Phi-3.5-vision-instruct` as the vision language model for image analysis. For sentiment analysis the model used is `ProsusAI/finbert` which classifies sentiment as (Positive, negative and Neutral). For final summarization and processing you can use `gpt-4o or gpt-4o-mini`. (Open source model will be supported soon)

## Usage

After installation, you can use SmartClaimAI's Gradio dashboard to experiment with some text cases. To launch the dashboard just use the following:

```bash
python main.py
```

- **Submit Claims**: Use the application's interface to submit insurance claims with the necessary images.
- **Automated Processing**: Leverage AI capabilities for image analysis, sentiment analysis, and fraud detection to process claims efficiently.

**Dashboard Preview**
![Gradio Dashboard](https://github.com/yasho191/SmartClaimAI/blob/main/test/images/claim_refund_agent_preview.png)
