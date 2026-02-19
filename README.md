# Trading Bot (Binance Futures Testnet)

**[Live Demo](https://demo-trader.onrender.com)**

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

## Tutorial: Your First Trade

This 5-minute guide will help you place your first order on the Binance Futures Testnet.

### Step 1: Get Testnet Credentials
1.  Go to [testnet.binancefuture.com](https://testnet.binancefuture.com/en/futures/BTCUSDT).
2.  Log in or Register.
3.  Scroll down to find your **API Key** and **Secret Key**. (Do not share these!).

### Step 2: Launch the Dashboard
Start the local server:
```bash
python server.py
```
Open your browser and navigate to: [http://localhost:8000](http://localhost:8000)

### Step 3: Configure the Bot
1.  In the top-right corner or the "API Configuration" modal, enter the **API Key** and **Secret Key** you got in Step 1.
2.  Click **Save Credentials**.

### Step 4: Place an Order
1.  **Select Side**: Choose **Buy / Long** (Green).
2.  **Symbol**: Default is `BTCUSDT`.
3.  **Order Type**: Keep it as `MARKET` for immediate execution.
4.  **Size**: Enter `0.002` (This is ~100-150 USDT value).
5.  Click the big green **Buy / Long** button.

### Step 5: Verify
-   Look at the **Order History** table below the chart. You should see a new row with Status `FILLED`.
-   You can also check your [Binance Testnet Account](https://testnet.binancefuture.com/en/futures/BTCUSDT) to see the open position.

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

## Advanced Usage (CLI)

If you prefer the command line:

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
