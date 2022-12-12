from math import sqrt, e, log
from scipy.stats import norm
import pandas as pd

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


def get_dataframe():
    data = pd.read_csv("MATH425_Stock_prices_F22 - MATH425_Stock_prices_F22.csv")
    df = pd.DataFrame(data, columns=[str("Stock"), str("initials"), "w2", "w3", "w4", "w5", "w6", "w7", "w8", "w9",
                                     "w10", "w11", "w12", "w13", "w14"])
    # print(df)
    return df


def black_scholes_put(vol, T, t, r, s_t, E):
    # function returns the fair price of a put option under the Black_scholes model given:
    # spot price of an asset = s_t, strike price = k_strike, risk-free rate = r, time to maturity = t_expiry,
    # and volatility = vol
    d1_value = (1 / (vol * sqrt(T - t))) * (((r + (vol ** 2 / 2)) * (T - t)) + log(s_t / E))
    d2_value = d1_value - vol * sqrt(T - t)
    put_option_price = (E * e ** (-r * (T - t)) * norm.cdf(-d2_value)) - (s_t * norm.cdf(-d1_value))
    return round(put_option_price, 4)


def csv_df():
    data = pd.read_csv("MATH425_Stock_prices_F22 - MATH425_Stock_prices_F22.csv")
    df = data.values
    return df


def d1(vol, T, t, r, s_t, E):
    d1_function = (1 / (vol * sqrt(T - t))) * (((r + (vol ** 2 / 2)) * (T - t)) + log(s_t / E))
    return d1_function


def hedged_portfolio():
    sell = bool
    buy = bool
    cash_flow = 0
    portfolio_position = {"puts": -100, "shares": 0, "cash": 0}
    portfolio_value = 0
    wells_fargo_apr = 0.0015
    vol_index = .2621
    df = csv_df()

    prices = [float(df[28][i]) for i in range(2, 15)]
    print("Weekly NVDA prices:", prices)
    put_option_t0 = round(black_scholes_put(vol_index, 13 / 52, 0, wells_fargo_apr, float(df[28][2]),
                                            0.99 * float(df[28][2])), 4)
    # print("put option price =", put_option_t0)
    put_option_hundred_value = 100 * put_option_t0

    time_t = 0
    time_T = 13 / 52
    delta_previous = 0
    print()
    for i in prices:
        print("------------")
        print("t =", round(time_t, 4))
        print("------------")
        print()
        interest_cash = cash_flow * e ** (wells_fargo_apr * (time_T - time_t))
        print("cash with earned interest =", round(interest_cash, 4))
        cash_flow = interest_cash
        cash_flow += put_option_hundred_value

        # print(" d1:", d1(vol_index, time_T, time_t, wells_fargo_apr, i, 0.99 * i))
        print("-d1 =", -d1(vol_index, time_T, time_t, wells_fargo_apr, i, 0.99 * i))
        print("norm.cdf(-d1) =", norm.cdf(-d1(vol_index, time_T, time_t, wells_fargo_apr, i, 0.99 * i)))
        delta_now = -1 * norm.cdf((-d1(vol_index, time_T, time_t, wells_fargo_apr, i, 0.99 * i))
                                  )
        print()
        print("delta now =", delta_now)
        print("delta previous =", delta_previous)
        # print("cash flow:", cash_flow)
        print()
        if delta_now < delta_previous:
            sell = True
            print("For time t =", round(time_t, 4), "we are selling", round(100 * abs(delta_now - delta_previous), 4),
                  "shares at price", i)
            difference = abs(delta_previous - delta_now)
            cash = round(100 * difference * i, 4)
            cash_flow += cash
            print("We receive", cash, "dollars")
            print("Net cash-flow is", cash_flow, "dollars")

        elif delta_now > delta_previous:
            buy = True
            print("For time t =", round(time_t, 4), "we are buying", round(100 * abs(delta_now - delta_previous), 4),
                  "shares at price", i)
            difference = abs(delta_previous - delta_now)
            cash = round(100 * difference * i, 4)
            cash_flow -= cash
            print("We lose", cash, "dollars")
            print("Net cash-flow is", cash_flow, "dollars")

        portfolio_position["shares"] = round(100 * delta_now, 4)
        portfolio_position["cash"] = round(cash_flow, 4)

        delta_previous = delta_now
        time_t += 1 / 52
        put_option_hundred_value = 0
        print()
        print("For the hedged portfolio we have:", portfolio_position)
        print()

    return portfolio_position


def unhedged_portfolio():
    wells_fargo_apr = 0.0015
    vol_index = .2621
    df = csv_df()
    put_option_t0 = black_scholes_put(vol_index, 13 / 52, 0, wells_fargo_apr, float(df[28][2]),
                                      0.99 * float(df[28][2]))
    price_week_13 = float(df[28][14])
    portfolio_cash = 100 * put_option_t0
    portfolio_cash_at_expiry = portfolio_cash * e ** (wells_fargo_apr * 13 / 52)
    strike = 0.99 * float(df[28][2])
    portfolio_value = max(0.0, (strike - price_week_13))
    portfolio_0 = {"puts": -100, "cash": round(portfolio_cash, 4)}
    portfolio_expiry = {"puts": -100, "cash": round(portfolio_cash_at_expiry, 4)}
    print("The value of the unhedged portfolio at t = 0 is: ", portfolio_0)
    if portfolio_value == 0.0:
        portfolio_expiry["puts"] = 0
    return portfolio_expiry


def historical_volatility():
    delta_t = float(1 / 52)
    M = 13
    wells_fargo_apr = 0.0015
    vol_index = .2621
    df = csv_df()
    prices = [float(df[28][i]) for i in range(2, 15)]
    prices.reverse()
    sum_volatility = 0
    for i in range(M - 1):
        sum_volatility += log(prices[i] / prices[i + 1]) ** 2

    historical_volatility_value = \
        (1 / sqrt(delta_t)) * sqrt(((1 / (M - 1)) * sum_volatility) -
                                   ((1 / (M * (M - 1))) * sum_volatility))
    return historical_volatility_value


def option_1():
    wells_fargo_apr = 0.0015
    vol_index = .2621
    print("\nPatrick chose Nvidia (NVDA) for his project.")
    # data = read_csv("MATH425_Stock_prices_F22 - MATH425_Stock_prices_F22.csv")
    df = csv_df()
    # print(df)
    # print("df type", type(df))
    # print()
    # print("The recorded stock price data for NVDA is:\n", df[28])
    print("The first recorded price for Nvidia is:", df[28][2])
    print()
    print("The Wells Fargo annual interest rate is 0.15% or {}".format(wells_fargo_apr))
    print("The volatility index, as obtained from MarketWatch, on August 30, 2022 was:", vol_index)

    # using black scholes put function to calculate the fair price of an option at t = 0
    print()
    print("-------------------------------------------------------------------------------")
    print("PART 1")
    print("The price of one NVDA put option at "
          " \n- time: t = 0"
          " \n- with interest rate: r = {}"
          " \n- with VIX: vol = {}"
          " \n- strike price: E = {}"
          " \n- initial price: s_0 = {}"
          " \n- expiry: T = {} weeks".format(wells_fargo_apr, vol_index, round(0.99 * float(df[28][2]), 4),
                                             float(df[28][2]), 13))
    put_option_t0 = black_scholes_put(vol_index, 13 / 52, 0, wells_fargo_apr, float(df[28][2]),
                                      0.99 * float(df[28][2]))
    print("is\n$", put_option_t0)

    print()
    x = hedged_portfolio()

    print()
    print("-------------------------------------------------------------------------------")
    print("PART 2")
    print("The final portfolio position at t = 12/52 is {'puts': -100, 'shares': -38.3814, 'cash': 6688.0421}")
    print("At expiry, s_t =", df[28][14], "and the strike price of the option was", round(0.99 * float(df[28][2]), 4),
          "so the put options are not exercised.")
    print("We bring the options contract forward by selling the shares and accounting for the put options not"
          " exercised")
    print("We buy back", -x["shares"], "shares at", df[28][14], "dollars for a total of", x["shares"] * df[28][14])
    print("Our new total cash is", round(x["cash"] + x["shares"] * df[28][14], 4))
    final_cash = round(x["cash"] + x["shares"] * df[28][14], 4)
    print("The final value of the hedged portfolio is {}".format("'puts': 0, 'shares': 0, 'cash':") +
          str(final_cash))

    print()
    print("-------------------------------------------------------------------------------")
    print("PART 3 ")
    print("The value of the unhedged portfolio at expiry is: ", unhedged_portfolio())
    print()
    print("-------------------------------------------------------------------------------")
    print("PART 4")
    print("Ultimately the unhedged portfolio proved to be a better investment with a final value of $726.5224 compared"
          " to the hedged portfolio's final value of $466.4172. Since the underlying asset went up in "
          "price and the options were not executed, hedging was not needed though there's no way we could have"
          " known that at t = 0 which is why hedging is a beneficial risk mitigation practice. Had the options been "
          "exercised, we would have been much more prepared for the downside of the investment and our losses would "
          "have been limited")
    print()
    print("-------------------------------------------------------------------------------")
    print("PART 5")
    print("Historical volatility =", round(historical_volatility(), 4))
    print("The historical volatility was determined to be", round(historical_volatility(), 4), ". This value was larger"
            " than the VIX volatility of", vol_index, "by almost 2x. When I ran the program with this volatility my "
            "final portfolio valuation was 'puts': 0, 'shares': 0, 'cash': 1129.1184 .Using this historical volatility"
            " would ultimately prove to be better but we wouldn't have had it at t = 0 anyways so its more of a "
            "hindsight 20/20")


def option_2():
    # print("Option 2 is still under development! Check the github repository for an up-to-date program with this
    # feature enabled!")
    # print("https://github.com/patrickhny/MATH425_final_project.git")
    df = get_dataframe()
    columns = df["Stock"]
    # print(columns)
    # print("columns size:", len(columns))
    stock_names = [columns[i] for i in range(0, (len(columns)))]
    print("choose from the following stocks: ")
    print("stock names:", sorted(stock_names))
    stock_name_user = input("Enter stock name: ")
    print()

    while stock_name_user.upper() not in stock_names:
        print("That stock is not in our spreadsheet. Try another!")
        print("stock names:", sorted(stock_names))
        stock_name_user = input("Enter stock name: ")
        print()
        continue

    # interest_bool = False
    # volatility_bool = False
    input_bool = True
    while input_bool:
        try:
            annual_interest_rate_user = float(input("Enter annual interest rate as a percent: "))
            # print("You entered {}%. Is this correct?".format(annual_interest_rate_user))
            '''
            correctness_interest = input("Type (yes/no), (Y/N), (y/n): ")
            correctness_interest.lower()
            if correctness_interest == "no" or "n":
                interest_bool = False
            else:
                continue
            '''

            volatility_user = float(input("Enter volatility: "))
            '''
            print("You entered {} for volatility. Is this correct?".format(volatility_user))
            correctness_volatility = input("Type (yes/no), (Y/N), (y/n): ")
            correctness_volatility.lower()
            if correctness_volatility == "yes" or "y":
                volatility_bool = True
            else:
                continue
            '''
            input_bool = False

        except ValueError:
            print("Input was non numerical. Try Again")
            print()
            continue


def all_purpose_calc(r, vol, stock):
    return 0
