# Running on EC2 Instance

## Prerequisites
- An EC2 instance running Ubuntu/Debian
- Python 3.x installed
- Git installed

## Step-by-Step Installation Guide

1. Clone the repository and navigate to project directory:
   ```bash
   git clone https://github.com/yushni/ai-chat
   cd ai-chat
   ```

2. Update system packages and install Python virtual environment:
   ```bash
   sudo apt update
   sudo apt install -y python3-venv
   ```

3. Create and activate a virtual environment:
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate
   ```

4. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the Streamlit application:
   ```bash
   streamlit run main.py
   ```

## Running in Background

To keep the application running after closing the SSH session:

1. Install screen (if not already installed):
   ```bash
   sudo apt install screen
   ```

2. Create a new screen session:
   ```bash
   screen -S chatapp
   ```

3. Activate the virtual environment and run the app:
   ```bash
   source myenv/bin/activate
   streamlit run main.py
   ```

4. Detach from the screen session:
   - Press `Ctrl + A`, then `D`
   - Your app will continue running in the background

5. To reattach to the session later:
   ```bash
   screen -r chatapp
   ```
