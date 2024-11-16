
# WhatsApp Chat Analyzer

This project helps you analyze WhatsApp chat files by determining whether messages are original or forwarded using OpenAI's API. The tool can perform both individual and group-level analysis.

## Installation

1. Clone the repository to your local machine.
  ```bash
   git clone https://github.com/Amit-Rohila33/Whatsapp-Chats-Analyser.git
   ```
2. Install the required Python packages by running:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Navigate to the project directory in your terminal.
2. Start the Streamlit app using the following command:

   ```bash
   streamlit run app.py
   ```

## Usage

1. **Enter Group Name**: Start by entering the name of the WhatsApp group you want to analyze.
2. **Select Group Type**: Choose the type of group (you can choose "Other" if it does not fit any predefined categories).
3. **Upload WhatsApp Chat File**: Upload the `.txt` file that you have exported from WhatsApp.
4. **Table Generation**: Once the file is uploaded, a table of messages will be generated.
5. **Choose Analysis Type**:
   - You can select either **Individual** or **Group** analysis.
   - The analysis will categorize the messages based on whether they are original or forwarded, and is completely anonymized

## Notes

- The analysis can take some time, as the app fetches data from the OpenAI API, especially to determine the originality or forwarded status of the messages.
- In app.py file, please update your OpenAI API key
  
