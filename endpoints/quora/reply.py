import requests

params = {
    'q': 'CommentableCommentAreaLoaderInnerQuery',
}

json_data = {
    'queryName': 'CommentableCommentAreaLoaderInnerQuery',
    'variables': {
        'id': 'QW5zd2VyQDEwOjE3NDY5MzYxOQ==',
        'first': 2,
    },
    'extensions': {
        'hash': '7049e6ccf2e18aa1683cf340f4ab83a167ffe783381fdc89195a88646d2bba57',
    },
}

response = requests.post(
    'https://id.quora.com/graphql/gql_para_POST',
    params=params,
    json=json_data,
)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"queryName":"CommentableCommentAreaLoaderInnerQuery","variables":{"id":"QW5zd2VyQDEwOjE3NDY5MzYxOQ==","first":2},"extensions":{"hash":"7049e6ccf2e18aa1683cf340f4ab83a167ffe783381fdc89195a88646d2bba57"}}'
#response = requests.post('https://id.quora.com/graphql/gql_para_POST', params=params, cookies=cookies, headers=headers, data=data)