from rtsw.shared import fetch_hourly_rtsw_json


def test_fetch_hourly_rtsw_json():
    results = fetch_hourly_rtsw_json()
    assert len(results) > 0
