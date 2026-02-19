# Trading Bot (Binance Futures Testnet)

A Python application to place Market and Limit orders on the Binance Futures Testnet.

## Prerequisites

- [Python 3.8+](https://www.python.org/)
- A Binance Futures Testnet Account ([Register here](https://testnet.binancefuture.com/en/login)) to get API Key and Secret.

## Setup

1. **Clone or Download** this repository.
2. **Create a Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure API Keys**:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and paste your Testnet API Key and Secret.

## Testing

To run the automated tests for validators, client, and order logic:

1.  **Install Test Dependencies**:
    ```bash
    pip install pytest
    ```

2.  **Run Tests**:
    ```bash
    pytest tests/
    ```

## Usage

### CLI Mode

Run the CLI tool using Python:

```bash
python cli.py
```

The CLI will prompt you for the necessary details.

#### Examples using request arguments:

**Market Buy Order:**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**Limit Sell Order:**
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 95000
```

### Web Dashboard (UI)

1.  **Run the Server**:
    ```bash
    python server.py
    ```
2.  **Access Dashboard**:
    Open [http://localhost:8000](http://localhost:8000) in your browser.
3.  **Configure**:
    Enter your API Key and Secret in the "API Settings" box.

## Deployment

### Option 1: Render (Free Tier)

**Note:** This method uses a temporary filesystem. Your database (history/settings) will be reset if the app restarts. For persistence, upgrade to a paid plan with a disk or use an external database.

1.  **Push to GitHub**: ensure your repository is public or private on GitHub.
2.  **Sign up**: Create an account on [Render.com](https://render.com).
3.  **New Web Service**:
    -   Click "New +" -> "Web Service".
    -   Connect your GitHub repository.
    -   Runtime: **Python 3**.
    -   Build Command: `pip install -r requirements.txt`
    -   Start Command: `uvicorn server:app --host 0.0.0.0 --port $PORT`
4.  **Environment Variables**:
    -   Add `PYTHON_VERSION` = `3.9.0` (optional).
5.  **Deploy**: Click "Create Web Service".

Your app will be live at `https://your-app-name.onrender.com`.

### Option 2: Docker (Local / VPS)

1.  **Start Services**:
    ```bash
    docker-compose up -d --build
    ```
2.  **Access the UI**:
    Open [http://localhost:8000](http://localhost:8000)
3.  **Data Persistence**:
    Database and logs are stored in the `./data` directory.
4.  **Stopping**:
    ```bash
    docker-compose down
    ```


## Logs

Execution logs are saved to `trading_bot.log` in the current directory.

## File Structure

- `bot/`: Contains core logic (client, orders, validators).
- `cli.py`: Entry point for the Command Line Interface.
- `requirements.txt`: Python dependencies.
