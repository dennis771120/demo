
import streamlit as st
from datetime import datetime, timedelta

st.title("📅 溢領金額計算工具")

# 使用者輸入
monthly_fee = st.number_input("每月包管費／代管費（元）", min_value=0, value=4000)
contract_start = st.date_input("合約起日", value=datetime(2025, 1, 1))
contract_end = st.date_input("合約迄日", value=datetime(2025, 12, 31))
cancel_date = st.date_input("解約日", value=datetime(2025, 5, 22))

# 計算按鈕
if st.button("計算溢領金額"):
    # 計算付款期
    pay_start = contract_start
    while pay_start <= cancel_date:
        try:
            pay_end = pay_start.replace(
                month=pay_start.month % 12 + 1,
                year=pay_start.year + (1 if pay_start.month == 12 else 0)
            ) - timedelta(days=1)
        except ValueError:
            # 處理月底問題
            next_month = (pay_start.month % 12) + 1
            next_year = pay_start.year + (1 if pay_start.month == 12 else 0)
            next_month_start = datetime(next_year, next_month, 1)
            pay_end = next_month_start - timedelta(days=1)

        if cancel_date <= pay_end:
            break
        pay_start = pay_end + timedelta(days=1)

    total_days = (pay_end - pay_start).days + 1
    unserved_start = cancel_date + timedelta(days=1)
    unserved_days = (pay_end - unserved_start).days + 1 if unserved_start <= pay_end else 0
    ratio = unserved_days / total_days
    overpaid = round(monthly_fee * ratio)

    # 顯示結果
    st.subheader("🧾 計算結果")
    st.write(f"付款期：{pay_start.strftime('%Y/%m/%d')} ～ {pay_end.strftime('%Y/%m/%d')}")
    st.write(f"付款期天數：{total_days} 天")
    st.write(f"未服務天數：{unserved_days} 天")
    st.write(f"溢領比例：{round(ratio, 4)}")
    st.success(f"💰 溢領金額：NT$ {overpaid:,} 元")
