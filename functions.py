from math import sqrt, e, log
from scipy.stats import norm
from pandas import read_csv

'''
def black_scholes_call(s_t, k_strike, r, t_expiry, vol):
    # function returns the fair price of a call option under the Black_scholes model given:
    # spot price of an asset = s_t, strike price = k_strike, risk-free rate = r, time to maturity = t_expiry,
    # and volatility = vol
    d1 = (1 / (vol * sqrt(t_expiry))) * (((r + (vol ** 2 / 2)) * t_expiry) + ln(s_t / E))
    d2 = d1 - vol * sqrt(t_expiry)
    call_option_price = norm.cdf(d1) * s_t - norm.cdf(d2) * k_strike * (e**(-r*t_expiry))
    return call_option_price
'''


def black_scholes_put(s_t, k_strike, r, t_expiry, vol):
    # function returns the fair price of a put option under the Black_scholes model given:
    # spot price of an asset = s_t, strike price = k_strike, risk-free rate = r, time to maturity = t_expiry,
    # and volatility = vol
    d1 = (1 / (vol * sqrt(t_expiry))) * (((r + (vol ** 2 / 2)) * t_expiry) + log(s_t / k_strike))
    d2 = d1 - vol * sqrt(t_expiry)
    put_option_price = (k_strike * e**(-r * t_expiry) * norm.cdf(-d2)) - (s_t * norm.cdf(-d1))
    return round(put_option_price, 4)


def csv_df():
    data = read_csv("MATH425_Stock_prices_F22 - MATH425_Stock_prices_F22.csv")
    df = data.values
    return df


def d1(vol, T, t, r, s_t, E):
    d1_value = (1 / (vol * sqrt(T - t))) * (((r + (vol ** 2 / 2)) * (T - t)) + log(s_t / E))
    return d1_value


def hedged_portfolio():
    sell = bool
    buy = bool
    cash_flow = 0
    portfolio_position = {"puts": -20, "shares": 0, "cash": 0}
    portfolio_value = 0
    delta = 0
    wells_fargo_apr = 0.0015
    vol_index = .2621
    df = csv_df()
    prices = []
    for i in range(2, 15):
        price = df[28][i]
        prices.append(float(price))
    print("Weekly NVDA prices:", prices)
    put_option_t0 = black_scholes_put(prices[0], 0.99 * prices[0], wells_fargo_apr, 13 / 52, vol_index)

    # t = 0
    time_T = 13/52
    time_t = 0
    interest_cash = cash_flow * e**(-wells_fargo_apr * (time_T - time_t))
    print("interest cash:", interest_cash)
    cash_flow += interest_cash
    print(" d1:", d1(vol_index, time_T, time_t, wells_fargo_apr, prices[0], 0.99 * prices[0]))
    print("-d1:", -d1(vol_index, time_T, time_t, wells_fargo_apr, prices[0], 0.99 * prices[0]))
    print("norm.cdf(-d1):", norm.cdf(-d1(vol_index, time_T, time_t, wells_fargo_apr, prices[0], 0.99 * prices[0])))
    delta_now = -1 * norm.cdf((-d1(vol_index, time_T, time_t, wells_fargo_apr, prices[0], 0.99 * prices[0])))
    delta_previous = 0
    if delta_now < delta_previous:
        sell = True
        difference = abs(delta_previous - delta_now)
        cash = 100 * difference * prices[0]
        cash_flow += cash
    elif delta_now > delta_previous:
        buy = True
        difference = abs(delta_previous - delta_now)
        cash = 100 * difference * prices[0] * -1
        cash_flow += cash
    print()
    print("delta now:", delta_now)
    print("delta previous:", delta_previous)
    print("cash flow:", cash_flow)
    print()
    portfolio_position["shares"] = delta_now * prices[0]
    portfolio_position["cash"] = cash_flow

    print("For the hedged portfolio we initially have:", portfolio_position)
    print("The initial value of the hedged portfolio is:", portfolio_value)
    return portfolio_position


def unhedged_portfolio():
    wells_fargo_apr = 0.0015
    vol_index = .2621
    df = csv_df()
    put_option_t0 = black_scholes_put(float(df[28][2]), 0.99 * float(df[28][2]), wells_fargo_apr, 13 / 52, vol_index)
    price_week_13 = float(df[28][14])
    portfolio_cash = 100 * put_option_t0
    portfolio_cash_at_expiry = portfolio_cash * e**(wells_fargo_apr * 13/52)
    strike = 0.99 * float(df[28][2])
    portfolio_value = max(0.0, (strike - price_week_13))
    portfolio_0 = {"puts": -100, "cash": round(portfolio_cash, 4)}
    portfolio_expiry = {"puts": -100, "cash": round(portfolio_cash_at_expiry, 4)}
    print("The value of the unhedged portfolio at t = 0 is: ", portfolio_0)
    if portfolio_value == 0.0:
        portfolio_expiry["puts"] = 0
    return portfolio_expiry


def option_1():
    wells_fargo_apr = 0.0015
    vol_index = .2621
    print("\nPatrick chose Nvidia (NVDA) for his project.")
    # data = read_csv("MATH425_Stock_prices_F22 - MATH425_Stock_prices_F22.csv")
    df = csv_df()
    # print(df)
    # print("df type", type(df))
    print()
    print("The recorded stock price data for NVDA is:\n", df[28])
    print("The first recorded price for Nvidia is:", df[28][2])
    print()
    print("The Wells Fargo annual interest rate is 0.15% or {}".format(wells_fargo_apr))
    print("The volatility index, as obtained from MarketWatch, on August 30, 2022 was:", vol_index)

    # using black scholes put function to calculate the fair price of an option at t = 0
    print()
    print("The price of one NVDA put option at "
          " \n- time: t = 0"
          " \n- with interest rate: r = {}"
          " \n- with VIX: vol = {}"
          " \n- strike price: E = {}"
          " \n- initial price: s_0 = {}"
          " \n- expiry: T = {} weeks".format(wells_fargo_apr, vol_index, round(0.99 * float(df[28][2]), 4),
                                             float(df[28][2]), 13))
    put_option_t0 = black_scholes_put(float(df[28][2]), 0.99 * float(df[28][2]), wells_fargo_apr, 13 / 52, vol_index)
    print("is\n$", put_option_t0)

    print()
    print("The value of the unhedged portfolio at expiry is: ", unhedged_portfolio())
    print()
    print("The value of the hedged portfolio at t = 0 is: ", hedged_portfolio())


def option_2():
    print("option 2 executes")
