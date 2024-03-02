from fastapi import FastAPI, Request, Form
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import yfinance as yf
import mplfinance as mpf
import pandas as pd
import io
import base64

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit")
async def handle_form(request: Request, ticker: str = Form(...), start: str = Form(...), end: str = Form(...) ):
    data = yf.download(ticker, start=start, end=end)
    buffer = io.BytesIO()
    # mpf.plot(data, type='candle', mav=(3,6,9), volume=True, savefig=buffer)
    mpf.plot(
        data, # 使用するデータフレームを第一引数に指定
        type='candle', # グラフ表示の種類を指定 ローソク足チャートであれば"candle"
        style='yahoo', # ここにスタイル一覧の中から好みのものを指定 例では"yahoo"を指定

        # チャートのサイズの設定
        figratio=(20, 10), # 図のサイズをタプルで指定
        figscale=1.0, # 図の大きさの倍率を指定、デフォルトは1
        tight_layout=False, # 図の端の余白を狭くして最適化するかどうかを指定

        # 軸の設定
        datetime_format='%Y/%m/%d', # X軸の日付の表示書式を指定
        # xlim=('2021-01-01', '2021-02-01'), # X軸の日付の範囲をタプルで指定 指定無しならデータフレームを元に自動で設定される
        # ylim=(25000, 30000), # Y軸の範囲をタプルで指定 指定無しなら自動で設定される
        xrotation=45, # X軸の日付ラベルの回転角度を指定 デフォルトは45度
        axisoff=False, # 軸を表示するかどうかを指定 デフォルトは"False"

        # データの表示設定
        volume=True, # ボリュームを表示するかどうかを指定 デフォルトは"False"
        show_nontrading=False, # データがない日付を表示するかどうかを指定 デフォルトは"False"

        # ラベルの設定
        title=f'{ticker}', # チャートのタイトル
        ylabel='ylabel', # チャートのY軸ラベル
        ylabel_lower='ylabel_lower', # ボリュームを表示する場合は、ボリュームのグラフのY軸ラベル
        savefig=buffer
    )
    buffer.seek(0)
    encoded_image = base64.b64encode(buffer.read()).decode("utf-8")
    return templates.TemplateResponse("result.html", {"request": request, "encoded_image": encoded_image})