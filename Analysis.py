import pandas as pd
import matplotlib.pyplot as plt
import os

# read the csv file
file1 = pd.read_csv(r'C:\Users\annad\Desktop\IDEATON_SKRYPT\kopia_xls_netto\kopia_daty\Stara_wersja\FAKTURY_NOWE.csv', sep=';')

# make a list of orders
list_of_defined_orders = []

for i in range(len(file1)):
    new_order = file1.iloc[i, 0]
    if new_order not in list_of_defined_orders:
        list_of_defined_orders.append(new_order)
#for i in range(len(list_of_defined_orders)):
#    print(list_of_defined_orders[i])
print("Zlecenia Ideatona to:", ", ".join(list_of_defined_orders))

# read the order selected by the user and throw an error if the order is not in the order list
chosen_order = input("Podaj nazwę zlecenia: ")
print("\n")

if chosen_order not in list_of_defined_orders:
    print("Nieprawidłowa nazwa klienta")
    exit()

# make a dataframe for the order selected by the user
chosen_order_dataframe = file1[file1["Nazwa zlecenia"] == chosen_order].copy()

# sort the data for the selected order according to the date
chosen_order_dataframe['Data'] = pd.to_datetime(chosen_order_dataframe['Data'])
sorted_dates = chosen_order_dataframe.sort_values(by="Data", ascending=True, inplace=True)
print("posortowane daty to:")
print(sorted_dates)

# calculate cumulative cost
# commas in decimals must be changed into dots in the xlsx file, otherwise cumsum does not work.
# to change the xlsx file, open File > Options > Advanced, tick off "Use system separators", type .
chosen_order_dataframe["Całkowity_koszt_kumulacyjny_brutto"] = chosen_order_dataframe["Koszt_brutto_w_zł"].cumsum()
chosen_order_dataframe["Całkowity_koszt_kumulacyjny_netto"] = chosen_order_dataframe["Koszt_netto_w_zł"].cumsum()
print("Całkowity koszt podany jest w ostatniej kolumnie.")
result = chosen_order_dataframe.loc[:, ["Nazwa zlecenia", "Data", "Całkowity_koszt_kumulacyjny_brutto", "Całkowity_koszt_kumulacyjny_netto" ]]
print(result)
result.to_html(os.path.join(r"C:\Users\annad\Desktop\ideaton", chosen_order))
print("\n")

# draw the plot
plt.scatter(result.Data, result.Całkowity_koszt_kumulacyjny_brutto)
plt.scatter(result.Data, result.Całkowity_koszt_kumulacyjny_netto)

font1 = {'family': 'serif', 'color': 'blue', 'size': 20}
font2 = {'family': 'serif', 'color': 'darkred', 'size': 11}

plt.title(f"Koszty: {chosen_order}", fontdict=font1)
plt.xlabel("czas", fontdict=font2)
plt.xticks(rotation = 90, fontsize=6)
plt.ylabel("całkowity koszt kumulacyjny [zł]", fontdict=font2)
plt.legend(["brutto", "netto"], loc='upper left')
plt.grid()

# save the file with the plot
file_name = input("Podaj nazwę pliku pod jaką ma być zapisany wykres: ")
plot_destination = os.path.join(r"C:\Users\annad\Desktop\ideaton", file_name)
plt.savefig(f"{plot_destination}.png")
plt.show()
print('finished!')
