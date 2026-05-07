"""GA4 網站流量拉取 — 采妍官網 (Property: 464488069)"""
import json

CONFIG_PATH = "config/ga4.json"
GA4_PROPERTY_ID = "464488069"


def _creds():
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "ga4" in st.secrets:
            cfg = {
                "client_id": st.secrets["ga4"]["client_id"],
                "client_secret": st.secrets["ga4"]["client_secret"],
                "refresh_token": st.secrets["ga4"]["refresh_token"],
            }
        else:
            raise KeyError("no st.secrets ga4")
    except Exception:
        with open(CONFIG_PATH, "r") as f:
            cfg = json.load(f)
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    creds = Credentials(
        token=None,
        refresh_token=cfg["refresh_token"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=cfg["client_id"],
        client_secret=cfg["client_secret"],
        scopes=["https://www.googleapis.com/auth/analytics.readonly"],
    )
    creds.refresh(Request())
    return creds


def _chg(curr, prev):
    if not prev:
        return None
    return round((curr - prev) / prev * 100, 1)


def _fmt_dur(seconds):
    if not seconds:
        return "0:00"
    m = int(float(seconds) // 60)
    s = int(float(seconds) % 60)
    return f"{m}:{s:02d}"


def get_ga4_summary(since, until, compare_since, compare_until):
    """帳號摘要指標，含比較期。回傳 (current_dict, compare_dict)

    注意：dateRange 不可放在 dimensions 內，API 會自動附加。
    無其他 dimensions 時，row.dimension_values[0] = dateRange。
    """
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        RunReportRequest, DateRange, Metric,
    )
    client = BetaAnalyticsDataClient(credentials=_creds())
    req = RunReportRequest(
        property=f"properties/{GA4_PROPERTY_ID}",
        date_ranges=[
            DateRange(start_date=since, end_date=until),
            DateRange(start_date=compare_since, end_date=compare_until),
        ],
        # dateRange 由 API 自動附加，不可顯式宣告
        metrics=[
            Metric(name="sessions"),
            Metric(name="screenPageViews"),
            Metric(name="engagementRate"),
            Metric(name="averageSessionDuration"),
            Metric(name="bounceRate"),
            Metric(name="totalUsers"),
            Metric(name="newUsers"),
        ],
    )
    resp = client.run_report(req)

    def _parse(vals):
        return {
            "sessions":             int(float(vals[0])),
            "pageviews":            int(float(vals[1])),
            "engagement_rate":      round(float(vals[2]) * 100, 1),
            "avg_session_duration": round(float(vals[3]), 0),
            "bounce_rate":          round(float(vals[4]) * 100, 1),
            "total_users":          int(float(vals[5])),
            "new_users":            int(float(vals[6])),
        }

    current = {}
    compare = {}
    for row in resp.rows:
        # 無顯式 dimension → dateRange 自動附加為唯一 dimension_value[0]
        period = row.dimension_values[0].value
        vals = [v.value for v in row.metric_values]
        if period == "date_range_0":
            current = _parse(vals)
        else:
            compare = _parse(vals)
    return current, compare


def get_ga4_traffic_sources(since, until, compare_since, compare_until, limit=15):
    """工作階段來源/媒介，含比較期

    有 sessionSourceMedium 作為顯式 dimension：
      row.dimension_values[0] = sessionSourceMedium
      row.dimension_values[1] = dateRange（API 自動附加）
    """
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        RunReportRequest, DateRange, Metric, Dimension, OrderBy,
    )
    client = BetaAnalyticsDataClient(credentials=_creds())
    req = RunReportRequest(
        property=f"properties/{GA4_PROPERTY_ID}",
        date_ranges=[
            DateRange(start_date=since, end_date=until),
            DateRange(start_date=compare_since, end_date=compare_until),
        ],
        dimensions=[
            Dimension(name="sessionSourceMedium"),  # [0]
            # dateRange 由 API 自動附加為 [1]
        ],
        metrics=[
            Metric(name="sessions"),
            Metric(name="engagedSessions"),
            Metric(name="engagementRate"),
            Metric(name="averageSessionDuration"),
            Metric(name="eventCount"),
            Metric(name="keyEvents"),
            Metric(name="totalRevenue"),
        ],
        order_bys=[OrderBy(
            metric=OrderBy.MetricOrderBy(metric_name="sessions"),
            desc=True,
        )],
        limit=limit * 2,
    )
    resp = client.run_report(req)

    def _parse(vals):
        sessions = int(float(vals[0]))
        engaged  = int(float(vals[1]))
        return {
            "sessions":         sessions,
            "engaged_sessions": engaged,
            "engagement_rate":  round(float(vals[2]) * 100, 1),
            "avg_duration":     round(float(vals[3]), 0),
            "event_count":      int(float(vals[4])),
            "key_events":       int(float(vals[5])),
            "key_event_rate":   round(engaged / sessions * 100, 2) if sessions > 0 else 0,
            "revenue":          round(float(vals[6]), 0),
        }

    curr_map, prev_map = {}, {}
    for row in resp.rows:
        source = row.dimension_values[0].value   # sessionSourceMedium
        period = row.dimension_values[1].value   # dateRange（自動附加）
        parsed = _parse([v.value for v in row.metric_values])
        if period == "date_range_0":
            curr_map[source] = parsed
        else:
            prev_map[source] = parsed

    all_sources = sorted(
        set(curr_map) | set(prev_map),
        key=lambda s: curr_map.get(s, {}).get("sessions", 0),
        reverse=True,
    )[:limit]

    result = []
    for source in all_sources:
        c = curr_map.get(source, {})
        p = prev_map.get(source, {})
        result.append({
            "source":                source,
            "sessions":              c.get("sessions", 0),
            "sessions_chg":          _chg(c.get("sessions", 0), p.get("sessions")),
            "engaged_sessions":      c.get("engaged_sessions", 0),
            "engaged_sessions_chg":  _chg(c.get("engaged_sessions", 0), p.get("engaged_sessions")),
            "engagement_rate":       c.get("engagement_rate", 0),
            "engagement_rate_chg":   _chg(c.get("engagement_rate", 0), p.get("engagement_rate")),
            "avg_duration":          c.get("avg_duration", 0),
            "avg_duration_fmt":      _fmt_dur(c.get("avg_duration", 0)),
            "avg_duration_chg":      _chg(c.get("avg_duration", 0), p.get("avg_duration")),
            "event_count":           c.get("event_count", 0),
            "event_count_chg":       _chg(c.get("event_count", 0), p.get("event_count")),
            "key_events":            c.get("key_events", 0),
            "key_events_chg":        _chg(c.get("key_events", 0), p.get("key_events")),
            "key_event_rate":        c.get("key_event_rate", 0),
            "key_event_rate_chg":    _chg(c.get("key_event_rate", 0), p.get("key_event_rate")),
            "revenue":               c.get("revenue", 0),
            "revenue_chg":           _chg(c.get("revenue", 0), p.get("revenue")),
        })
    return result


def get_ga4_pages(since, until, compare_since, compare_until, limit=20):
    """網頁路徑參與指標，含比較期

      row.dimension_values[0] = pagePath
      row.dimension_values[1] = dateRange（API 自動附加）
    """
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        RunReportRequest, DateRange, Metric, Dimension, OrderBy,
    )
    client = BetaAnalyticsDataClient(credentials=_creds())
    req = RunReportRequest(
        property=f"properties/{GA4_PROPERTY_ID}",
        date_ranges=[
            DateRange(start_date=since, end_date=until),
            DateRange(start_date=compare_since, end_date=compare_until),
        ],
        dimensions=[
            Dimension(name="pagePath"),  # [0]
            # dateRange 由 API 自動附加為 [1]
        ],
        metrics=[
            Metric(name="screenPageViews"),
            Metric(name="activeUsers"),
            Metric(name="userEngagementDuration"),
            Metric(name="eventCount"),
            Metric(name="keyEvents"),
            Metric(name="totalRevenue"),
        ],
        order_bys=[OrderBy(
            metric=OrderBy.MetricOrderBy(metric_name="screenPageViews"),
            desc=True,
        )],
        limit=limit * 2,
    )
    resp = client.run_report(req)

    def _parse(vals):
        views = int(float(vals[0]))
        users = int(float(vals[1]))
        dur   = float(vals[2])
        return {
            "views":           views,
            "active_users":    users,
            "views_per_user":  round(views / users, 2) if users > 0 else 0,
            "avg_dur_per_user": round(dur / users, 0) if users > 0 else 0,
            "event_count":     int(float(vals[3])),
            "key_events":      int(float(vals[4])),
            "revenue":         round(float(vals[5]), 0),
        }

    curr_map, prev_map = {}, {}
    for row in resp.rows:
        path   = row.dimension_values[0].value   # pagePath
        period = row.dimension_values[1].value   # dateRange（自動附加）
        parsed = _parse([v.value for v in row.metric_values])
        if period == "date_range_0":
            curr_map[path] = parsed
        else:
            prev_map[path] = parsed

    all_paths = sorted(
        set(curr_map) | set(prev_map),
        key=lambda p: curr_map.get(p, {}).get("views", 0),
        reverse=True,
    )[:limit]

    result = []
    for path in all_paths:
        c = curr_map.get(path, {})
        p = prev_map.get(path, {})
        result.append({
            "path":                 path,
            "views":                c.get("views", 0),
            "views_chg":            _chg(c.get("views", 0), p.get("views")),
            "active_users":         c.get("active_users", 0),
            "active_users_chg":     _chg(c.get("active_users", 0), p.get("active_users")),
            "views_per_user":       c.get("views_per_user", 0),
            "avg_dur_per_user":     c.get("avg_dur_per_user", 0),
            "avg_dur_per_user_chg": _chg(c.get("avg_dur_per_user", 0), p.get("avg_dur_per_user")),
            "avg_dur_per_user_fmt": _fmt_dur(c.get("avg_dur_per_user", 0)),
            "event_count":          c.get("event_count", 0),
            "event_count_chg":      _chg(c.get("event_count", 0), p.get("event_count")),
            "key_events":           c.get("key_events", 0),
            "key_events_chg":       _chg(c.get("key_events", 0), p.get("key_events")),
            "revenue":              c.get("revenue", 0),
            "revenue_chg":          _chg(c.get("revenue", 0), p.get("revenue")),
        })
    return result


def get_ga4_products(since, until, compare_since, compare_until, limit=20):
    """商品購買/收益，含比較期。

    注意：itemName 維度只相容 itemsPurchased / itemRevenue，
    itemViews / addToCarts 在此 GA4 屬性無法混用，已移除。
      row.dimension_values[0] = itemName
      row.dimension_values[1] = dateRange（API 自動附加）
    """
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        RunReportRequest, DateRange, Metric, Dimension, OrderBy,
    )
    client = BetaAnalyticsDataClient(credentials=_creds())
    req = RunReportRequest(
        property=f"properties/{GA4_PROPERTY_ID}",
        date_ranges=[
            DateRange(start_date=since, end_date=until),
            DateRange(start_date=compare_since, end_date=compare_until),
        ],
        dimensions=[
            Dimension(name="itemName"),  # [0]
            # dateRange 由 API 自動附加為 [1]
        ],
        metrics=[
            Metric(name="itemsPurchased"),
            Metric(name="itemRevenue"),
        ],
        order_bys=[OrderBy(
            metric=OrderBy.MetricOrderBy(metric_name="itemRevenue"),
            desc=True,
        )],
        limit=limit * 2,
    )
    resp = client.run_report(req)

    def _parse(vals):
        pur = int(float(vals[0]))
        rev = round(float(vals[1]), 0)
        return {
            "purchases": pur,
            "revenue":   rev,
        }

    curr_map, prev_map = {}, {}
    for row in resp.rows:
        name   = row.dimension_values[0].value   # itemName
        period = row.dimension_values[1].value   # dateRange（自動附加）
        parsed = _parse([v.value for v in row.metric_values])
        if period == "date_range_0":
            curr_map[name] = parsed
        else:
            prev_map[name] = parsed

    all_names = sorted(
        set(curr_map) | set(prev_map),
        key=lambda n: curr_map.get(n, {}).get("revenue", 0),
        reverse=True,
    )[:limit]

    result = []
    for name in all_names:
        c = curr_map.get(name, {})
        p = prev_map.get(name, {})
        c_aov = round(c.get("revenue", 0) / c.get("purchases", 1), 0) if c.get("purchases", 0) > 0 else 0
        p_aov = round(p.get("revenue", 0) / p.get("purchases", 1), 0) if p.get("purchases", 0) > 0 else 0
        result.append({
            "name":          name,
            "purchases":     c.get("purchases", 0),
            "purchases_chg": _chg(c.get("purchases", 0), p.get("purchases")),
            "revenue":       c.get("revenue", 0),
            "revenue_chg":   _chg(c.get("revenue", 0), p.get("revenue")),
            "aov":           c_aov,
            "aov_chg":       _chg(c_aov, p_aov) if p_aov > 0 else None,
        })
    return result


def get_ga4_region_revenue(since, until, limit=15):
    """縣市收益分佈（單一期間，用於圓餅圖）"""
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        RunReportRequest, DateRange, Metric, Dimension, OrderBy,
    )
    client = BetaAnalyticsDataClient(credentials=_creds())
    req = RunReportRequest(
        property=f"properties/{GA4_PROPERTY_ID}",
        date_ranges=[DateRange(start_date=since, end_date=until)],
        dimensions=[Dimension(name="region")],
        metrics=[
            Metric(name="totalRevenue"),
            Metric(name="keyEvents"),
        ],
        order_bys=[OrderBy(
            metric=OrderBy.MetricOrderBy(metric_name="totalRevenue"),
            desc=True,
        )],
        limit=limit,
    )
    resp = client.run_report(req)
    result = []
    for row in resp.rows:
        region  = row.dimension_values[0].value
        revenue = round(float(row.metric_values[0].value), 0)
        events  = int(float(row.metric_values[1].value))
        if revenue > 0 and region not in ("(not set)", "", "(not provided)"):
            result.append({"region": region, "revenue": revenue, "key_events": events})
    return result


def get_ga4_data(since, until, compare_since, compare_until):
    summary, compare_summary = get_ga4_summary(since, until, compare_since, compare_until)
    try:
        traffic = get_ga4_traffic_sources(since, until, compare_since, compare_until)
    except Exception:
        traffic = []
    try:
        pages = get_ga4_pages(since, until, compare_since, compare_until)
    except Exception:
        pages = []
    try:
        products = get_ga4_products(since, until, compare_since, compare_until)
    except Exception:
        products = []
    try:
        regions = get_ga4_region_revenue(since, until)
    except Exception:
        regions = []
    return {
        "summary":         summary,
        "compare_summary": compare_summary,
        "traffic_sources": traffic,
        "pages":           pages,
        "products":        products,
        "regions":         regions,
    }
