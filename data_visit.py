import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif']=['SimHei']
# pd.set_option("display.max_columns",None)

data = pd.read_csv(r"58home_info.csv",sep=",")


plt.subplots(figsize=(7,6))
plt.subplots_adjust(hspace=0.3)

# 各省份房总数top10
plt.subplot(211)
province_home_count_top10=data.groupby("homeprovince").count().sort_values(by="homename",ascending=False)[:10]
print(province_home_count_top10)
x=province_home_count_top10.index
y=province_home_count_top10["homename"]
bar_label = plt.bar(x,y,label="各省份房总数top10")
plt.bar_label(bar_label)
plt.legend(loc="upper center",bbox_to_anchor=(0.5,1.18))


# 省份平均房价top10
plt.subplot(212)
data["homecity"]=data["homeprovince"]+data["homecity"]
data = data.loc[data["homeprice"].str.startswith("均价")]
data["homeprice"]=data["homeprice"].str[2:-3].astype(int)
city_meanprice_top10=data.groupby("homecity")["homeprice"].mean().sort_values(ascending=False)[0:10]
x=city_meanprice_top10.index
y=np.round(city_meanprice_top10,2)
plt.xticks(rotation=30)
bars = plt.bar(x,y,label="省份平均房价top10",color="green")
plt.bar_label(bars,rotation=30)

plt.legend(loc="upper center",bbox_to_anchor=(0.5,1.18))
plt.show()

