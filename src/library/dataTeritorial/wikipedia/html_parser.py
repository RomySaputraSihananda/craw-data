__author__ = 'Gumilar Ganjar Permana'

import re
from datetime import datetime
from bs4 import BeautifulSoup

class HTMLParser:
    def __init__(self, base_url=None):
        pass

    def bs4_parser(self, html, selector):
        result = None
        try:
            html = BeautifulSoup(html, 'lxml')
            result = html.select(selector)
        except Exception as e:
            print(e)
        finally:
            return result

    def get_url_list(self, page_source):
        result = []
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            data = soup.find_all('div', class_='alert_item')
            for item in data:
                event_name = ' '.join((re.sub(r'\r?\n', '', item.text.strip())).split())
                a_class = item.find_all('a', href=True)
                url_ = a_class[0].get('href')
                event_item = {'event_name': event_name,
                            'url': url_}
                result.append(event_item)
        except Exception as e:
            print(e)
        return result

    def get_alert_detail(self, page_source):
        result = []
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            summary_container = soup.find('table', class_='summary')
            if summary_container is not None:
                rows = summary_container.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    field_name = cols[0].text
                    if cols[1].find('span'):
                        span_text = (cols[1].find('span')).text
                        cols[1].span.decompose()
                        col_text = cols[1].text
                        col_value = '{}{}'.format(col_text, span_text)
                    else:
                        col_value = cols[1].get_text(strip=True, separator='\n')

                    if 'more info' in field_name.lower():
                        a_class = cols[1].find_all('a', href=True)
                        info_url = a_class[0].get('href')
                        info_source = cols[1].get_text(strip=True, separator='\n')
                        field_value = {'info_url': info_url,
                                       'info_source': info_source}
                    else:
                        field_value = col_value
                    row_data = {'field_name': field_name,
                                'field_value': field_value}
                    result.append(row_data)

            if soup.find('tbody', id='tableScoreMain'):
                score_container = soup.find('tbody', id='tableScoreMain')
            else:
                score_container = soup.find('tbody', id='main_sources')

            if score_container is not None:
                score_list = []
                rows = score_container.find_all('tr')
                rows.pop(0)
                for row in rows:
                    cols = row.find_all('td')
                    score_source = cols[0].text
                    score_value = cols[len(cols)-1].text
                    score = {'score_source': score_source,
                             'score_value': score_value}
                    score_list.append(score)
                gdac_score = {'field_name': 'gdacs_score',
                              'field_value': score_list}
                result.append(gdac_score)
        except Exception as e:
            print(e)
        return result

    def get_rsoe_event_list(self, page_source):
        result = []
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            categories = soup.find_all('div', class_='category-section')
            for event_category in categories:
                category = event_category.find('h3').text
                event_item_container = event_category.find_all('div', class_='event-card')
                for item in event_item_container:
                    event_title = item.find('h5')
                    event_date = item.find('td', class_='eventDate').get_text(strip=True, separator='\n')
                    event_location = item.find('td', class_='location').get_text(strip=True, separator='\n')
                    detail_container = item.find('td', class_='details')
                    a_class = detail_container.find('a', href=True)
                    event_url = a_class.get('href')
                    event_detail = {
                        'event_category': category,
                        'title': event_title,
                        'date': event_date,
                        'country': event_location,
                        'detail_url': event_url,
                    }
                    result.append(event_detail)
        except Exception as e:
            print(e)
        return result

    def get_gfp_url_list(self, page_source):
        result = []
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            url_list = soup.find('aside')
            a_class = url_list.find_all('a', href=True, title=True)
            for item in a_class:
                url = item.get('href')
                title = item.get('title')
                text = item.find('span').get_text(strip=True, separator='\n')
                item_detail = {
                    'url': url,
                    'title': title,
                    'text': text
                }
                result.append(item_detail)
        except Exception as e:
            print(e)
        return result

    def get_gfp_data(self, page_source):
        result = []
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            if soup.find('div', class_='mainBlockContainer'):
                container = soup.find_all('div', class_='mainBlockContainer')
                for item in container:
                    country = item.find('span', class_='textLarge').get_text(strip=True, separator='\n')
                    date_container = item.find_all('span', class_='textNormal')
                    if len(date_container)>1:
                        date = date_container[1].get_text(strip=True, separator='\n')
                    else:
                        date = date_container[0].get_text(strip=True, separator='\n')
                    data = {
                        'country_name': country,
                        'join_date': date
                    }
                    result.append(data)
            elif soup.find('div', class_='mainLists'):
                container = soup.find_all('div', class_='mainLists')
                for item in container:
                    year = item.find('span', class_='textLarger').get_text(strip=True, separator='\n')
                    rank_list = []
                    country_holder = item.find_all('div', class_='countryHolder')
                    for country in country_holder:
                        country_name = country.find('div', class_='countryName').get_text(strip=True, separator='\n')
                        rank = country.find('div', class_='rnkNum').get_text(strip=True, separator='\n')
                        country_rank = {
                            'country_name': country_name,
                            'rank': rank
                        }
                        rank_list.append(country_rank)
                    data = {
                        'year': year,
                        'rank': rank_list
                    }
                    result.append(data)
            elif soup.find('div', class_='recordsetContainer'):
                container = soup.find_all('div', class_='recordsetContainer')
                for item in container:
                    if item.find('div', class_='barGraphContainer'):
                        country = item.find('div', class_='longFormName').get_text(strip=True, separator='\n')
                        short_name = item.find('div', class_='shortFormName').get_text(strip=True, separator='\n')
                        rank = item.find('div', class_='rankNumContainer').get_text(strip=True, separator='\n')
                        value_text = item.find('div', class_='valueContainer').get_text(strip=True, separator='\n')
                        value_text = value_text.replace('\t', '')
                        value_text.split()
                        value = " ".join(value_text.split())
                        data = {
                            'rank': rank,
                            'country_name': country,
                            'country_name_short': short_name,
                            'value': value
                        }
                        result.append(data)
                    else:
                        country = item.find('div', class_='longFormName').get_text(strip=True, separator='\n')
                        short_name = item.find('div', class_='shortFormName').get_text(strip=True, separator='\n')
                        rank = item.find('div', class_='rankNumContainer').get_text(strip=True, separator='\n')
                        power_index = item.find('div', class_='pwrIndxContainer').get_text(strip=True, separator='\n')
                        power_index = power_index.replace('PwrIndx Score: ', '')
                        data = {
                            'rank': rank,
                            'country_name': country,
                            'country_name_short': short_name,
                            'power_index': power_index
                        }
                        result.append(data)
            else:
                print('Different Page Format!!!')
        except Exception as e:
            print(e)
        return result

    def get_global_edge_country_list(self, page_source):
        result = []
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            country_container = soup.find('select', id='countries')
            country_list = country_container.find_all('option')
            country_list.pop(0)
            for item in country_list:
                country_id = item['value']
                country_name = (item.get_text(strip=True, separator='\n'))
                country_detail = {
                    'id': country_id,
                    'country_name': country_name
                }
                result.append(country_detail)
        except Exception as e:
            print(e)
        return result

    def get_global_edge_organization_list(self, page_source):
        result = []
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            organization_container = soup.find('ul', id='organization-list')
            organization_list = organization_container.find_all('li')
            for item in organization_list:
                organization_name = item.get_text(strip=True, separator='\n')
                result.append(organization_name)
        except Exception as e:
            print(e)
        return result

    def get_uis_unesco_data(self, page_source):
        result = {}
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            country_name = (soup.find('h2', id='countryInfo')).get_text(strip=True, separator='\n')
            origin_container = soup.find('div', id='orgCountriesList')
            destination_container = soup.find('div', id='dstCountriesList')
            indicator_container = soup.find('div', id='mainIndicators')

            origin = []
            try:
                origin_list = origin_container.find_all('tr')
                for origin_item in origin_list:
                    origin_row = origin_item.find_all('td')
                    origin_country = origin_row[0].get_text(strip=True, separator='\n')
                    origin_count = origin_row[1].get_text(strip=True, separator='\n')
                    origin_data = {
                        'origin_country': origin_country,
                        'origin_count': origin_count
                    }
                    origin.append(origin_data)
            except:
                pass

            destination = []
            try:
                destination_list = destination_container.find_all('tr')
                for destination_item in destination_list:
                    destination_row = destination_item.find_all('td')
                    destination_country = destination_row[0].get_text(strip=True, separator='\n')
                    destination_count = destination_row[1].get_text(strip=True, separator='\n')
                    destination_data = {
                        'destination_country': destination_country,
                        'destination_count': destination_count
                    }
                    destination.append(destination_data)
            except:
                pass

            indicator = []
            try:
                indicator_list = indicator_container.find_all('tr')
                for indicator_item in indicator_list:
                    indicator_row = indicator_item.find_all('td')
                    indicator_country = indicator_row[0].get_text(strip=True, separator='\n')
                    indicator_count = indicator_row[1].get_text(strip=True, separator='\n')
                    indicator_data = {
                        'indicator': indicator_country,
                        'indicator_count': indicator_count
                    }
                    indicator.append(indicator_data)
            except:
                pass

            country_data = {
                'country': country_name,
                'country_of_origin': origin,
                'destination_country': destination,
                'key_indicator': indicator
            }
            result = country_data
        except Exception as e:
            print(e)
        return result

    def get_wikiwand_data(self, page_source):
        result = {}
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            media = []
            article_container = soup.find('ul', id='article_content_wrapper')
            title_container = soup.find('section', class_='title_wrapper')
            title = (title_container.find('h1')).get_text(strip=True, separator='\n')
            content_container = soup.find('div', id='fullContent')
            sections = content_container.find('section')
            imege_source = content_container.find_all('img')
            for image in imege_source:
                image_item = {
                    'type': 'image',
                    'url': image['src']
                }
                media.append(image_item)
            print('done')
        except Exception as e:
            print(e)
        return result

    def get_ddi_data(self, page_source):
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            table_container = soup.find('section', class_='table')
            table_header = table_container.find('div', class_='table__header')
            table_rows = table_container.find_all('article', class_='row')
            last_update = table_header.find('div', class_='table__header__date').get_text(strip=True, separator='\n')
            last_update = last_update.replace('Last updated: ', '')
            header_field = table_header.find_all('div', class_='table__header__cell')

            field_names = []
            for item in header_field:
                field = (item.get_text(strip=True, separator='\n')).lower()
                field = field.replace(' ', '_')
                field_names.append(field)

            data_rows = []
            for row in table_rows:
                rank = row.find('p', class_='row__main__ranking').get_text(strip=True, separator='\n')
                country = row.find('p', class_='row__main__country__name').get_text(strip=True, separator='\n')
                field_value = row.find_all('div', class_='row__cell row__cell--desktop')
                value_list = []
                for field in field_value:
                    value = field.get_text(strip=True, separator='\n')
                    value_list.append(value)
                row_data = {
                    'rank': rank,
                    'country': country,
                    'values': value_list
                }
                data_rows.append(row_data)

            result = {
                'last_update': last_update,
                'field_names': field_names,
                'rows': data_rows
            }
            return result
        except Exception as e:
            print(e)

    def get_witz_data(self, page_source):
        soup = BeautifulSoup(page_source, 'html.parser')
        result = []
        try:
            table_header = soup.find('thead')
            header_field = table_header.find_all('th')
            table_body = soup.find('div', id='DataDiv')
            table_rows = table_body.find_all('tr')

            field_names = []
            for item in header_field:
                field = (item.get_text(strip=True, separator='\n')).lower()
                field = field.replace(' ', '_')
                field_names.append(field)
            for row in table_rows:
                row_content = row.find_all('td')
                a_class = row_content[7].find('a', href=True)
                try:
                    pdf_url = a_class['href']
                    if pdf_url == '#':
                        onclick = a_class['onclick']
                        onclick = re.sub(r'.+\(', '', onclick)
                        onclick = re.sub(r'\).+', '', onclick)
                        pdf_url = int(onclick)
                except:
                    pdf_url = None
                data = {
                    field_names[0]: row_content[0].get_text(strip=True, separator='\n'),
                    field_names[1]: row_content[1].get_text(strip=True, separator='\n'),
                    field_names[2]: row_content[2].get_text(strip=True, separator='\n'),
                    field_names[3]: row_content[3].get_text(strip=True, separator='\n'),
                    field_names[4]: row_content[4].get_text(strip=True, separator='\n'),
                    field_names[5]: row_content[5].get_text(strip=True, separator='\n'),
                    field_names[6]: row_content[6].get_text(strip=True, separator='\n'),
                    field_names[7]: pdf_url
                }
                result.append(data)
            return result
        except Exception as e:
            print(e)

    def get_witz_pdf(self, page_source):
        soup = BeautifulSoup(page_source, 'html.parser')
        result = []
        try:
            a_class = soup.find_all('a', href=True)
            for item in a_class:
                pdf_url = item['href']
                result.append(pdf_url)
            return result
        except Exception as e:
            print(e)

    def get_distance_country_list_url(self, page_source):
        result = []
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            tables = soup.find_all('table')
            content_table = tables[1]
            table_rows = content_table.find_all('tr')
            for row in table_rows:
                try:
                    row_urls = row.find_all('a', href=True)
                    if len(row_urls) > 0:
                        url = row_urls[0]['href']
                        result.append(url)
                except:
                    pass
        except Exception as e:
            print(e)
        return result

    def get_distance_country_detail(self, page_source):
        result = []
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            tables = soup.find_all('table')
            content_table = tables[1]
            table_rows = content_table.find_all('tr')
            for row in table_rows:
                try:
                    row_fields = row.find_all('td')
                    if len(row_fields) > 1:
                        country = row_fields[0].get_text(strip=True, separator='\n')
                        city = row_fields[1].get_text(strip=True, separator='\n')
                        detail = {
                            'country': country,
                            'city': city
                        }
                        result.append(detail)
                except:
                    pass
        except Exception as e:
            print(e)
        return result

    def get_numbeo_date_list(self, page_source):
        result = []
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            select_container = soup.find('select', {"name": "title"})
            option_list = select_container.find_all('option')
            for item in option_list:
                date = item['value']
                result.append(date)
        except Exception as e:
            print(e)
        return result

    def get_numbeo_rank_list(self, page_source, date_time):
        result = []
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            rank = 1
            table = soup.find('table', id='t2')
            table_body = table.find('tbody')
            rows = table_body.find_all('tr')
            for item in rows:
                cols = item.find_all('td')
                row_data = {
                    'date_time': date_time,
                    'rank': rank,
                    'country': cols[1].get_text(strip=True, separator='\n'),
                    'pollution_score': cols[2].get_text(strip=True, separator='\n'),
                    'exp_pollution_score': cols[3].get_text(strip=True, separator='\n'),
                }
                result.append(row_data)
                rank += 1
        except Exception as e:
            print(e)
        return result

    def get_inaexport_inqueris_data(self, page_source):
        result = []
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            card_list = soup.find_all('div', class_='card-body')
            for card in card_list:
                title = card.find('p', class_='title-event').get_text(strip=True, separator='\n')
                rows = card.find_all('tr')
                date_fields = rows[0].find_all('td')
                date = date_fields[3].get_text(strip=True, separator='\n')
                buyer_fields = rows[1].find_all('td')
                buyer = buyer_fields[3].get_text(strip=True, separator='\n')
                product_fields = rows[2].find_all('td')
                product = product_fields[3].get_text(strip=True, separator='\n')
                order_fields = rows[3].find_all('td')
                order = order_fields[3].get_text(strip=True, separator='\n')
                active_fields = rows[4].find_all('td')
                active = active_fields[3].get_text(strip=True, separator='\n')
                download_fields = rows[5].find_all('td')
                download = download_fields[3].get_text(strip=True, separator='\n')

                card_detail = {
                    'product': title,
                    'detail_product': {
                        'date': date,
                        'buyer_from': buyer,
                        'product_name': product,
                        'qyt_order': order,
                        'active_period': active,
                        'download_by': download
                    }
                }
                result.append(card_detail)
        except Exception as e:
            print(e)
        finally:
            return result

    def get_inaexport_supplier_list(self, page_source):
        result = []
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            card_list = soup.find_all('div', class_='single_product')
            for card in card_list:
                detail_container = card.find('div', class_='eksporter-detail')
                a_class = detail_container.find_all('a', href=True)
                url_ = a_class[0].get('href')
                url_ = re.sub(r'\s', '%20', url_)
                result.append(url_)
        except Exception as e:
            print(e)
        finally:
            return result

    def get_inaexport_supplier_product_detail(self, page_source):
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            images_container = soup.find_all('a', class_='elevatezoom-gallery')
            image_list = []
            for image in images_container:
                image_url = image.find('img')['src']
                image_list.append(image_url)
            detail_container = soup.find('div', class_='product_d_right')
            product_name = detail_container.find('h1').get_text(strip=True, separator='\n')
            variant_container = detail_container.find('div', class_='product_variant')
            variant_labels = variant_container.find_all('label')
            min_order = variant_labels[1].get_text(strip=True, separator='\n')
            international_commercial_terms = variant_labels[3].get_text(strip=True, separator='\n')
            product_description = soup.find('div', class_='product_info_content').get_text(strip=True, separator='\n')
            specification_container = soup.find('div', class_='product_d_table')
            rows = specification_container.find_all('tr')
            specification_data = {}
            for row in rows:
                td = row.find_all('td')
                spec_field_name = td[0].get_text(strip=True, separator='\n')
                spec_field_name = spec_field_name.lower()
                spec_field_name = re.sub(r'\s', '_', spec_field_name)
                spec_field_name = re.sub(r'\(', '', spec_field_name)
                spec_field_name = re.sub(r'\)', '', spec_field_name)
                spec_field_value = td[1].get_text(strip=True, separator='\n')
                specification_data.update({spec_field_name: spec_field_value})
            product_detail = {
                'product_name': product_name,
                'product_images': image_list,
                'min_order': min_order,
                'international_commercial_terms': international_commercial_terms,
                'description': product_description,
                'specification': specification_data,
            }
            return product_detail
        except Exception as e:
            print(e)

    def get_inaexport_supplier_product_list(self, page_source):
        result = []
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            a_class = soup.find_all('a', href=True, class_='primary_img')
            for item in a_class:
                url_ = item.get('href')
                result.append(url_)
        except Exception as e:
            print(e)
        finally:
            return result

    def get_inaexport_supplier_detail(self, page_source):
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            shop_area = soup.find_all('div', class_='shop_area')
            container = shop_area[0].find_all('div', class_='container')
            company_logo = (container[0].find('img', class_='eksporter_img'))['src']
            company_name = (container[0].find_all('h3'))[0].get_text(strip=True, separator='\n')
            company_address1 = (container[0].find_all('h5'))[0].get_text(strip=True, separator='\n')
            company_address2 = (container[0].find_all('h5'))[1].get_text(strip=True, separator='\n')
            company_address = '{} {}'.format(company_address1, company_address2)
            detail_container = container[0].find('div', id='myTabContent')
            detail_cards = detail_container.find_all('div', class_='card-body')
            about_us = {}
            for card in detail_cards:
                try:
                    card_title = card.find('h4', class_='namecompany').get_text(strip=True, separator='\n')
                except:
                    card_title = ''

                if card_title == 'COMPANY PROFILE':
                    company_profile = {}
                    rows = card.find_all('div', class_='row')
                    for row in rows:
                        fields = row.find_all('div')
                        field_title = fields[0].get_text(strip=True, separator='\n')
                        field_title = field_title.lower()
                        field_title = re.sub(r'\s', '_', field_title)
                        field_content = fields[len(fields)-1].get_text(strip=True, separator='\n')
                        field_content = re.sub(r'^:', '', field_content)
                        field_content = field_content.strip()
                        field_content = " ".join(field_content.split())
                        company_profile.update({field_title: field_content})
                    about_us.update({'company_profile': company_profile})
                elif card_title == 'TRADE CAPACITY':
                    trade_capacity = {}
                    rows = card.find_all('div', class_='row')
                    for row in rows:
                        fields = row.find_all('div')
                        field_title = fields[0].get_text(strip=True, separator='\n')
                        field_title = field_title.lower()
                        field_title = re.sub(r'\s', '_', field_title)
                        field_content = fields[len(fields)-1].get_text(strip=True, separator='\n')
                        field_content = re.sub(r'^:', '', field_content)
                        field_content = field_content.strip()
                        field_content = " ".join(field_content.split())
                        trade_capacity.update({field_title: field_content})
                    about_us.update({'trade_capacity': trade_capacity})
                elif card_title == 'PRODUCTION CAPACITY':
                    production_capacity = {}
                    rows = card.find_all('div', class_='row')
                    for row in rows:
                        fields = row.find_all('div')
                        field_title = fields[0].get_text(strip=True, separator='\n')
                        field_title = field_title.lower()
                        field_title = re.sub(r'\s', '_', field_title)
                        field_content = fields[len(fields)-1].get_text(strip=True, separator='\n')
                        field_content = re.sub(r'^:', '', field_content)
                        field_content = field_content.strip()
                        field_content = " ".join(field_content.split())
                        production_capacity.update({field_title: field_content})
                    about_us.update({'production_capacity': production_capacity})
                elif card_title == 'CERTIFICATE':
                    certificate = []
                    certificate_list = card.find_all('img')
                    for img in certificate_list:
                        url_img = img['src']
                        certificate.append(url_img)
                    about_us.update({'certificate': certificate})
            supplier_detail = {
                'company_logo': company_logo,
                'company_name': company_name,
                'company_address': company_address,
                'about_us': about_us
            }
            return supplier_detail
        except Exception as e:
            print(e)

    def get_global_economy_indicator_list(self, page_source):
        result = []
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            indicator_list = soup.find_all('div', class_='indicatorRow')
            for indicator in indicator_list:
                indicator_type = indicator.find('div', class_='indicatorsType').get_text(strip=True, separator='\n')
                if indicator_type == 'annual':
                    container = indicator.find('div', class_='indicatorsName')
                    indicator_name =container.get_text(strip=True, separator='\n')
                    a_class = container.find_all('a', href=True)
                    url_ = a_class[0].get('href')
                    indicator_item = {
                        'indicator_name': indicator_name,
                        'indicator_url': url_
                    }
                    result.append(indicator_item)
        except Exception as e:
            print(e)
        finally:
            return result

    def get_global_economy_indicator_data(self, page_source):
        result = []
        soup = BeautifulSoup(page_source, 'html.parser')
        selected = soup.find_all('option', selected=True)
        year = selected[0].get_text(strip=True, separator='\n')
        try:
            table = soup.find('table', id='benchmarkTable')
            table_body = table.find('tbody')
            rows = table_body.find_all('tr')
            for row in rows:
                fields = row.find_all('td')
                country = fields[0].get_text(strip=True, separator='\n')
                value = fields[1].get_text(strip=True, separator='\n')
                rank = fields[2].get_text(strip=True, separator='\n')
                available_data = fields[3].get_text(strip=True, separator='\n')
                row_data = {
                    'country': country,
                    'value': value,
                    'rank': rank,
                    'available_data': available_data
                }
                result.append(row_data)
        except Exception as e:
            print(e)
        finally:
            return result, year

    def get_bmkg_prov_url(self, page_source):
        result = []
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            prov_containers = soup.find('div', class_='list-cuaca-provinsi')
            a_class = prov_containers.find_all('a', href=True)
            for item in a_class:
                url_ = item.get('href')
                result.append(url_)
            return result
        except Exception as e:
            print(e)

    def get_bmkg_kec_url(self, page_source):
        result = []
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            kec_containers = soup.find('select', class_='chosen-select')
            kec_option = kec_containers.find_all('option')
            for item in kec_option:
                try:
                    url_ = item['value']
                    result.append(url_)
                except:pass
            return result
        except Exception as e:
            print(e)

    def get_bmkg_weather_detail(self, page_source):
        result = []
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            tabs_container = soup.find('ul', class_='nav-tabs')
            tabs = tabs_container.find_all('li')
            for tab in tabs:
                day_list = []
                date = tab.get_text(strip=True, separator='\n')
                a_class = tab.find('a', href=True)
                panel_name = a_class.get('href')
                panel_name = re.sub(r'#', '', panel_name)
                weather_container = soup.find('div', id=panel_name)
                weather_card = weather_container.find_all('div', class_='cuaca-flex-child')
                for card in weather_card:
                    time = card.find('h2', class_='kota').get_text(strip=True, separator='\n')
                    weather = card.find('div', class_='kiri').get_text(strip=True, separator='\n')
                    detail_container = card.find('div', class_='kanan')
                    temperature = detail_container.find('h2').get_text(strip=True, separator='\n')
                    sub_detail = detail_container.find_all('p')
                    raindrop = sub_detail[0].get_text(strip=True, separator='\n')
                    wind = (sub_detail[1].get_text(strip=True, separator='\n')).split('\n')
                    wind_speed = wind[0]
                    wind_direction = wind[1]
                    weather_detail = {
                        'time': time,
                        'weather': weather,
                        'temperature': temperature,
                        'raindrop': raindrop,
                        'wind_speed': wind_speed,
                        'wind_direction': wind_direction,
                    }
                    day_list.append(weather_detail)

                day_weather = {
                    'date': date,
                    'weather_list': day_list
                }
                result.append(day_weather)
            return result
        except Exception as e:
            print(e)

    def get_wiki_profile_detail(self, page_source):
        detail = {}
        relasi = {}
        url_list = []
        relation_check = ['suami', 'anak', 'orang_tua', 'hubungan']
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            profile_containers = soup.find('table', class_='infobox')
            rows = profile_containers.find_all('tr')
            for row in rows:
                try:
                    field_name_container = row.find('th')
                    field_content_container = row.find('td')
                    if field_name_container and field_content_container is not None:
                        field_name = field_name_container.get_text(strip=True, separator='\n')
                        field_name = (re.sub(r' ', '_', field_name)).lower()
                        if field_name == 'tanda_tangan':
                            img_container = field_content_container.find('img')
                            field_content = img_container['src']
                        elif (field_name == 'website') or (field_name == 'situs_web'):
                            web_name = field_content_container.get_text(strip=True, separator='\n')
                            a_class = field_content_container.find('a', href=True)
                            url_ = a_class.get('href')
                            field_content ={
                                'website_name': web_name,
                                'url': url_
                            }
                        else:
                            content_list = field_content_container.find_all('li')
                            if len(content_list) > 0:
                                field_content = []
                                for item in content_list:
                                    item_content = item.get_text(strip=True, separator='\n')
                                    item_content = (re.sub(r'\n\(', '(', item_content))
                                    item_content = (re.sub(r'\(\n', '(', item_content))
                                    item_content = (re.sub(r'\n\)', ')', item_content))
                                    item_content = (re.sub(r'(\n)?\[.*\](\n)?', '', item_content))
                                    item_content = (re.sub(r'\n\,', ',', item_content))
                                    field_content.append(item_content)
                                    a_class = item.find_all('a', href=True)
                                    for url_tag in a_class:
                                        url_ = url_tag.get('href')
                                        if 'wiki/' in url_:
                                            url_list.append(url_)
                            else:
                                field_content = field_content_container.get_text(strip=True, separator='\n')
                                field_content = (re.sub(r'\n\(', '(', field_content))
                                field_content = (re.sub(r'\(\n', '(', field_content))
                                field_content = (re.sub(r'\n\)', ')', field_content))
                                field_content = (re.sub(r'(\n)?\[.*\](\n)?', '', field_content))
                                field_content = (re.sub(r'\n\,', ',', field_content))
                                if '\n' in field_content:
                                    field_content = field_content.split('\n')
                                a_class = field_content_container.find_all('a', href=True)
                                for url_tag in a_class:
                                    url_ = url_tag.get('href')
                                    if 'wiki/' in url_:
                                        url_list.append(url_)
                        detail.update({
                            field_name: field_content
                        })
                        for relation in relation_check:
                            if relation in field_name:
                                relasi.update({
                                    field_name: field_content
                                })
                except Exception as e:
                    print(e)
                    pass
            return detail, url_list, relasi
        except Exception as e:
            print(e)

    def get_magma_esdm_event_url(self, page_source):
        result = []
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            event_containers = soup.find_all('div', class_='timeline-item')
            for event in event_containers:
                a_class = event.find_all('a', href=True)
                for item in a_class:
                    item_text = item.get_text(strip=True, separator='\n')
                    item_text = re.sub(r'\s', '_', item_text)
                    if item_text.lower() == 'lihat_detail':
                        url_ = item.get('href')
                        result.append(url_)
            return result
        except Exception as e:
            print(e)

    def get_magma_esdm_event_gempa_detail(self, page_source):
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            titles = []
            card_body = soup.find('div', class_='card-body')
            wilayah = card_body.find('h5', class_='card-title').get_text(strip=True, separator='\n')
            subtitle = card_body.find('p', class_='card-subtitle')
            pelapor = subtitle.find('a').get_text(strip=True, separator='\n')
            date_time = subtitle.find('span').get_text(strip=True, separator='\n')
            date_time = re.sub(r', ', '', date_time)
            intensitas_gempa = card_body.find('p', class_='blog-text').get_text(strip=True, separator='\n')

            card_texts = card_body.find_all('p', class_='card-text')
            gempa_detail = card_texts[0].find_all('span', class_='badge')
            magnitudo = gempa_detail[0].get_text(strip=True, separator='\n')
            potensi = gempa_detail[1].get_text(strip=True, separator='\n')

            result = {
                'type': 'Gempa Bumi',
                'wilayah': wilayah,
                'pelapor': pelapor,
                'date_time': date_time,
                'magnitudo': magnitudo,
                'potensi': potensi,
                'intensitas_gempa': intensitas_gempa
            }

            card_titles = card_body.find_all('label', class_='slim-card-title')
            for card_title in card_titles:
                title = card_title.get_text(strip=True, separator='\n')
                title = re.sub(r'\s', '_', title)
                titles.append(title.lower())

            card_index = 1
            for dest_title in titles:
                result.update({
                    dest_title: card_texts[card_index].get_text(strip=True, separator='\n')
                })
                card_index += 1

            lokasi_waktu = result['lokasi_dan_waktu_kejadian']
            koordinat = re.sub(r'.*pada koordinat ', '', lokasi_waktu)
            koordinat = re.sub(r',? berjarak sekitar.*', '', koordinat)
            koordinat = re.sub(r',? dengan magnitudo.*', '', koordinat)
            koordinat = koordinat.split(' dan ')
            lattitude = 0
            longitude = 0
            for item in koordinat:
                koordinat_item = item.split(' ')
                koordinat_value = koordinat_item[0]
                koordinat_value = re.sub(r',', '.', koordinat_value)
                koordinat_value = re.sub(r'\N{DEGREE SIGN}', '', koordinat_value)
                koordinat_value = float(koordinat_value)
                if koordinat_item[1].lower() == 'lu':
                    lattitude = koordinat_value
                elif koordinat_item[1].lower() == 'ls':
                    lattitude = -abs(koordinat_value)
                elif koordinat_item[1].lower() == 'bt':
                    longitude = koordinat_value
                elif koordinat_item[1].lower() == 'bb':
                    longitude = -abs(koordinat_value)
            result.update({
                'koordinat': {"coordinates": [longitude, lattitude],
                              "type": "Point"}
            })

            kedalaman = re.sub(r'.*pada kedalaman ', '', lokasi_waktu)
            kedalaman = re.sub(r'\..*', '', kedalaman)
            result.update({
                'kedalaman': kedalaman
            })
            return result
        except Exception as e:
            print(e)

    def get_magma_esdm_event_gerakan_tanah_detail(self, page_source):
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            first_card_titles = []
            cards = soup.find_all('div', class_='card')
            title = cards[0].find('h3').get_text(strip=True, separator='\n')
            subtitle = cards[0].find('p', class_='tx-12')
            pelapor = subtitle.find('a').get_text(strip=True, separator='\n')
            date_time = subtitle.find('span').get_text(strip=True, separator='\n')
            date_time = re.sub(r', ', '', date_time)
            result = {
                'type': 'Gerakan Tanah',
                'title': title,
                'pelapor': pelapor,
                'date_time': date_time
            }

            first_card_conents = cards[0].find_all('p')
            first_card_title_container = cards[0].find_all('h6', class_='slim-card-title')
            for first_card_title_item in first_card_title_container:
                first_cars_item_title = first_card_title_item.get_text(strip=True, separator='\n')
                first_cars_item_title = re.sub(r'\s', '_', first_cars_item_title)
                first_card_titles.append(first_cars_item_title.lower())
            first_card_index = 1
            for first_card_title in first_card_titles:
                if 'foto' in first_card_title:
                    image_url_list = []
                    image_container = cards[0].find('div', class_='carousel')
                    image_items = image_container.find_all('img')
                    for image in image_items:
                        image_url_list.append(image['src'])
                    result.update({
                        first_card_title: image_url_list
                    })
                else:
                    result.update({
                        first_card_title: first_card_conents[first_card_index].get_text(strip=True, separator='\n')
                    })
                first_card_index += 1

            second_card_tables = cards[1].find_all('dl', class_='row')
            for table in second_card_tables:
                field_index = 0
                field_name_container = table.find_all('dt')
                field_value_container = table.find_all('dd')
                for field_row in field_name_container:
                    field_name = field_row.get_text(strip=True, separator='\n')
                    field_name = (re.sub(r'\s', '_', field_name)).lower()
                    field_value = field_value_container[field_index].get_text(strip=True, separator='\n')
                    result.update({
                        field_name: field_value
                    })
                    field_index += 1

            second_card_divs = cards[1].find_all('div')
            if len(second_card_divs) > 0:
                for div in second_card_divs:
                    div_content = div.get_text(strip=True, separator='\n')
                    if 'Anggota Tim' in div_content:
                        anggota_tim = (re.sub(r'\t', '', div_content)).split('\n')
                        anggota_tim.pop(0)
                        result.update({
                            'anggota_tim': anggota_tim
                        })
                    elif div_content == '':
                        pass
                    else:
                        faktor_penyebab_gerakan_tanah = div_content.split('\n')
                        result.update({
                            'faktor_penyebab_gerakan_tanah': faktor_penyebab_gerakan_tanah
                        })
            return result
        except Exception as e:
            print(e)

    def get_magma_esdm_event_gunung_api_detail(self, page_source):
        result = {}
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            header_container = soup.find('div', class_='card-body')
            content_container = soup.find('div', class_='card-columns')

            level = header_container.find('span', class_='badge').get_text(strip=True, separator='\n')
            pelapor = header_container.find('p', class_='card-subtitle').get_text(strip=True, separator='\n')
            pelapor = re.sub(r'Dibuat oleh, ', '', pelapor)

            title = header_container.find('h5', class_='card-title').get_text(strip=True, separator='\n').split(',')
            nama_gunung = title[0]
            event_date = title[1].split('-')
            day = event_date[0]
            date = event_date[1]
            periode = title[2]
            periode = re.sub(r'periode ', '', periode)

            subtitle = header_container.find_all('p')
            lokasi = (subtitle[1].get_text(strip=True, separator='\n'))

            image_container = content_container.find('img', class_='img-fluid')
            image_url = image_container['src']

            result.update({
                'type': 'Gunung Api',
                'level': level,
                'nama_gunung': nama_gunung,
                'day': day,
                'data_time': date,
                'periode': periode,
                'lokasi_administratif_geografis': lokasi,
                'pelapor': pelapor,
                'image': image_url
            })

            detail_cards = content_container.find_all('div', class_='media-body')
            detail_list = []
            for card in detail_cards:
                card_title = card.find('h6', class_='slim-card-title').get_text(strip=True, separator='\n')
                card_title = (re.sub(r'\s', '_', card_title)).lower()
                card_content = []
                contents = card.find_all('p')
                if len(contents) == 1:
                    detail_list.append({
                        'card_title': card_title,
                        'card_content': contents[0].get_text(strip=True, separator='\n')
                    })
                else:
                    for content in contents:
                        card_content.append(content.get_text(strip=True, separator='\n'))
                    detail_list.append({
                        'card_title': card_title,
                        'card_content': card_content
                    })

            for detail in detail_list:
                result.update({
                    detail['card_title']: detail['card_content']
                })
            return result
        except Exception as e:
            print(e)

    def get_djpk_kemenkeu_detail(self, page_source, year, prov, pemda, data_type):
        result = []
        type_name = ''
        category_name = ''
        detail_name = ''
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            print('Proses data wilayah:{}, sub-wilayah={}, tahun={}'.format(
                prov['prov_name'], pemda['pemda_name'], year))
            table_container = soup.find('table', class_='table')
            rows = table_container.find_all('tr')
            rows.pop(0)
            for row in rows:
                cols = row.find_all('td')
                if len(cols) > 0:
                    field_name_col = cols[1]
                    field_name = cols[1].get_text(strip=True, separator='\n')
                    anggaran = re.sub(r'\s(M|m)', '', (cols[2].get_text(strip=True, separator='\n')))
                    realisasi = re.sub(r'\s(M|m)', '', (cols[3].get_text(strip=True, separator='\n')))
                    persentase = cols[4].get_text(strip=True, separator='\n')
                    if field_name_col.attrs.get('style') is None:
                        type_name = field_name
                        category_name = ''
                        detail_name = ''
                    elif field_name_col.attrs.get('style') == 'text-indent: 2em' or field_name_col.attrs.get('style') == 'text-indent: 1em':
                        category_name = field_name
                        detail_name = ''
                    elif field_name_col.attrs.get('style') == 'text-indent: 3em':
                        detail_name = field_name
                    else:
                        print('Different col styles')

                    row_data = {
                        'jenis_data': data_type,
                        'tahun': year,
                        'wilayah': prov['prov_name'],
                        'sub_wilayah': pemda['pemda_name'],
                        'jenis': type_name,
                        'kategori': category_name,
                        'rincian': detail_name,
                        'anggaran': anggaran,
                        'realisasi': realisasi,
                        'persentase': persentase,
                        'units': 'M'
                    }
                    result.append(row_data)
        except Exception as e:
            print(e)
        finally:
            return result

    def get_sigap_view_detail(self, page_source):
        result = None
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            description_box = soup.find_all('div', class_='deskripsi-box')
            detail = {
                'topik': None,
                'intansi_yang_dituju': None,
                'notes': None,
                'update': None,
                'lampiran': None
            }
            update_list = {
                'terverifikasi': None,
                'dalam_proses': None,
                'selesai': None,
                'tidak_valid': None
            }
            for box in description_box:
                label = box.find('label')
                if label is not None:
                    label_name = label.get_text(strip=True, separator='\n')
                    if label_name == 'Topik':
                        topic_container = box.find('p')
                        if topic_container is not None:
                            topic = topic_container.get_text(strip=True, separator='\n')
                            detail.update(
                                {'topik': topic}
                            )
                    elif label_name == 'Intansi yang di tuju':
                        target = []
                        target_list = box.find_all('li')
                        for target_row in target_list:
                            target_item = target_row.get_text(strip=True, separator='\n')
                            target.append(target_item)
                        detail.update(
                            {'intansi_yang_dituju': target}
                        )
                    elif label_name == 'Notes':
                        notes_container = box.find('p')
                        if notes_container is not None:
                            notes = notes_container.get_text(strip=True, separator='\n')
                            detail.update(
                                {'notes': notes}
                            )
                    elif label_name == 'Terverifikasi':
                        is_verified_container = box.find('p')
                        if is_verified_container is not None:
                            verified_date = is_verified_container.get_text(strip=True, separator='\n')
                            update_list.update(
                                {'terverifikasi': verified_date}
                            )
                    elif label_name == 'Dalam Proses':
                        is_process_container = box.find('p')
                        if is_process_container is not None:
                            process_date = is_process_container.get_text(strip=True, separator='\n')
                            update_list.update(
                                {'dalam_proses': process_date}
                            )
                    elif label_name == 'Selesai':
                        is_done_container = box.find('p')
                        if is_done_container is not None:
                            done_date = is_done_container.get_text(strip=True, separator='\n')
                            update_list.update(
                                {'selesai': done_date}
                            )
                    elif label_name == 'Tidak Valid':
                        is_invalid_container = box.find('p')
                        if is_invalid_container is not None:
                            invalid_date = is_invalid_container.get_text(strip=True, separator='\n')
                            update_list.update(
                                {'tidak_valid': invalid_date}
                            )
                else:
                    image_containers = box.find_all('a', class_='pop')
                    if len(image_containers) > 0:
                        image_urls = []
                        for image_item in image_containers:
                            image = image_item.find('img')
                            if image is not None:
                                image_url = image['src']
                                image_urls.append(image_url)
                        detail.update(
                            {'lampiran': image_urls}
                        )
            detail.update({'update': update_list})
            result = detail
        except Exception as e:
            print(e)
        finally:
            return result

    def get_wikidata_detail(self, page_source):
        in_more_lang = []
        statement = None
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            more_lang_container = soup.find('tbody', class_='wikibase-entitytermsforlanguagelistview-listview')
            lang_rows = more_lang_container.find_all('tr')
            for lang_item in lang_rows:
                language = lang_item.find('th', class_='wikibase-entitytermsforlanguageview-language').get_text(strip=True, separator='\n')
                label = lang_item.find('td', class_='wikibase-entitytermsforlanguageview-label').get_text(strip=True, separator='\n')
                description = lang_item.find('td', class_='wikibase-entitytermsforlanguageview-description').get_text(strip=True, separator='\n')
                also_known_as = lang_item.find('td', class_='wikibase-entitytermsforlanguageview-aliases').get_text(strip=True, separator='\n')
                in_more_lang.append({
                    'language': language,
                    'label': label,
                    'description': description,
                    'also_known_as': also_known_as,
                })

            statement_container = soup.find_all('div', class_='wikibase-statementgrouplistview')
            statement_items = statement_container[0].find_all('div', class_='wikibase-statementgroupview')
            statement_detail = {}
            for statement_item in statement_items:
                statement_label = statement_item.find('div', class_='wikibase-statementgroupview-property-label').get_text(strip=True, separator='\n')
                print('---{}---'.format(statement_label))
                if 'image' in statement_label or 'signature' in statement_label:
                    statement_contents_container = statement_item.find('div', class_='wikibase-statementview-mainsnak-container')
                    image_containers = statement_contents_container.find_all('a', class_='image')
                    image_urls = []
                    if len(image_containers) > 0:
                        for image_item in image_containers:
                            image = image_item.find('img')
                            if image is not None:
                                image_url = image['src']
                                image_urls.append(image_url)
                    content_data = image_urls
                else:
                    statement_contents_container = statement_item.find_all('div', class_='wikibase-statementview-mainsnak-container')
                    if len(statement_contents_container) == 1:
                        item_value_container = statement_contents_container[0].find('div', class_='wikibase-snakview-value-container')
                        content_data = item_value_container.find('div', class_='wikibase-snakview-body').get_text(strip=True, separator='\n')
                    else:
                        content_data = []
                        for statement_contents_container_item in statement_contents_container:
                            item_value_container = statement_contents_container_item.find('div', class_='wikibase-snakview-value-container')
                            item_value = item_value_container.find('div', class_='wikibase-snakview-body').get_text(strip=True, separator='\n')
                            item_property_container = statement_contents_container_item.find('div', class_='wikibase-statementview-qualifiers')
                            item_property = []
                            try:
                                item_property_list = item_property_container.find_all('div', class_='wikibase-snaklistview')
                                for property_item in item_property_list:
                                    property_name = property_item.find('div', class_='wikibase-snakview-property').get_text(strip=True, separator='\n')
                                    property_content = property_item.find('div', class_='wikibase-snakview-body').get_text(strip=True, separator='\n')
                                    item_property.append({'property_name': property_name,
                                                          'property_content': property_content})

                            except:
                                pass
                            if len(item_property) > 0:
                                content_data.append({
                                    'desc': item_value,
                                    'properties': item_property
                                })
                            else:
                                content_data.append({
                                    'desc': item_value
                                })
                statement_detail.update({statement_label: content_data})
            statement = statement_detail
        except Exception as e:
            print(e)
        finally:
            return in_more_lang, statement
