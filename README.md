# Github Issues Discord Bot

A simple Discord bot that retrieves issues from a (private) GitHub repository and displays them in Discord as an embed. It can be configured to show only open issues, issues with a specific label, or any custom filtering you prefer.

## Features

- **Retrieve GitHub issues** from a private repository using a Personal Access Token (PAT).  
- **Display issues** in Discord with a single command (`!kanban` or any command name you choose).  
- **Handles long lists** of issues by splitting the output into multiple fields (to avoid Discord’s 1024-character limit per embed field).  
- **Easily configurable** via environment variables.

## Requirements

- **Python 3.8+** (recommended)  
- **pip** for installing dependencies  
- **Discord Bot Token** (from [Discord Developer Portal](https://discord.com/developers/applications))  
- **GitHub Personal Access Token** (with at least `read` access to issues in your private repo)

## Setup

1. **Clone or download** this repository.
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Your `requirements.txt` should include packages like:
   - `discord.py` or `py-cord`  
   - `python-dotenv`  
   - `requests`
3. **Rename the `.env.example` file to `.env`** in the root directory. It should include:
   ```bash
   DISCORD_TOKEN=<your_discord_bot_token>
   GITHUB_TOKEN=<your_github_personal_access_token>
   GITHUB_REPO_OWNER=<your_github_username_or_org>
   GITHUB_REPO_NAME=<your_repository_name>
   ```
4. **Configure Discord Intents** in the [Discord Developer Portal](https://discord.com/developers/applications):
   - Go to your application → *Bot* → *Privileged Gateway Intents*  
   - Enable **Message Content Intent** if you plan to use prefix commands (e.g. `!kanban`).

5. **Invite the bot to your server** using an OAuth2 link generated in the Developer Portal (Bot → OAuth2 → URL Generator → select `bot` and appropriate permissions).

## File Structure

- **discord_issues_bot.py**  
  Contains the main bot logic, including the `!kanban` command that displays issues in an embed.
- **github_issues.py**  
  Contains a helper function (`get_issues()`) that calls the GitHub API to fetch issues.
- **.env**  
  Holds sensitive tokens and repository details (not tracked in Git).  
- **requirements.txt**  
  Lists all required Python packages.

## Usage

1. **Run the bot**:
   ```bash
   python discord_issues_bot.py
   ```
2. **Check the console** to confirm the bot has successfully connected:  
   ```
   Bot is logged as
   ```
3. **In Discord**, type:
   ```
   !kanban
   ```
   (or whichever command prefix/command name you configured)
4. The bot will respond with an embed listing the relevant GitHub issues (e.g., only open issues).

## Customization

- **Filtering**  
  - By default, the code may use `get_issues("open")` to retrieve only open issues. You can change this to `"all"` or `"closed"` if needed.  
- **Label-based**  
  - If you want to display only issues with a specific label (e.g. `todo`), you can filter by checking `if "todo" in labels: ...` in the bot command logic.
- **Embed Fields**  
  - The bot uses an internal function to split long text into 1024-character chunks, so it doesn’t exceed Discord’s field limit. You can adjust how that splitting logic works if you prefer a different format.

## Troubleshooting

- **Command doesn’t work**:  
  - Make sure the **Message Content Intent** is enabled in the Developer Portal.  
  - Verify you have the correct channel permissions (Send Messages, Embed Links).
- **`Invalid Form Body` or 1024 length error**:  
  - Your list of issues is too long. The included chunk-splitting logic should handle this, but if you see errors, verify the chunk-splitting code is present.
- **No issues displayed**:  
  - Double-check that your GitHub token has `repo` (read) permission and that your repository is spelled correctly in `.env`.  
  - Verify the `state="open"` or any label-based filter actually matches existing issues in your repo.

## Contributing

If you’d like to contribute improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is released under the [MIT License](LICENSE). You’re free to use, modify, and distribute this code, provided the original license is included in any copies or substantial portions of the software.
