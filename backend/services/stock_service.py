from sqlalchemy.orm import Session
from backend.models.stock import Stock
from ml.data_loader import fetch_stock_data
import logging

logger = logging.getLogger(__name__)


# ---------------- CREATE STOCK ---------------- #
def create_stock(db: Session, data):
    stock_data = data.dict()

    # 🔹 Normalize
    stock_data["symbol"] = stock_data["symbol"].upper().strip()
    stock_data["risk_tolerance"] = stock_data["risk_tolerance"].lower().strip()

    # 🔹 Validate risk
    if stock_data["risk_tolerance"] not in ["low", "medium", "high"]:
        raise ValueError("risk_tolerance must be low, medium, or high")

    # 🔹 Prevent duplicate
    existing = db.query(Stock).filter(Stock.symbol == stock_data["symbol"]).first()
    if existing:
        logger.warning(f"Stock already exists: {stock_data['symbol']}")
        return existing

    stock = Stock(**stock_data)

    db.add(stock)
    db.commit()
    db.refresh(stock)

    logger.info(f"Stock created: {stock.symbol}")

    return stock


# ---------------- GET ALL STOCKS ---------------- #
def get_all_stocks(db: Session):
    return db.query(Stock).all()


# ---------------- GET BY SYMBOL ---------------- #
def get_stock_by_symbol(db: Session, symbol: str):
    if not symbol:
        return None

    return db.query(Stock).filter(
        Stock.symbol == symbol.upper().strip()
    ).first()


# ---------------- GET BY RISK ---------------- #
def get_stocks_by_risk(db: Session, risk_level: str):
    if not risk_level:
        return []

    risk_level = risk_level.lower().strip()

    return db.query(Stock).filter(
        Stock.risk_tolerance.ilike(risk_level)
    ).all()


# ---------------- DIVERSIFIED STOCKS ---------------- #
def get_diversified_stocks(db: Session, risk_level: str, limit: int = 10):

    stocks = get_stocks_by_risk(db, risk_level)

    if not stocks:
        logger.warning(f"No stocks found for risk: {risk_level}")
        return []

    sectors_seen = {}
    diversified = []

    # 🔹 Dynamic diversification
    if risk_level == "low":
        max_per_sector = 2
    elif risk_level == "high":
        max_per_sector = 4
    else:
        max_per_sector = 3

    for stock in stocks:
        sector = stock.sector or "Unknown"

        if sector not in sectors_seen:
            sectors_seen[sector] = 0

        if sectors_seen[sector] < max_per_sector:
            diversified.append(stock)
            sectors_seen[sector] += 1

        if len(diversified) >= limit:
            break

    return diversified


# ---------------- AUTO FETCH (CORE LOGIC) ---------------- #
def auto_fetch_stock_if_missing(db: Session, symbol: str):
    """
    Ensures stock exists in DB.
    If missing → fetch from Yahoo Finance → store → return.
    """

    if not symbol:
        return None, False

    symbol = symbol.upper().strip()

    # 🔹 Step 1: Check DB
    stock = get_stock_by_symbol(db, symbol)
    if stock:
        logger.info(f"{symbol} found in DB")
        return stock, False

    logger.warning(f"{symbol} not found in DB. Fetching from Yahoo...")

    try:
        # 🔹 Step 2: Fetch real stock data
        df = fetch_stock_data(symbol)

        if df is None or df.empty:
            logger.error(f"Yahoo fetch failed for {symbol}")
            return None, False

        # 🔹 Step 3: Create stock entry
        stock = Stock(
            symbol=symbol,
            sector="Unknown",
            industry="Unknown",
            market_cap=0.0,
            style="Unknown",
            risk_tolerance="medium"
        )

        db.add(stock)
        db.commit()
        db.refresh(stock)

        logger.info(f"{symbol} added to DB via Yahoo fetch")

        return stock, True

    except Exception as e:
        logger.exception(f"Auto-fetch failed for {symbol}: {e}")
        return None, False