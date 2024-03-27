POST /_msearch/ HTTP/2
Host: search.asia.lamudi.sector.run
Authorization: Basic bGFtdWRpLWlkLXByb2R1Y3Rpb24tc2VhcmNoOjZVejNySSY9VmZoSVkqdGdRS1FpKGEmKm19MnRHQXRs
Content-Type: application/x-ndjson
Content-Length: 325
Accept-Encoding: gzip, deflate, br
User-Agent: okhttp/4.10.0

{
  "index": "lamudi-id-production-locations-id"
}
{
  "from": 0,
  "query": {
    "bool": {
      "minimum_should_match": 1,
      "must": [
        {
          "range": {
            "level": {
              "gte": 3
            }
          }
        }
      ],
      "should": [
        {
          "multi_match": {
            "fields": "*",
            "query": "jakart",
            "type": "phrase_prefix"
          }
        },
        {
          "multi_match": {
            "fields": "*",
            "query": "jakart",
            "type": "most_fields"
          }
        }
      ]
    }
  },
  "size": 25,
  "track_total_hits": 1000
}