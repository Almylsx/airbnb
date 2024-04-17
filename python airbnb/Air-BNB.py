
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats


file_path = './listings.csv'
df = pd.read_csv(file_path)


df.dropna(subset=['price', 'availability_365'], inplace=True)
df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)


q1 = df['price'].quantile(0.25)
q3 = df['price'].quantile(0.75)
iqr = q3 - q1
df = df[(df['price'] >= (q1 - 1.5 * iqr)) & (df['price'] <= (q3 + 1.5 * iqr))]

plt.figure(figsize=(10, 6))
sns.histplot(df['price'], bins=30, kde=True)
plt.title('توزيع أسعار Airbnb')
plt.xlabel('السعر')
plt.ylabel('عدد القوائم')
plt.show()

plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='room_type')
plt.title('توزيع أنواع الغرف')
plt.xlabel('نوع الغرفة')
plt.ylabel('عدد القوائم')
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='longitude', y='latitude', hue='room_type', alpha=0.6)
plt.title('التوزيع الجغرافي لقوائم Airbnb')
plt.xlabel('خط الطول')
plt.ylabel('خط العرض')
plt.show()


entire_home_prices = df[df['room_type'] == 'Entire home/apt']['price']
private_room_prices = df[df['room_type'] == 'Private room']['price']
t_stat, p_value = stats.ttest_ind(entire_home_prices, private_room_prices, equal_var=False)
print(f'T-statistic: {t_stat}, P-value: {p_value}')

if p_value < 0.05:
    print('يوجد فرق معنوي في الأسعار بين النوعين من الغرف.')
else:
    print('لا يوجد فرق معنوي في الأسعار بين النوعين من الغرف.')


plt.savefig('price_distribution.png')
plt.savefig('room_type_distribution.png')
plt.savefig('geographical_distribution.png')

