# 量化回测平台

## 安装回测平台
- 创建python虚拟环境
    ```
    xcode-select --install
    sudo xcode-select -s /Applications/Xcode.app/Contents/Developer
    export SDKROOT=$(xcrun --show-sdk-path)
    pyenv install 3.13.3
    pyenv virtualenv 3.13.3 algo-trading-demo
    pyenv activate algo-trading-demo
    ```

- 安装回测工具[NautilusTrader](https://github.com/nautechsystems/nautilus_trader)
    ```
    export SDKROOT=$(xcrun --show-sdk-path)
    brew install cython rust
    pip install git+https://github.com/nautechsystems/nautilus_trader.git@v1.216.0
    ```
- 安装 requirements.txt 中的组件：`pip install -r requirements.txt`
- 运行 `ema_cross_trade_ticks.py`，验证安装是否成功 
