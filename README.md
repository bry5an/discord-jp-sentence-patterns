# Discord Japanese Fluency Bot

A grammar-first Discord bot designed to help adult learners build spoken Japanese fluency. It ingests your active vocabulary, pairs it with high-leverage grammar patterns, and generates natural, casual spoken sentences using AI.

## Features

### 1. Active Vocabulary Ingestion
Dictionary definitions don't create fluency. Context does.
-   **Channel**: `#active-vocab-inbox`
-   **Usage**: Just type a word you want to master (e.g., `気になる`).
-   **Bot Action**:
    1.  Checks dictionary definitions (optional).
    2.  Selects 2-3 casual grammar patterns compatible with the word.
    3.  Generates **spoken, first-person sentences** using Google Gemini.
    4.  Saves everything to the database for future review.

### 2. Grammar-First Practice
Reinforce grammar patterns by seeing them used with your existing vocabulary.
-   **Channel**: `#grammar-inbox`
-   **Usage**: Type a grammar pattern (e.g., `～てるんだけど`).
-   **Bot Action**:
    1.  Finds 2-3 words from your **existing** active vocabulary.
    2.  Generates new conversation examples combining the grammar + your words.

### 3. Database-Backed
All data is stored in **Supabase (PostgreSQL)**, creating a personal phrasebook of sentences that actually mean something to you.

---

## Hosting Requirements

To host this bot, you need:

1.  **Python 3.12+**
2.  **Supabase Project**: A free Supabase project for the PostgreSQL database.
3.  **Discord Bot Token**: From the [Discord Developer Portal](https://discord.com/developers/applications).
4.  **Google Gemini API Key**: From [Google AI Studio](https://aistudio.google.com/).

## Setup Guide

### 1. Clone & Install Dependencies
This project uses `uv` for modern Python dependency management.

```bash
# Install uv if you haven't already
pip install uv

# Clone the repository
git clone <repo-url>
cd discord-jp-sentence-patterns

# Sync dependencies (creates virtualenv automatically)
uv sync
```

### 2. Environment Variables
Create a `.env` file in the root directory:

```ini
# Discord
DISCORD_TOKEN=your_discord_bot_token

# Supabase (Settings -> API)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_public_key

# Google Gemini
GEMINI_API_KEY=your_google_api_key
```

### 3. Database Setup
Run the SQL migration files located in the `sql/` directory in your Supabase SQL Editor in the following order:

1.  `active_vocab_table.sql`
2.  `grammar_patterns_table.sql`
3.  `example_phrases_table.sql`
4.  `usage_history.sql`
5.  `seed.sql` (Important: Seeds the initial grammar patterns)

### 4. Running the Bot

**Local Development:**
```bash
uv run python main.py
```

**Production (e.g., VPS, Docker):**
Ensure `uv` is installed and run the same command, or build a Docker image based on the python environment.

## Channel Setup in Discord
Create two text channels in your server:
-   `#active-vocab-inbox`
-   `#grammar-inbox`

The bot listens specifically to these channel names.
