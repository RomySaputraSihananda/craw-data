import json
import os
import requests
import time
from datetime import datetime
from playwright.sync_api import Playwright, sync_playwright, expect
from loguru import logger
import traceback


sekarang = datetime.now()
format_ymd_hms = sekarang.strftime("%Y-%m-%d %H:%M:%S")

def dpr():
    dapil_url = 'https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/pdpr/dapil_dpr.json'
    response = requests.get(dapil_url)
    response.raise_for_status()
    data = response.json()
    for datas in data:
        dapil = datas['nama']
        kode = datas['kode']
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.goto(f"https://pemilu2024.kpu.go.id/pilegdpr/hitung-suara/dapil/{kode}")
            vers = page.inner_text('//*[@id="main"]/div[3]/div[2]/div[2]/div[2]/div/div[2]/div[1]')
            progres_tps = vers.split('Progress: ')[-1].split(" dari ")[0]
            total_tps = vers.split('Progress: ')[-1].split(" dari ")[-1].split(' TPS ')[0]
            percent_tps = vers.split('Progress: ')[-1].split(" dari ")[-1].split(' TPS ')[-1].replace('(', '').replace(')',
                                                                                                                 '').replace(
                '%', '')

            context.close()
            browser.close()

        for i in range(1, 25):
            url_data_partai = 'https://sirekap-obj-data.kpu.go.id/pemilu/partai.json'
            response = requests.get(url_data_partai)
            response.raise_for_status()
            data_url_data_partai = response.json()
            one_data_url_data_partai = data_url_data_partai[f'{i}']

            nama_partai = one_data_url_data_partai['nama']
            no_urut = one_data_url_data_partai['nomor_urut']

            try:
                udpas = f'https://sirekap-obj-data.kpu.go.id/pemilu/caleg/partai/{kode}.json'
                response = requests.get(udpas)
                response.raise_for_status()
                data_udpas = response.json()
                data_caleg = data_udpas[f'{i}']


                udc = f'https://sirekap-obj-data.kpu.go.id/pemilu/hhcd/pdpr/{kode}.json'
                response = requests.get(udc)
                response.raise_for_status()
                data = response.json()

                les = data['ts']
                table_data = data['table']
                if table_data != None:
                    one_table_data = table_data[f'{i}']

                    total_suara = one_table_data['jml_suara_total']
                    jumlah_partai = one_table_data['jml_suara_partai']

                    calon_legislatif = []
                    for k, v in data_caleg.items():
                        if k in one_table_data:
                            total_suara_caleg = one_table_data[k]
                            caleg = {
                                'name_caleg': v['nama'],
                                'total_suara_caleg': total_suara_caleg,
                                'no_urut': v['nomor_urut'],
                                'jenis_kelamin': v['jenis_kelamin'],
                                'tempat_tinggal': v['tempat_tinggal']
                            }
                            calon_legislatif.append(caleg)

                    hasil = {
                        "domain": "pemilu2024.kpu.go.id",
                        "link": f"https://pemilu2024.kpu.go.id/pilegdpr/hitung-suara",
                        "tag": [
                            "pemilu2024",
                            "kpu.go.id",
                            "pileg dpr"
                          ],
                        'dapil': dapil,
                        'partai': nama_partai,
                        'no_urut_partai': no_urut,
                        'jml_suara_partai': jumlah_partai,
                        'jml_suara_total': total_suara,
                        'calon_legislatif': calon_legislatif,
                        'version': les,
                        'progres_tps': int(progres_tps),
                        'total_tps': int(total_tps),
                        'total_tps_(%)': float(percent_tps),
                        "crawling_time": format_ymd_hms,
                        "crawling_time_epoch": int(time.time()),
                        "detail": {
                            "psu": "Reguler",
                            "persen": float(percent_tps),
                            "status_progress": True
                        }
                    }
                    print(hasil)

                else:
                    hasil = {
                        "domain": "pemilu2024.kpu.go.id",
                        "link": f"https://pemilu2024.kpu.go.id/pilegdpr/hitung-suara",
                        "tag": [
                            "pemilu2024",
                            "kpu.go.id",
                            "pileg dpr"
                        ],
                        'dapil': dapil,
                        'partai': nama_partai,
                        'no_urut_partai': no_urut,
                        'version': les,
                        'progres_tps': int(progres_tps),
                        'total_tps': int(total_tps),
                        'total_tps_(%)': float(percent_tps),
                        "crawling_time": format_ymd_hms,
                        "crawling_time_epoch": int(time.time()),
                        "detail": {
                            "psu": "Reguler",
                            "persen": 0,
                            "status_progress": False
                        }
                    }
                    print(hasil)
            except:
                continue

if __name__ == "__main__":
    dpr()
