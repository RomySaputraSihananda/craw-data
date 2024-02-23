import re
import requests

from json import loads, dumps

res = requests.get('https://api22-normal-useast1a.lemon8-app.com/api/550/search/stream?is_stream=1&search_tab=main&max_cursor=0&query=makanan&count=500&search_id&query_source=history&session_id=494bcb9b-836a-4327-90b4-33ceb1554d7f&session_first_search=0&last_click_gid=7305909228953420293&sar_card_last_pos=0&sar_card_display_part=0&questionnaire_card_skip_count=0&questionnaire_type=0&hasEverAppliedFilter=false&close_q_correct=0&search_from=history&search_time=1706436986669&dpi=420&resolution=1794*1080&aid=2657&app_id=2657&device_platform=android&device_type=unknown&brand=Genymotion&device_brand=Google&os=android&os_api=28&hevc_supported=1&os_version=9&tz_offset=-18000&tz_name=America%2FNew_York&sim_region=us&carrier_region=us&sys_region=US&mcc_mnc=310260&sim_oper=310270&sys_language=en&channel=gp&original_channel=gp&release_build=v5.5.0-gp-637b2f5c&version_code=550&app_version=5.5.0&update_version_code=55014&manifest_version_code=550&version_name=5.5.0&app_version_minor=5.5.0&youtube=1&cold_start=0&logo=topbuzz&iid=7327929081746474757&device_id=7327914106715145729&cdid=0c6539b5-9b39-4dec-998f-f4c2f1373532&openudid=9dd11b8d7ca37e80&gaid=00000000-0000-0000-0000-000000000000&region=us&real_region=us&language=en&ui_language=en&ac=wifi&latest_articles0=7305909228953420293&latest_articles1=7305946679012868613')

text = res.text


print(len(loads(re.findall(r'({"message":"success".*?,"result_status":\d})', text)[-1])['data']['items'][:-1]))
