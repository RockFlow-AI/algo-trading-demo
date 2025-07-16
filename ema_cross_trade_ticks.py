import datetime
import os
import time
from decimal import Decimal

import pandas as pd
from nautilus_trader.backtest.engine import BacktestEngineConfig, BacktestEngine
from nautilus_trader.common.config import LoggingConfig
from nautilus_trader.core.datetime import dt_to_unix_nanos
from nautilus_trader.data.engine import ParquetDataCatalog
from nautilus_trader.examples.strategies.ema_cross import EMACrossConfig, EMACross
from nautilus_trader.execution.algorithm import ExecAlgorithm
from nautilus_trader.model import TraderId, Venue, Money
from nautilus_trader.model.currencies import USD
from nautilus_trader.model.data import BarType, BarAggregation, BarSpecification
from nautilus_trader.model.enums import OmsType, BookType, AccountType, PriceType, AggregationSource

from algo._polygon.data_client import PolygonEquityData
from algo.settings import POLYGON_API_KEY

if __name__ == "__main__":
    CATALOG_PATH = os.getcwd() + "/catalog"
    # Prepare to download historical data of stocks in ticker list
    poly = PolygonEquityData(POLYGON_API_KEY, ["TSLA"], CATALOG_PATH)
    poly.get_tickers()
    # Specify datetime range and timeframe of historical data to download
    poly.get_bar_data_for_tickers(
        datetime.date(2021, 1, 4),
        datetime.date(2024, 12, 31),
        1,
        BarAggregation.DAY,
    )

    # Load existing catalog (only if not already created above)
    catalog = ParquetDataCatalog(CATALOG_PATH)

    instrument = catalog.instruments(as_nautilus=True)[0]

    config = BacktestEngineConfig(
        trader_id=TraderId("BACKTESTER-001"),
        logging=LoggingConfig(
            log_level="INFO",
            log_colors=True,
            use_pyo3=False,
        ),
    )

    # Build the backtest engine
    engine = BacktestEngine(config=config)

    # Add a trading venue (multiple venues possible)
    XNAS = Venue("XNAS")
    engine.add_venue(
        venue=XNAS,
        oms_type=OmsType.NETTING,
        book_type=BookType.L1_MBP,
        account_type=AccountType.MARGIN,
        base_currency=USD,
        starting_balances=[Money(1_000_000.0, USD)],
        trade_execution=True,  # Only use with L1_MBP book type or throttled book data
    )

    bar_type = BarType(
        instrument.id,
        BarSpecification(1, BarAggregation.DAY, PriceType.LAST),
        AggregationSource.EXTERNAL,
    )
    # Add instrument and historical bars to backtest engine
    engine.add_instrument(instrument)
    engine.add_data(catalog.bars(bar_types=[str(bar_type)]))

    # Special configuration for EMA cross strategy
    config = EMACrossConfig(
        instrument_id=instrument.id,
        bar_type=bar_type,
        trade_size=Decimal("10"),
        fast_ema_period=10,
        slow_ema_period=20,
    )

    strategy = EMACross(config=config)
    engine.add_strategy(strategy=strategy)

    # Instantiate and add your execution algorithm
    exec_algorithm = ExecAlgorithm()
    engine.add_exec_algorithm(exec_algorithm)

    time.sleep(0.1)
    input("Press Enter to continue...")

    # Run the engine (from start to end of data)
    engine.run()

    # Optionally view reports
    with pd.option_context(
            "display.max_rows",
            100,
            "display.max_columns",
            None,
            "display.width",
            300,
    ):
        print(engine.trader.generate_account_report(XNAS))
        print(engine.trader.generate_order_fills_report())
        print(engine.trader.generate_positions_report())

    # For repeated backtest runs make sure to reset the engine
    engine.reset()

    # Good practice to dispose of the object
    engine.dispose()
