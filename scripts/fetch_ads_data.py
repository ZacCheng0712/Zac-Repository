"""
拉取好享宅家床墊廣告指標（本週 vs 上週）
回傳結構化 dict 供報告生成使用
"""

import warnings
warnings.filterwarnings('ignore')
from google.ads.googleads.client import GoogleAdsClient
from datetime import datetime, timedelta

CUSTOMER_ID = "3382089284"

def fetch_campaign_metrics(client, customer_id, date_range_clause):
    ga_service = client.get_service("GoogleAdsService")
    query = f"""
        SELECT
            campaign.name,
            campaign.advertising_channel_type,
            metrics.impressions,
            metrics.clicks,
            metrics.ctr,
            metrics.average_cpc,
            metrics.conversions,
            metrics.cost_micros,
            metrics.cost_per_conversion
        FROM campaign
        WHERE {date_range_clause}
          AND campaign.status = 'ENABLED'
        ORDER BY metrics.cost_micros DESC
    """
    response = ga_service.search(customer_id=customer_id, query=query)
    results = []
    for row in response:
        if row.metrics.impressions == 0 and row.metrics.clicks == 0:
            continue
        ch = str(row.campaign.advertising_channel_type).split(".")[-1]
        results.append({
            "name": row.campaign.name,
            "type": ch,
            "impressions": row.metrics.impressions,
            "clicks": row.metrics.clicks,
            "ctr": row.metrics.ctr,
            "cpc": row.metrics.average_cpc / 1_000_000,
            "conversions": row.metrics.conversions,
            "cost": row.metrics.cost_micros / 1_000_000,
            "cpa": row.metrics.cost_per_conversion / 1_000_000 if row.metrics.conversions > 0 else 0,
        })
    return results

def get_ads_data():
    client = GoogleAdsClient.load_from_storage("config/google_ads.yaml")
    today = datetime.today()

    # 本週：過去 7 天
    this_week_end = today - timedelta(days=1)
    this_week_start = today - timedelta(days=7)
    this_clause = f"segments.date BETWEEN '{this_week_start.strftime('%Y-%m-%d')}' AND '{this_week_end.strftime('%Y-%m-%d')}'"

    # 上週：再前 7 天
    last_week_end = today - timedelta(days=8)
    last_week_start = today - timedelta(days=14)
    last_clause = f"segments.date BETWEEN '{last_week_start.strftime('%Y-%m-%d')}' AND '{last_week_end.strftime('%Y-%m-%d')}'"

    this_week = fetch_campaign_metrics(client, CUSTOMER_ID, this_clause)
    last_week = fetch_campaign_metrics(client, CUSTOMER_ID, last_clause)

    return {
        "this_week": {
            "period": f"{this_week_start.strftime('%m/%d')} ~ {this_week_end.strftime('%m/%d')}",
            "campaigns": this_week,
            "search": [c for c in this_week if c["type"] == "SEARCH"],
            "pmax": [c for c in this_week if c["type"] == "PERFORMANCE_MAX"],
        },
        "last_week": {
            "period": f"{last_week_start.strftime('%m/%d')} ~ {last_week_end.strftime('%m/%d')}",
            "campaigns": last_week,
            "search": [c for c in last_week if c["type"] == "SEARCH"],
            "pmax": [c for c in last_week if c["type"] == "PERFORMANCE_MAX"],
        }
    }

def calc_change(current, previous):
    """計算變化百分比"""
    if previous == 0:
        return None
    return (current - previous) / previous * 100

def summarize(data):
    """彙總本週 vs 上週的關鍵指標變化"""
    def total(campaigns, key):
        return sum(c[key] for c in campaigns)

    tw = data["this_week"]["campaigns"]
    lw = data["last_week"]["campaigns"]
    tw_s = data["this_week"]["search"]
    lw_s = data["last_week"]["search"]
    tw_p = data["this_week"]["pmax"]
    lw_p = data["last_week"]["pmax"]

    return {
        "period": data["this_week"]["period"],
        "compare_period": data["last_week"]["period"],
        "overall": {
            "impressions": total(tw, "impressions"),
            "clicks": total(tw, "clicks"),
            "conversions": total(tw, "conversions"),
            "cost": total(tw, "cost"),
            "impressions_chg": calc_change(total(tw, "impressions"), total(lw, "impressions")),
            "clicks_chg": calc_change(total(tw, "clicks"), total(lw, "clicks")),
            "conversions_chg": calc_change(total(tw, "conversions"), total(lw, "conversions")),
            "cost_chg": calc_change(total(tw, "cost"), total(lw, "cost")),
        },
        "search": {
            "impressions": total(tw_s, "impressions"),
            "clicks": total(tw_s, "clicks"),
            "conversions": total(tw_s, "conversions"),
            "ctr": total(tw_s, "clicks") / total(tw_s, "impressions") if total(tw_s, "impressions") > 0 else 0,
            "cpc": total(tw_s, "cost") / total(tw_s, "clicks") if total(tw_s, "clicks") > 0 else 0,
            "cpa": total(tw_s, "cost") / total(tw_s, "conversions") if total(tw_s, "conversions") > 0 else 0,
            "impressions_chg": calc_change(total(tw_s, "impressions"), total(lw_s, "impressions")),
            "clicks_chg": calc_change(total(tw_s, "clicks"), total(lw_s, "clicks")),
            "conversions_chg": calc_change(total(tw_s, "conversions"), total(lw_s, "conversions")),
            "ctr_chg": calc_change(
                total(tw_s, "clicks") / total(tw_s, "impressions") if total(tw_s, "impressions") > 0 else 0,
                total(lw_s, "clicks") / total(lw_s, "impressions") if total(lw_s, "impressions") > 0 else 0
            ),
            "cpc_chg": calc_change(
                total(tw_s, "cost") / total(tw_s, "clicks") if total(tw_s, "clicks") > 0 else 0,
                total(lw_s, "cost") / total(lw_s, "clicks") if total(lw_s, "clicks") > 0 else 0
            ),
            "campaigns": tw_s,
            "campaigns_prev": lw_s,
        },
        "pmax": {
            "impressions": total(tw_p, "impressions"),
            "clicks": total(tw_p, "clicks"),
            "conversions": total(tw_p, "conversions"),
            "ctr": total(tw_p, "clicks") / total(tw_p, "impressions") if total(tw_p, "impressions") > 0 else 0,
            "cpa": total(tw_p, "cost") / total(tw_p, "conversions") if total(tw_p, "conversions") > 0 else 0,
            "impressions_chg": calc_change(total(tw_p, "impressions"), total(lw_p, "impressions")),
            "clicks_chg": calc_change(total(tw_p, "clicks"), total(lw_p, "clicks")),
            "conversions_chg": calc_change(total(tw_p, "conversions"), total(lw_p, "conversions")),
            "campaigns": tw_p,
            "campaigns_prev": lw_p,
        }
    }

if __name__ == "__main__":
    import json
    data = get_ads_data()
    summary = summarize(data)
    print(f"本週：{summary['period']} vs 比較期：{summary['compare_period']}")
    print(f"\n[關鍵字] 曝光 {summary['search']['impressions']:,} ({summary['search']['impressions_chg']:+.1f}%) | 點擊 {summary['search']['clicks']:,} ({summary['search']['clicks_chg']:+.1f}%) | 轉換 {summary['search']['conversions']:.0f} ({summary['search']['conversions_chg']:+.1f}%)")
    print(f"         CTR {summary['search']['ctr']:.2%} ({summary['search']['ctr_chg']:+.1f}%) | CPC ${summary['search']['cpc']:.0f} ({summary['search']['cpc_chg']:+.1f}%) | CPA ${summary['search']['cpa']:.0f}")
    print(f"\n[PMAX]  曝光 {summary['pmax']['impressions']:,} ({summary['pmax']['impressions_chg']:+.1f}%) | 點擊 {summary['pmax']['clicks']:,} ({summary['pmax']['clicks_chg']:+.1f}%) | 轉換 {summary['pmax']['conversions']:.0f} ({summary['pmax']['conversions_chg']:+.1f}%)")
