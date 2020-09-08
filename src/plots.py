import matplotlib.pyplot as plt
def pie_chart_positions(stock, bond, cash):
    labels = ['Stock', 'Bond', 'Cash']
    sizes = [stock, bond, cash]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()

def pie_chart_positions_stock_bonds(stock, bond):
    labels = ['Stock', 'Bond']
    sizes = [stock, bond]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()