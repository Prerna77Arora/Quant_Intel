from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.schemas.stock import StockCreate
from backend.services.stock_service import (
    create_stock,
    get_all_stocks,
    get_stock_by_symbol,
    auto_fetch_stock_if_missing
)
from backend.utils.dependencies import get_db, get_current_user
from backend.models.stock import Stock


# ✅ FIX: Removed prefix from here
router = APIRouter(tags=["Stocks"])


# ---------------------- ADD STOCK ---------------------- #
@router.post("/", status_code=status.HTTP_201_CREATED)
def add_stock(
    data: StockCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        stock = create_stock(db, data)

        return {
            "success": True,
            "data": {
                "id": stock.id,
                "symbol": stock.symbol,
                "sector": stock.sector,
                "industry": stock.industry,
                "market_cap": stock.market_cap,
                "style": stock.style,
                "risk_level": stock.risk_level
            },
            "message": "Stock added successfully"
        }

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to add stock"
        )


# ---------------------- GET ALL STOCKS ---------------------- #
@router.get("/", status_code=status.HTTP_200_OK)
def list_stocks(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        stocks = get_all_stocks(db)

        return {
            "success": True,
            "data": [
                {
                    "id": s.id,
                    "symbol": s.symbol,
                    "sector": s.sector,
                    "industry": s.industry,
                    "market_cap": s.market_cap,
                    "style": s.style,
                    "risk_level": s.risk_level
                }
                for s in stocks
            ],
            "message": "Stocks fetched successfully"
        }

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch stocks"
        )


# ---------------------- SEARCH STOCK ---------------------- #
@router.get("/search/{symbol}", status_code=status.HTTP_200_OK)
def search_stock(
    symbol: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        stock = get_stock_by_symbol(db, symbol.upper())

        if stock:
            return {
                "success": True,
                "found": True,
                "auto_fetched": False,
                "data": {
                    "id": stock.id,
                    "symbol": stock.symbol,
                    "sector": stock.sector,
                    "industry": stock.industry,
                    "market_cap": stock.market_cap,
                    "style": stock.style,
                    "risk_level": stock.risk_level
                }
            }

        stock, fetched = auto_fetch_stock_if_missing(db, symbol.upper())

        if stock:
            return {
                "success": True,
                "found": True,
                "auto_fetched": True,
                "data": {
                    "id": stock.id,
                    "symbol": stock.symbol,
                    "sector": stock.sector,
                    "industry": stock.industry,
                    "market_cap": stock.market_cap,
                    "style": stock.style,
                    "risk_level": stock.risk_level
                },
                "message": f"{symbol.upper()} auto-fetched"
            }

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{symbol.upper()} not found"
        )

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Stock search failed"
        )


# ---------------------- GET STOCK BY ID ---------------------- #
@router.get("/{stock_id}", status_code=status.HTTP_200_OK)
def get_stock(
    stock_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        stock = db.query(Stock).filter(Stock.id == stock_id).first()

        if not stock:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Stock not found"
            )

        return {
            "success": True,
            "data": {
                "id": stock.id,
                "symbol": stock.symbol,
                "sector": stock.sector,
                "industry": stock.industry,
                "market_cap": stock.market_cap,
                "style": stock.style,
                "risk_level": stock.risk_level
            }
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch stock"
        )