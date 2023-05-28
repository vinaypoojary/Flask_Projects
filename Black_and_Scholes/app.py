from flask import Flask, render_template, redirect, request
import numpy as np
from scipy.stats import norm

N = norm.cdf

app = Flask(__name__)

@app.route('/', methods=['GET',"POST"])
def home():
    if request.method == "POST":
        S = request.form.get('num1')
        K = request.form.get('num2')
        T = request.form.get('num3')
        r = request.form.get('num5')
        q = request.form.get('num6')
        sigma = request.form.get('num4')
        callput = request.form.get('num7')

        if callput == "Call":
            bs_price = black_scholes_call(float(S),float(K),float(T),float(r),float(q),float(sigma))
        else:
            bs_price = black_scholes_put(float(S),float(K),float(T),float(r),float(q),float(sigma))

        #bs_price = black_scholes_call(float(S),float(K),float(T),float(r),float(q),float(sigma))
        return render_template('index.html', Calculate=bs_price)
    return render_template('index.html')


def black_scholes_call(S,K,T,r,q,sigma):
    """
    Inputs
    #S = Current stock Price
    #K = Strike Price
    #T = Time to maturity 1 year = 1, 1 months = 1/12
    #r = risk free interest rate
    #q = dividend yield
    # sigma = volatility 
    
    Output
    # call_price = value of the option 
    """
    d1 = (np.log(S/K) + (r - q + sigma**2/2)*T) / sigma*np.sqrt(T)
    d2 = d1 - sigma* np.sqrt(T)
    
    #call = S * N(d1) - K * np.exp(-r*T)* N(d2)
    call = S * np.exp(-q*T)* norm.cdf(d1) - K * np.exp(-r*T)*norm.cdf(d2)
    return call


def black_scholes_put(S,K,T,r,q,sigma):
    """
    Inputs
    #S = Current stock Price
    #K = Strike Price
    #T = Time to maturity 1 year = 1, 1 months = 1/12
    #r = risk free interest rate
    #q = dividend yield
    # sigma = volatility 
    
    Output
    # call_price = value of the option 
    """
    d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma* np.sqrt(T)
    
    put = K*np.exp(-r*T)*N(-d2) - S*N(-d1)
    return put


if __name__ == "__main__":
    app.run(debug=True)


#https://goodcalculators.com/black-scholes-calculator/