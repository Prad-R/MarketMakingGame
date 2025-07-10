
import time
import random
import threading
import os
import matplotlib.pyplot as plt
import numpy as np

def failure():
    print(" Timer is over, too slow !")
    os._exit(0)

def compute_EV(info, distribution, nb_range):
    sumValue = 0
    for element in info:
        if np.isnan(element):
            if distribution == "uniform":
                sumValue += nb_range / 2
            elif distribution == "normal":
                sumValue += nb_range / 2
            elif distribution == "skewed":
                sumValue += nb_range * 0.3
        else:
            sumValue += element
    return round(sumValue / len(info), 1)

def compute_EV_extreme(info, nb_range, extreme):
    sumValue = 0
    for element in info:
        if np.isnan(element):
            sumValue += nb_range if extreme == "max" else 0
        else:
            sumValue += element
    return round(sumValue / len(info), 1)

def test_price(value):
    try:
        value = float(value)
        if value < 0:
            raise ValueError("Price cannot be negative")
    except:
        raise ValueError("Price needs to be a float")
    return round(value, 1)

def draw_card(distribution, nb_range):
    if distribution == "uniform":
        return random.randint(0, nb_range)
    elif distribution == "normal":
        val = int(np.clip(np.random.normal(loc=nb_range / 2, scale=nb_range / 5), 0, nb_range))
        return val
    elif distribution == "skewed":
        val = int(np.clip(np.random.beta(2, 5) * nb_range, 0, nb_range))
        return val

def main():
    print("Welcome to the Market Making Game (Random Distribution Mode)")
    print("Prices rounded to 1 decimal")
    print("=====SETUP========")

    nb_step = int(input("Select number of steps: "))
    nb_range = int(input("Select the range of the price: "))
    timer_s = int(input("Select calculation time per round (seconds): "))

    distribution = random.choice(["uniform", "normal", "skewed"])
    print(f"🔍 Distribution for this game (unknown to player during run): {distribution}")
    print("PRESS ENTER WHEN READY")
    input()
    print(f"Game starts in 3 seconds. You have {timer_s}s per round.")
    for c in ["3", "2", "1"]:
        print(c)
        time.sleep(1)

    informations = [np.nan] * nb_step

    Delta = []
    Spreads = []
    Bids = []
    Asks = []
    Times = []
    Mids = []
    Highers = []
    Lowers = []

    for i in range(nb_step):
        t = threading.Timer(timer_s, lambda: failure())
        Highers.append(compute_EV_extreme(informations, nb_range, "max"))
        Lowers.append(compute_EV_extreme(informations, nb_range, "min"))
        Mids.append(compute_EV(informations, distribution, nb_range))

        start = time.time()
        print(f"=== Round {i+1} ===")
        print("Known so far:", informations)
        t.start()
        bid = input("Enter your Bid (Buy max): ")
        bid = test_price(bid)
        ask = input("Enter your Ask (Sell min): ")
        ask = test_price(ask)
        t.cancel()
        end = time.time()

        Bids.append(bid)
        Asks.append(ask)
        Times.append(end - start)
        informations[i] = draw_card(distribution, nb_range)
        Spreads.append(ask - bid)

    X = [x + 1 for x in range(nb_step)]
    mxs = [nb_range] * nb_step
    mns = [0] * nb_step
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(X, Highers, label="Higher limit of uncertainty", color='red', linestyle='--')
    plt.plot(X, Lowers, label='Lower limit of uncertainty', color='red')
    plt.plot(X, Mids, color="green", label="True expected value")
    plt.plot(X, Bids, color="blue", label="Your Bids")
    plt.plot(X, Asks, color="blue", linestyle="--", label="Your Asks")
    plt.fill_between(X, Asks, Bids, color='mintcream')
    plt.fill_between(X, mns, Lowers, color='lightcoral')
    plt.fill_between(X, mxs, Highers, color='lightcoral')

    plt.title("Performance of Game | Avg calculation time: " + str(round(np.mean(Times), 1)) + 's')
    plt.legend()
    plt.ylabel('Value')
    plt.xlabel('Rounds')
    plt.ylim(0, nb_range)
    for i, v in enumerate(Mids):
        ax.annotate(str(v), xy=(i + 1, v), xytext=(-7, 7), textcoords='offset points', color='green')
    plt.show()

main()
