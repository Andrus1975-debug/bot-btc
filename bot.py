import requests, time, numpy as np
from sklearn.ensemble import RandomForestClassifier

TOKEN="8670568704:AAFOA3bEjfIUl_Uo8DVFoZ8f1oY6s39GKzM"
CHAT_ID="698685063"

def tg(m):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",data={"chat_id":CHAT_ID,"text":m,"parse_mode":"Markdown"},timeout=15)
    except: pass

def get_data():
    r=requests.get("https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=5m&limit=500",timeout=10).json()
    return np.array([float(x[4]) for x in r])

def predecir(c):
    d=np.diff(c); g=np.where(d>0,d,0); l=np.where(d<0,-d,0)
    rsi=[]
    for i in range(14,len(c)):
        ag=np.mean(g[i-14:i]); al=np.mean(l[i-14:i])
        rsi.append(100-(100/(1+ag/(al+1e-9))))
    rsi=np.array(rsi)
    X=[]; y=[]
    for i in range(20,len(c)-1):
        idx=i-(len(c)-len(rsi))
        if idx<0 or idx>=len(rsi): continue
        X.append([rsi[idx], c[i]/c[i-1]-1, (c[i]-c[i-5])/c[i]])
        y.append(1 if c[i+1]>c[i] else 0)
    m=RandomForestClassifier(n_estimators=50,max_depth=5)
    m.fit(np.array(X),np.array(y))
    prob=m.predict_proba([[rsi[-1], c[-1]/c[-2]-1, (c[-1]-c[-5])/c[-1]]])[0][1]*100
    return prob, rsi[-1], c[-1]

tg("✅ BOT V5 IA REAL - bot-btc INICIADO")
while True:
    try:
        c=get_data()
        prob,rsi_v,price=predecir(c)
        pred="LONG" if prob>60 else "SHORT" if prob<40 else "NEUTRAL"
        if pred!="NEUTRAL":
            tg(f"🤖 *{pred} IA* {prob:.1f}%\nPrecio: ${price:.2f}\nRSI: {rsi_v:.1f}")
        time.sleep(300)
    except Exception as e:
        print(e); time.sleep(30)
