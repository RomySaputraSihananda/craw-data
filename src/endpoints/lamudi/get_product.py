POST /_msearch/ HTTP/2
Host: search.asia.lamudi.sector.run
Authorization: Basic bGFtdWRpLWlkLXByb2R1Y3Rpb24tc2VhcmNoOjZVejNySSY9VmZoSVkqdGdRS1FpKGEmKm19MnRHQXRs
Content-Type: application/x-ndjson
Content-Length: 1943
Accept-Encoding: gzip, deflate, br
User-Agent: okhttp/4.10.0

{
  "index": "lamudi-id-production-ads-id"
}
{
  "from": 0,
  "query": {
    "function_score": {
      "boost_mode": "replace",
      "functions": [
        {
          "script_score": {
            "script": "double cvrPdpSku = doc.containsKey('scoreDetails.cvrPdpSku') && doc['scoreDetails.cvrPdpSku'].size() > 0 ? doc['scoreDetails.cvrPdpSku'].value : 0; double ctrClpSku = doc.containsKey('scoreDetails.ctrClpSku') && doc['scoreDetails.ctrClpSku'].size() > 0 ? doc['scoreDetails.ctrClpSku'].value : 0; double leadScoreSku = doc.containsKey('scoreDetails.leadScoreSku') && doc['scoreDetails.leadScoreSku'].size() > 0 ? doc['scoreDetails.leadScoreSku'].value : 0; double viewScoreSku = doc.containsKey('scoreDetails.viewScoreSku') && doc['scoreDetails.viewScoreSku'].size() > 0 ? doc['scoreDetails.viewScoreSku'].value : 0; double cplScoreSku = doc.containsKey('scoreDetails.cplScoreSku') && doc['scoreDetails.cplScoreSku'].size() > 0 ? doc['scoreDetails.cplScoreSku'].value : 0; double premiumScore = doc.containsKey('scoreDetails.premiumScore') && doc['scoreDetails.premiumScore'].size() > 0 ? doc['scoreDetails.premiumScore'].value : 0; return (cvrPdpSku * 300 + ctrClpSku * 300 + leadScoreSku * 3 + viewScoreSku * 7 + cplScoreSku * 150 + premiumScore * 500) / 6"
          }
        }
      ],
      "query": {
      },
      "score_mode": "avg"
    }
  },
  "size": 25,
  "track_total_hits": 1000000
}