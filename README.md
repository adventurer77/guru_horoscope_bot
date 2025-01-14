# Guru Horoscope Bot

**Guru Horoscope Bot** is a Telegram bot that provides users with daily, weekly and monthly horoscopes for their chosen zodiac sign.

## Features

- Get daily, weeklyиand monthly horoscopes for your zodiac sign.
- Change your zodiac sign at any time.

## Technologies

- Python 3.9+
- [aiogram](https://docs.aiogram.dev/) library for Telegram API integration.

## Installation and Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/adventurer77/guru_horoscope_bot.git
   cd guru_horoscope_bot
   ```

2. **Create and activate a virtual environment:**

   - For Windows:

     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

   - For Linux/MacOS:

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the bot:**

   - Create a `.env` file in the root directory and add your Telegram bot token:

     ```
     BOT_TOKEN=your_bot_token_here
     ```

5. **Run the bot:**

   ```bash
   python app.py
   ```

## Usage

- Start the bot in Telegram and use the `/start` command to begin.
- Select Catalog/Horoscope, select your zodiac sign, and select Dates using the interactive keyboard. 
- Obtaining administrative rights (adding banners, zodiac signs and viewing them) takes place through the group. 
- Create a group - add a bot as an admin - write the /admin command.


## Contributions

- Feel free to submit pull requests and open issues to improve the bot's functionality.


