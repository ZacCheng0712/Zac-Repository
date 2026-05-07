"""
拉取采姸服飾 Meta 廣告指標
- 帳號層：本月至今 vs 上月同期
- 活動層：各活動成效拆分
- 素材（Ad）層：每支素材的轉換效率
回傳結構化 dict 供月報生成使用
"""

import json
import requests
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

CONFIG_PATH = "config/meta_ads.json"
ACCOUNT_ID = "act_855160356095857"
GA4_PROPERTY_ID = "464488069"

API_VERSION = "v21.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

MARGIN_MULTIPLIER = 1 / 0.8  # 實際花費 × 1.25 = 客戶認知花費

PURCHASE_FIELDS = [
    "impressions",
    "clicks",
    "ctr",
    "cpm",
    "spend",
    "reach",
    "frequency",
    "actions",
    "action_values",
    "cost_per_action_type",
    "website_ctr",
    "unique_clicks",
    "unique_ctr",
]

def load_config():
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "meta" in st.secrets:
            return {
                "app_id": st.secrets["meta"]["app_id"],
                "app_secret": st.secrets["meta"]["app_secret"],
                "long_lived_token": st.secrets["meta"]["long_lived_token"],
                "token_expires": st.secrets["meta"]["token_expires"],
                "ad_accounts": json.loads(st.secrets["meta"]["ad_accounts_json"]),
            }
    except Exception:
        pass
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def get_date_ranges():
    today = date.today()
    # 本月至今（排除今天，昨天為止）
    this_month_start = today.replace(day=1)
    this_month_end = today - relativedelta(days=1)

    # 上月同期（1號到上月的同一天，避免超過上月天數）
    last_month_start = (this_month_start - relativedelta(months=1))
    last_month_day = min(today.day, (last_month_start + relativedelta(months=1) - relativedelta(days=1)).day)
    last_month_end = last_month_start.replace(day=last_month_day)

    return {
        "this_month": {
            "since": this_month_start.strftime("%Y-%m-%d"),
            "until": this_month_end.strftime("%Y-%m-%d"),
        },
        "last_month": {
            "since": last_month_start.strftime("%Y-%m-%d"),
            "until": last_month_end.strftime("%Y-%m-%d"),
        },
        "last_month_full": {
            "since": last_month_start.strftime("%Y-%m-%d"),
            "until": (last_month_start + relativedelta(months=1) - relativedelta(days=1)).strftime("%Y-%m-%d"),
        }
    }

def extract_action(actions, action_type):
    if not actions:
        return 0
    for a in actions:
        if a["action_type"] == action_type:
            return float(a["value"])
    return 0

def extract_action_value(action_values, action_type):
    if not action_values:
        return 0
    for a in action_values:
        if a["action_type"] == action_type:
            return float(a["value"])
    return 0

def parse_insights(data):
    """從一筆 insight row 萃取關鍵指標（花費相關指標已換算為客戶認知金額）"""
    actual_spend = float(data.get("spend", 0))
    # 客戶認知花費（含代操利潤）
    spend = actual_spend * MARGIN_MULTIPLIER

    impressions = int(data.get("impressions", 0))
    clicks = int(data.get("clicks", 0))
    reach = int(data.get("reach", 0))
    frequency = float(data.get("frequency", 0))
    ctr = float(data.get("ctr", 0))

    actions = data.get("actions", [])
    action_values = data.get("action_values", [])

    add_to_cart = extract_action(actions, "add_to_cart")
    initiate_checkout = extract_action(actions, "initiate_checkout")
    purchases = extract_action(actions, "purchase")
    purchase_value = extract_action_value(action_values, "purchase")
    link_clicks = extract_action(actions, "link_click")
    landing_page_view = int(extract_action(actions, "landing_page_view"))

    # 連結點閱率（不涉及花費，不調整）
    link_ctr = (link_clicks / impressions * 100) if impressions > 0 else 0
    # 千次曝光成本（用客戶認知花費）
    cpm = spend / impressions * 1000 if impressions > 0 else 0
    # 點擊成本（用客戶認知花費）
    cpc = spend / clicks if clicks > 0 else 0
    # 購買成本（用客戶認知花費）
    cpa = spend / purchases if purchases > 0 else 0
    # ROAS（用客戶認知花費，數值會低於後台）
    roas = purchase_value / spend if spend > 0 else 0
    # 客單價（不涉及花費，不調整）
    avg_order_value = purchase_value / purchases if purchases > 0 else 0
    # 轉換率 = 購買 / 頁面瀏覽（真正進站分母）
    conversion_rate = purchases / landing_page_view * 100 if landing_page_view > 0 else 0
    # 加入購物車率 = 加購 / 頁面瀏覽（真正進站分母）
    add_to_cart_rate = add_to_cart / landing_page_view * 100 if landing_page_view > 0 else 0
    # 加購成本（用客戶認知花費）
    cpa_cart = spend / add_to_cart if add_to_cart > 0 else 0
    # 開始結帳率 = 開始結帳 / 加入購物車（漏斗進展率）
    checkout_rate = initiate_checkout / add_to_cart * 100 if add_to_cart > 0 else 0

    return {
        "spend":             round(spend, 0),
        "actual_spend":      round(actual_spend, 0),
        "impressions":       impressions,
        "reach":             reach,
        "frequency":         round(frequency, 2),
        "cpm":               round(cpm, 2),
        "clicks":            clicks,
        "ctr":               round(ctr, 2),
        "link_clicks":       int(link_clicks),
        "link_ctr":          round(link_ctr, 2),
        "cpc":               round(cpc, 2),
        "add_to_cart":       int(add_to_cart),
        "add_to_cart_rate":  round(add_to_cart_rate, 2),
        "initiate_checkout": int(initiate_checkout),
        "checkout_rate":     round(checkout_rate, 2),
        "purchases":         int(purchases),
        "purchase_value":    round(purchase_value, 0),
        "cpa":               round(cpa, 2),
        "roas":              round(roas, 2),
        "avg_order_value":   round(avg_order_value, 0),
        "conversion_rate":   round(conversion_rate, 2),
        "landing_page_view": landing_page_view,
        "cpa_cart":          round(cpa_cart, 2),
    }

def fetch_insights(token, account_id, date_range, level="account", fields=None):
    if fields is None:
        fields = PURCHASE_FIELDS
    url = f"{BASE_URL}/{account_id}/insights"
    params = {
        "access_token": token,
        "time_range": json.dumps(date_range),
        "level": level,
        "fields": ",".join(fields),
        "limit": 100,
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json().get("data", [])

def fetch_ad_insights(token, account_id, date_range):
    """素材（Ad）層，含素材名稱"""
    url = f"{BASE_URL}/{account_id}/insights"
    fields = PURCHASE_FIELDS + ["ad_name", "ad_id"]
    params = {
        "access_token": token,
        "time_range": json.dumps(date_range),
        "level": "ad",
        "fields": ",".join(fields),
        "limit": 100,
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json().get("data", [])

def fetch_daily_insights(token, account_id, since, until):
    """每日 breakdown，用於趨勢圖（time_increment=1）"""
    url = f"{BASE_URL}/{account_id}/insights"
    params = {
        "access_token": token,
        "time_range": json.dumps({"since": since, "until": until}),
        "level": "account",
        "time_increment": 1,
        "fields": ",".join(PURCHASE_FIELDS),
        "limit": 100,
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json().get("data", [])


def get_daily_data(days=30, since=None, until=None):
    """取得指定日期區間每日指標，供趨勢圖使用"""
    config = load_config()
    token = config["long_lived_token"]
    if not since or not until:
        today = date.today()
        since = (today - relativedelta(days=days)).strftime("%Y-%m-%d")
        until = (today - relativedelta(days=1)).strftime("%Y-%m-%d")
    raw = fetch_daily_insights(token, ACCOUNT_ID, since, until)
    daily = []
    for row in raw:
        parsed = parse_insights(row)
        parsed["date"] = row.get("date_start", "")
        daily.append(parsed)
    return sorted(daily, key=lambda x: x["date"])


def fetch_campaign_insights(token, account_id, date_range):
    """活動層"""
    url = f"{BASE_URL}/{account_id}/insights"
    fields = PURCHASE_FIELDS + ["campaign_name", "campaign_id"]
    params = {
        "access_token": token,
        "time_range": json.dumps(date_range),
        "level": "campaign",
        "fields": ",".join(fields),
        "limit": 100,
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json().get("data", [])

def get_meta_data():
    config = load_config()
    token = config["long_lived_token"]
    ranges = get_date_ranges()

    # 帳號層：本月 vs 上月同期
    this_raw = fetch_insights(token, ACCOUNT_ID, ranges["this_month"])
    last_raw = fetch_insights(token, ACCOUNT_ID, ranges["last_month"])

    this_account = parse_insights(this_raw[0]) if this_raw else {}
    last_account = parse_insights(last_raw[0]) if last_raw else {}

    # 活動層：本月
    campaigns_raw = fetch_campaign_insights(token, ACCOUNT_ID, ranges["this_month"])
    campaigns = []
    for c in campaigns_raw:
        parsed = parse_insights(c)
        parsed["name"] = c.get("campaign_name", "")
        parsed["id"] = c.get("campaign_id", "")
        campaigns.append(parsed)

    # 素材層：本月
    ads_raw = fetch_ad_insights(token, ACCOUNT_ID, ranges["this_month"])
    ads = []
    for a in ads_raw:
        parsed = parse_insights(a)
        parsed["name"] = a.get("ad_name", "")
        parsed["id"] = a.get("ad_id", "")
        ads.append(parsed)

    # 素材層：上月同期（用於素材若跨月仍在跑時比較）
    ads_last_raw = fetch_ad_insights(token, ACCOUNT_ID, ranges["last_month"])
    ads_last = []
    for a in ads_last_raw:
        parsed = parse_insights(a)
        parsed["name"] = a.get("ad_name", "")
        parsed["id"] = a.get("ad_id", "")
        ads_last.append(parsed)

    return {
        "account_id": ACCOUNT_ID,
        "this_month": {
            "period": f"{ranges['this_month']['since']} ~ {ranges['this_month']['until']}",
            "account": this_account,
            "campaigns": campaigns,
            "ads": ads,
        },
        "last_month": {
            "period": f"{ranges['last_month']['since']} ~ {ranges['last_month']['until']}",
            "account": last_account,
            "ads": ads_last,
        },
        "last_month_full_period": ranges["last_month_full"],
    }

def get_meta_data_flex(since, until, compare_since, compare_until):
    """自訂日期範圍版本，供 dashboard 日期選擇器使用"""
    config = load_config()
    token = config["long_lived_token"]

    this_range    = {"since": since,         "until": until}
    compare_range = {"since": compare_since, "until": compare_until}

    this_raw    = fetch_insights(token, ACCOUNT_ID, this_range)
    compare_raw = fetch_insights(token, ACCOUNT_ID, compare_range)
    this_account    = parse_insights(this_raw[0])    if this_raw    else {}
    compare_account = parse_insights(compare_raw[0]) if compare_raw else {}

    campaigns_raw = fetch_campaign_insights(token, ACCOUNT_ID, this_range)
    campaigns = []
    for c in campaigns_raw:
        parsed = parse_insights(c)
        parsed["name"] = c.get("campaign_name", "")
        parsed["id"]   = c.get("campaign_id", "")
        campaigns.append(parsed)

    ads_raw = fetch_ad_insights(token, ACCOUNT_ID, this_range)
    ads = []
    for a in ads_raw:
        parsed = parse_insights(a)
        parsed["name"] = a.get("ad_name", "")
        parsed["id"]   = a.get("ad_id", "")
        ads.append(parsed)

    return {
        "account_id": ACCOUNT_ID,
        "this_period": {
            "period": f"{since} ~ {until}",
            "account": this_account,
            "campaigns": campaigns,
            "ads": ads,
        },
        "compare_period": {
            "period": f"{compare_since} ~ {compare_until}",
            "account": compare_account,
        },
    }


def summarize_flex(data):
    """彙總比較結構（flex 版）"""
    tm = data["this_period"]["account"]
    cm = data["compare_period"]["account"]

    def chg(key):
        return calc_change(tm.get(key, 0), cm.get(key, 0))

    return {
        "period":         data["this_period"]["period"],
        "compare_period": data["compare_period"]["period"],
        "account": {
            **tm,
            "spend_chg":           chg("spend"),
            "impressions_chg":     chg("impressions"),
            "clicks_chg":          chg("clicks"),
            "ctr_chg":             chg("ctr"),
            "cpm_chg":             chg("cpm"),
            "link_clicks_chg":     chg("link_clicks"),
            "link_ctr_chg":        chg("link_ctr"),
            "cpc_chg":             chg("cpc"),
            "add_to_cart_chg":     chg("add_to_cart"),
            "add_to_cart_rate_chg":chg("add_to_cart_rate"),
            "purchases_chg":       chg("purchases"),
            "purchase_value_chg":  chg("purchase_value"),
            "roas_chg":            chg("roas"),
            "cpa_chg":             chg("cpa"),
            "avg_order_value_chg": chg("avg_order_value"),
            "conversion_rate_chg": chg("conversion_rate"),
            "frequency_chg":         chg("frequency"),
            "reach_chg":             chg("reach"),
            "initiate_checkout_chg": chg("initiate_checkout"),
            "landing_page_view_chg": chg("landing_page_view"),
            "cpa_cart_chg":          chg("cpa_cart"),
            "checkout_rate_chg":     chg("checkout_rate"),
        },
        "compare_account": cm,
        "campaigns": data["this_period"]["campaigns"],
        "ads":       data["this_period"]["ads"],
    }


def calc_change(current, previous):
    if previous == 0:
        return None
    return round((current - previous) / previous * 100, 1)

def summarize(data):
    """產生供月報使用的彙總比較結構"""
    tm = data["this_month"]["account"]
    lm = data["last_month"]["account"]

    def chg(key):
        return calc_change(tm.get(key, 0), lm.get(key, 0))

    return {
        "period": data["this_month"]["period"],
        "compare_period": data["last_month"]["period"],
        "account": {
            **tm,
            "spend_chg": chg("spend"),
            "impressions_chg": chg("impressions"),
            "clicks_chg": chg("clicks"),
            "ctr_chg": chg("ctr"),
            "cpm_chg": chg("cpm"),
            "link_clicks_chg": chg("link_clicks"),
            "link_ctr_chg": chg("link_ctr"),
            "cpc_chg": chg("cpc"),
            "add_to_cart_chg": chg("add_to_cart"),
            "add_to_cart_rate_chg": chg("add_to_cart_rate"),
            "purchases_chg": chg("purchases"),
            "purchase_value_chg": chg("purchase_value"),
            "roas_chg": chg("roas"),
            "cpa_chg": chg("cpa"),
            "avg_order_value_chg": chg("avg_order_value"),
            "conversion_rate_chg": chg("conversion_rate"),
            "frequency_chg":         chg("frequency"),
            "reach_chg":             chg("reach"),
            "initiate_checkout_chg": chg("initiate_checkout"),
            "landing_page_view_chg": chg("landing_page_view"),
            "cpa_cart_chg":          chg("cpa_cart"),
            "checkout_rate_chg":     chg("checkout_rate"),
        },
        "campaigns": data["this_month"]["campaigns"],
        "ads": data["this_month"]["ads"],
        "ads_last": data["last_month"]["ads"],
    }

if __name__ == "__main__":
    data = get_meta_data()
    summary = summarize(data)
    tm = summary["account"]

    print(f"采姸服飾 Meta 廣告成效")
    print(f"本月至今：{summary['period']}  vs  上月同期：{summary['compare_period']}")
    print()
    print(f"[帳號整體]")
    print(f"  花費：NT${tm['spend']:,.0f}  ({tm['spend_chg']:+.1f}%)")
    print(f"  曝光：{tm['impressions']:,}  ({tm['impressions_chg']:+.1f}%)  CPM：NT${tm['cpm']:,.0f}  ({tm['cpm_chg']:+.1f}%)")
    print(f"  觸及：{tm['reach']:,}  頻率：{tm['frequency']}次  ({tm['frequency_chg']:+.1f}%)")
    print(f"  連結點擊：{tm['link_clicks']:,}  ({tm['link_clicks_chg']:+.1f}%)  連結點閱率：{tm['link_ctr']:.2f}%  ({tm['link_ctr_chg']:+.1f}%)")
    print(f"  CPC：NT${tm['cpc']:,.0f}  ({tm['cpc_chg']:+.1f}%)")
    print()
    print(f"[購買漏斗]")
    print(f"  加入購物車：{tm['add_to_cart']}  ({tm['add_to_cart_chg']:+.1f}%)  加購率：{tm['add_to_cart_rate']:.1f}%  ({tm['add_to_cart_rate_chg']:+.1f}%)")
    print(f"  開始結帳：{tm['initiate_checkout']}")
    print(f"  購買：{tm['purchases']}  ({tm['purchases_chg']:+.1f}%)  購買成本：NT${tm['cpa']:,.0f}  ({tm['cpa_chg']:+.1f}%)")
    print(f"  客單價：NT${tm['avg_order_value']:,.0f}  ({tm['avg_order_value_chg']:+.1f}%)  轉換率：{tm['conversion_rate']:.2f}%  ({tm['conversion_rate_chg']:+.1f}%)")
    print(f"  轉換價值：NT${tm['purchase_value']:,.0f}  ROAS：{tm['roas']:.2f}  ({tm['roas_chg']:+.1f}%)")
    print()
    print(f"[素材表現]")
    for ad in sorted(summary["ads"], key=lambda x: x["spend"], reverse=True):
        print(f"  {ad['name']}")
        print(f"    花費 NT${ad['spend']:,.0f} | 點閱率 {ad['ctr']:.2f}% | 連結點閱率 {ad['link_ctr']:.2f}% | 加購率 {ad['add_to_cart_rate']:.1f}% | 轉換率 {ad['conversion_rate']:.2f}% | 購買 {ad['purchases']} 筆 | 客單價 NT${ad['avg_order_value']:,.0f} | ROAS {ad['roas']:.2f}")
