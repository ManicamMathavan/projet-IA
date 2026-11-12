import matplotlib.pyplot as plt

class PlotGraph:
    @staticmethod
    def plot_sales_by_promo(df, sales_column='Sales', title_suffix=''):
        plt.figure(figsize=(7, 4))
        promo_sales = df.groupby('Promo')[sales_column].mean()
        colors = ['#ff6347', '#90ee90'] if len(promo_sales) > 1 else ['skyblue']
        promo_sales.plot(kind='bar', color=colors, edgecolor='gray')
        plt.title(f"Ventes moyennes selon la présence d'une promotion {title_suffix}")
        plt.xlabel("Promotion (0 = non, 1 = oui)")
        plt.ylabel("Ventes moyennes")
        plt.xticks(rotation=0)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

    @staticmethod
    def plot_sales_by_day(df, sales_column='Sales', title_suffix=''):
        plt.figure(figsize=(9, 5))
        day_sales = df.groupby('DayOfWeek')[sales_column].mean()
        day_sales.plot(kind='bar', color='skyblue', edgecolor='gray')
        plt.title(f"Ventes moyennes par jour de la semaine {title_suffix}")
        plt.xlabel("Jour de la semaine (0 = Lundi, 6 = Dimanche)")
        plt.ylabel("Ventes moyennes")
        plt.xticks(ticks=range(len(day_sales)), labels=["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"][:len(day_sales)], rotation=0)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

    @staticmethod
    def plot_sales_by_store_type(df, sales_column='Sales', title_suffix=''):
        plt.figure(figsize=(7, 4))
        store_sales = df.groupby('StoreType')[sales_column].mean()
        store_sales.plot(kind='bar', color='skyblue', edgecolor='gray')
        plt.title(f"Ventes moyennes en fonction du type du magasin {title_suffix}")
        plt.xlabel("Type du magasin")
        plt.ylabel("Ventes moyennes")
        plt.xticks(rotation=0)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

# Création de l'alias gr
gr = PlotGraph()