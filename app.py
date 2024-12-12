import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 随机生成数据
def generate_data():
    regions = ['华北', '华东', '华南', '西南', '西北', '东北', '中南', '华中']
    provinces = ['北京市', '天津市', '河北省', '山西省', '内蒙古自治区', '辽宁省', '吉林省', '黑龙江省', '上海市', '江苏省', '浙江省', '安徽省', '福建省', '江西省', '山东省', '河南省', '湖北省', '湖南省', '广东省', '广西壮族自治区', '海南省', '重庆市', '四川省', '贵州省', '云南省', '陕西省', '甘肃省', '青海省', '宁夏回族自治区', '新疆维吾尔自治区']
    
    # 随机生成每月数据
    months = pd.date_range(start="2024-01-01", end="2024-12-31", freq="M").strftime('%Y-%m').tolist()
    
    data = {
        '地区': np.random.choice(regions, len(months) * len(provinces)),
        '省份': np.random.choice(provinces, len(months) * len(provinces)),
        '月份': np.tile(months, len(provinces)),
        '开立金额': np.random.randint(100, 1000, size=len(months) * len(provinces)),
        '融资金额': np.random.randint(50, 500, size=len(months) * len(provinces)),
        '新增客户数量': np.random.randint(1, 20, size=len(months) * len(provinces)),
        '销售人员数量': np.random.randint(1, 50, size=len(months) * len(provinces)),
    }
    
    return pd.DataFrame(data)

# 获取数据
data = generate_data()

# 页面布局
st.title("2024年全国及大区省份数据可视化")

# 层次1: 全国展示
level = st.selectbox("选择查看的层级", ("全国", "大区", "省份"))

# 月份选择
selected_months = st.multiselect("选择月份", data['月份'].unique(), default=data['月份'].unique())

# 数据指标选择
metrics = ['开立金额', '融资金额', '新增客户数量', '销售人员数量']
selected_metric = st.selectbox("选择展示的指标", metrics, index=metrics.index('开立金额'))

# 图表类型选择
chart_type = st.selectbox("选择图表类型", ("柱状图", "折线图", "饼图", "散点图", "热力图"))

# 过滤数据根据用户选择的月份
filtered_data = data[data['月份'].isin(selected_months)]

if level == "全国":
    # 全国展示
    st.subheader("全国数据展示")
    total_data = filtered_data.groupby(['月份', '地区']).agg({
        selected_metric: 'sum',
        '融资金额': 'sum',
        '新增客户数量': 'sum',
        '销售人员数量': 'sum'
    }).reset_index()

    if chart_type == "柱状图":
        fig = px.bar(total_data, x='月份', y=selected_metric, color='地区', title=f'全国各大区{selected_metric}')
        st.plotly_chart(fig)

    elif chart_type == "折线图":
        fig = px.line(total_data, x='月份', y=selected_metric, color='地区', title=f'全国各大区{selected_metric}')
        st.plotly_chart(fig)

    elif chart_type == "饼图":
        fig = px.pie(total_data, names='地区', values=selected_metric, title=f'全国各大区{selected_metric}比例')
        st.plotly_chart(fig)

    elif chart_type == "散点图":
        fig = px.scatter(total_data, x='月份', y=selected_metric, size='融资金额', color='地区', title=f'全国各大区{selected_metric}与融资金额')
        st.plotly_chart(fig)

    elif chart_type == "热力图":
        total_data_pivot = total_data.pivot("月份", "地区", selected_metric)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(total_data_pivot, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

elif level == "大区":
    # 层次2: 大区选择
    region = st.selectbox("选择大区", data['地区'].unique())
    region_data = filtered_data[filtered_data['地区'] == region]

    st.subheader(f"{region}数据展示")
    region_agg = region_data.groupby(['月份', '省份']).agg({
        selected_metric: 'sum',
        '融资金额': 'sum',
        '新增客户数量': 'sum',
        '销售人员数量': 'sum'
    }).reset_index()

    if chart_type == "柱状图":
        fig = px.bar(region_agg, x='月份', y=selected_metric, color='省份', title=f"{region}各省份{selected_metric}")
        st.plotly_chart(fig)

    elif chart_type == "折线图":
        fig = px.line(region_agg, x='月份', y=selected_metric, color='省份', title=f"{region}各省份{selected_metric}")
        st.plotly_chart(fig)

    elif chart_type == "饼图":
        fig = px.pie(region_agg, names='省份', values=selected_metric, title=f"{region}各省份{selected_metric}比例")
        st.plotly_chart(fig)

    elif chart_type == "散点图":
        fig = px.scatter(region_agg, x='月份', y=selected_metric, size='融资金额', color='省份', title=f"{region}各省份{selected_metric}与融资金额")
        st.plotly_chart(fig)

    elif chart_type == "热力图":
        region_agg_pivot = region_agg.pivot("月份", "省份", selected_metric)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(region_agg_pivot, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

elif level == "省份":
    # 层次3: 省份选择
    province = st.selectbox("选择省份", data['省份'].unique())
    province_data = filtered_data[filtered_data['省份'] == province]

    st.subheader(f"{province}数据展示")
    province_agg = province_data.groupby('月份').agg({
        selected_metric: 'sum',
        '融资金额': 'sum',
        '新增客户数量': 'sum',
        '销售人员数量': 'sum'
    }).reset_index()

    if chart_type == "柱状图":
        fig = px.bar(province_agg, x='月份', y=selected_metric, title=f"{province}{selected_metric}")
        st.plotly_chart(fig)

    elif chart_type == "折线图":
        fig = px.line(province_agg, x='月份', y=selected_metric, title=f"{province}{selected_metric}")
        st.plotly_chart(fig)

    elif chart_type == "饼图":
        fig = px.pie(province_agg, names='月份', values=selected_metric, title=f"{province}{selected_metric}比例")
        st.plotly_chart(fig)

    elif chart_type == "散点图":
        fig = px.scatter(province_agg, x='月份', y=selected_metric, size='融资金额', color='月份', title=f"{province}{selected_metric}与融资金额")
        st.plotly_chart(fig)

    elif chart_type == "热力图":
        province_agg_pivot = province_agg.pivot("月份", "月份", selected_metric)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(province_agg_pivot, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

# 显示数据表格
st.subheader("数据表格展示")
st.write(filtered_data)
