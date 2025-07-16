# 量化回测平台

## 安装回测平台
### Mac
- 创建python虚拟环境
    ```
    xcode-select --install
    sudo xcode-select -s /Applications/Xcode.app/Contents/Developer
    export SDKROOT=$(xcrun --show-sdk-path)
    pyenv install 3.13.3
    pyenv virtualenv 3.13.3 algo-trading-demo
    pyenv activate algo-trading-demo
    ```

- 安装 requirements.txt 中的组件：`pip install -r requirements.txt`
- 安装回测工具[NautilusTrader](https://github.com/nautechsystems/nautilus_trader)
    ```
    export SDKROOT=$(xcrun --show-sdk-path)
    brew install cython rust
    pip install git+https://github.com/nautechsystems/nautilus_trader.git@v1.216.0
    ```
### Windows
- 安装[python 3.13.2](https://www.python.org/downloads/release/python-3132/)，并选择添加到PATH
- 运行`python --version`确定版本正确
- 升级pip: `python -m pip install --upgrade pip`
- 安装 requirements.txt 中的组件：`pip install -r requirements.txt`
- 安装回测工具[NautilusTrader](https://github.com/nautechsystems/nautilus_trader)：`pip install nautilus_trader==1.216.0`

## 运行模拟回测
- 在项目根目录创建文件`.env`，并添加`POLYGON_API_KEY=<Your polygon API key>`
- 运行 `ema_cross_trade_ticks.py`，验证安装是否成功 

# 参考
- [NautilusTrader文档](http://nautilustrader.io/docs/latest/)
