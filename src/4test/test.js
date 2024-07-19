function ExportExcel(sData, sModul) {
  if (sModul == "dashboard") {
    if ($("#subsektor").val() == "00") {
      alert("Subsektor belum dipilih.");
    } else if ($("#komoditas").val() == "00") {
      alert("Komoditas belum dipilih.");
    } else if ($("#indikator").val() == "00") {
      alert("Indikator belum dipilih.");
    } else if ($("#satuan").val() == "00") {
      alert("Satuan belum dipilih.");
    } else if ($("#tahunAwal").val() == "00") {
      alert("Tahun Awal belum dipilih.");
    } else if ($("#tahunAkhir").val() == "00") {
      alert("Tahun Akhir belum dipilih.");
    } else if ($("#tahunAkhir").val() < $("#tahunAwal").val()) {
      alert("Tahun Akhir tidak boleh lebih kecil dari Tahun Awal.");
    } else {
      var pie;
      var options;
      var maps;
      $.ajax({
        type: "POST",
        url: "home/result",
        data: sData,
        error: function (XMLHttpRequest, textStatus, errorThrown) {
          alert(
            "status:" +
              XMLHttpRequest.status +
              ", status text: " +
              XMLHttpRequest.statusText
          );
          $("#loader").hide();
        },
        success: function (response) {
          resp = JSON.parse(response);
          console.log(resp.grafik2);
          $("#judultabel").text(
            resp.indikatornm +
              " " +
              resp.komoditasnm +
              " " +
              resp.selisih +
              " " +
              " Tahun Terakhir " +
              " " +
              resp.satuandetail
          );
          $("#isitabel").html(resp.isitabel);
          var maps_string = resp.maps;
          var maps_data = JSON.parse(maps_string);
          var dt = [];
          for (var i in maps_data) {
            dt.push([i, maps_data[i]]);
          }
          var mapdata = dt;
          var json_stringpie = resp.pie;
          var json_datapie = JSON.parse(json_stringpie);
          var dtpie = [];
          for (var i in json_datapie) {
            dtpie.push(json_datapie);
          }
          var datapie = dtpie;
          if (resp.jumgrafik != 1) {
            var judulgrafik = resp.indikatornm1 + " dan " + resp.indikatornm2;
            var dtyaxis = [
              {
                labels: {
                  format: "{value:,.0f} ",
                  style: { color: Highcharts.getOptions().colors[1] },
                },
                min: 0,
                title: {
                  text: resp.indikatornm2 + "(" + resp.satuannm2 + ")",
                  style: { color: Highcharts.getOptions().colors[1] },
                },
              },
              {
                title: {
                  text: resp.indikatornm1 + "(" + resp.satuannm1 + ")",
                  style: { color: Highcharts.getOptions().colors[0] },
                },
                labels: {
                  format: "{value:,.0f} ",
                  style: { color: Highcharts.getOptions().colors[0] },
                },
                opposite: true,
              },
            ];
            var dtseries = [
              {
                name: resp.indikatornm1,
                type: "column",
                yAxis: 1,
                data: resp.grafik1,
                tooltip: { valueSuffix: " " + resp.satuannm1 },
              },
              {
                name: resp.indikatornm2,
                type: "spline",
                data: resp.grafik2,
                tooltip: { valueSuffix: " " + resp.satuannm2 },
              },
            ];
          } else {
            var judulgrafik = resp.indikatornm2;
            var dtyaxis = [
              {
                labels: {
                  format: "{value} ",
                  style: { color: Highcharts.getOptions().colors[1] },
                },
                title: {
                  text: resp.indikatornm2 + "(" + resp.satuannm2 + ")",
                  style: { color: Highcharts.getOptions().colors[1] },
                },
              },
            ];
            var dtseries = [
              {
                name: resp.indikatornm2,
                type: "column",
                data: resp.grafik2,
                tooltip: { valueSuffix: " " + resp.satuannm2 },
              },
            ];
          }
          options = new Highcharts.setOptions({
            lang: {
              numericSymbols: null,
              thousandsSep: ",",
              decimalPoint: ".",
            },
            colors: [
              "#0B6623",
              "#FF7F00",
              "#994F05",
              "#63B1F1",
              "#7C0000",
              "#2335AB",
              "#FF7Fcc",
              "#994005",
              "#63B101",
              "#7C00F0",
              "#23351B",
            ],
          });
          maps = new Highcharts.mapChart("tampilanpeta", {
            chart: { renderTo: "tampilanpeta", map: "countries/id/id-all" },
            title: {
              text:
                "Peta Sebaran " +
                resp.indikatornm +
                " " +
                resp.komoditasnm +
                " " +
                resp.satuandetail,
            },
            subtitle: { text: "Rata-Rata " + resp.interval },
            mapNavigation: {
              enabled: true,
              buttonOptions: { verticalAlign: "bottom" },
            },
            colorAxis: {
              dataClasses: [
                { color: "#ccc", from: 0, to: 0, name: "Tidak ada data" },
                {
                  color: "red",
                  from: resp.maplimit[0],
                  to: resp.maplimit[1],
                  name:
                    "Rendah " +
                    resp.maplimit[0] +
                    " " +
                    resp.satuannm +
                    " - " +
                    resp.maplimit[1] +
                    " " +
                    resp.satuannm,
                },
                {
                  color: "yellow",
                  from: resp.maplimit[1],
                  to: resp.maplimit[2],
                  name:
                    "Sedang " +
                    resp.maplimit[1] +
                    " " +
                    resp.satuannm +
                    " - " +
                    resp.maplimit[2] +
                    " " +
                    resp.satuannm,
                },
                {
                  color: "#28810D",
                  from: resp.maplimit[2],
                  to: resp.maplimit[3],
                  name:
                    "Tinggi " +
                    resp.maplimit[2] +
                    " " +
                    resp.satuannm +
                    " - " +
                    resp.maplimit[3] +
                    " " +
                    resp.satuannm,
                },
              ],
            },
            series: [
              {
                data: mapdata,
                name: "Data " + resp.indikatornm + " " + resp.komoditasnm,
                states: { hover: { color: "#E1F1FF" } },
                dataLabels: { enabled: true, format: "{point.name} " },
              },
            ],
          });
          graph = new Highcharts.Chart("tampilangrafik", {
            chart: { renderTo: "tampilangrafik", zoomType: "xy" },
            title: { text: judulgrafik + " " + resp.komoditasnm },
            subtitle: { text: resp.interval },
            xAxis: [{ categories: resp.tahungrafik, crosshair: true }],
            yAxis: dtyaxis,
            tooltip: { shared: true },
            legend: {
              layout: "vertical",
              align: "left",
              x: 120,
              verticalAlign: "top",
              y: 100,
              floating: true,
              backgroundColor:
                Highcharts.defaultOptions.legend.backgroundColor ||
                "rgba(255,255,255,0.25)",
            },
            series: dtseries,
          });
          pie = new Highcharts.Chart({
            chart: {
              renderTo: "tampilanpie",
              plotBackgroundColor: null,
              plotBorderWidth: null,
              plotShadow: false,
              type: "pie",
            },
            title: {
              text:
                "Kontribusi " +
                resp.indikatornm +
                " " +
                resp.komoditasnm +
                ", Rata-Rata " +
                resp.interval,
            },
            tooltip: {
              pointFormat: "{series.name}: <b>{point.percentage:.1f}%</b>",
            },
            accessibility: { point: { valueSuffix: "%" } },
            plotOptions: {
              pie: {
                allowPointSelect: true,
                cursor: "pointer",
                dataLabels: {
                  enabled: true,
                  format: "<b>{point.name}</b>: {point.percentage:.1f} %",
                },
              },
            },
            series: [
              {
                name: resp.indikatornm + " " + resp.komoditasnm,
                colorByPoint: true,
                data: datapie[0],
              },
            ],
          });
        },
      });
    }
  } else {
    $.ajax({
      type: "POST",
      url: sModul + "/result",
      data: sData,
      error: function (XMLHttpRequest, textStatus, errorThrown) {
        alert(
          "status:" +
            XMLHttpRequest.status +
            ", status text: " +
            XMLHttpRequest.statusText
        );
        $("#loader").hide();
      },
      success: function (data) {
        $("#loader").hide();
        $("#frmFilter").hide();
        $("#result-box").show();
        $("#result").html(data);
        $("#judul").hide();
        $("#search").hide();
        $("#excel").hide();
      },
    });
  }
}
$("#search").click(function () {
  var pData = getData(),
    lvl = $("#level").val(),
    kab = $("#kab").val(),
    prov = $("#prov").val(),
    modul = $("#modul").val();
  $("#loader").show();
  $("#loader").html(
    "<div class='preloader-wrapper'> <div class='preloader'><span></span><span></span><span></span><span></span><span></span><span></span></div></div>"
  );
  if (modul == "komoditas") {
    if (lvl == "03" && kab == "00") {
      alert("Kabupaten Belum Dipilih");
      $("#loader").hide();
    } else if (lvl == "02" && prov == "00") {
      alert("Provinsi Belum Dipilih");
      $("#loader").hide();
    } else {
      ExportExcel(pData, modul);
    }
  }
  if (modul == "indikator") {
    if (lvl == "03" && kab == "00") {
      alert("Kabupaten Belum Dipilih");
      $("#loader").hide();
    } else if (lvl == "02" && prov == "00") {
      alert("Provinsi Belum Dipilih");
      $("#loader").hide();
    } else {
      ExportExcel(pData, modul);
    }
  }
  if (modul == "lokasi") {
    if (lvl == "03" && prov == "00") {
      alert("Provinsi Belum Dipilih");
      $("#loader").hide();
    } else {
      ExportExcel(pData, modul);
    }
  }
});
$("#searchDashboard").click(function () {
  var pData = getData();
  $("#loader").show();
  $("#loader").html(
    "<div class='preloader-wrapper'> <div class='preloader'><span></span><span></span><span></span><span></span><span></span><span></span></div></div>"
  );
  ExportExcel(pData, "dashboard");
});
$("#excel,#excel1").click(function () {
  var subsektorcd = "",
    subsektornm = "",
    level = "",
    levelnm = "",
    prov = "",
    provnm = "",
    kab = "",
    kabnm = "",
    kec = "",
    kecnm = "",
    sts_angka = "",
    sts_angkanm = "",
    sumb_data = "",
    sumb_datanm = "",
    tahunAwal = "",
    tahunAkhir = "",
    rangethn = "",
    satuancd = "",
    satuannm = "",
    komoditas = "",
    komoditasnm = "",
    indikator = "",
    indikatornm = "",
    modul = $("#modul").val();
  if ($("#subsektor").length > 0) {
    subsektorcd = $("#subsektor").val();
    subsektornm = $("#subsektor option:selected").text();
  }
  if ($("#level").length > 0) {
    level = $("#level").val();
    levelnm = $("#level option:selected").text();
  }
  if ($("#prov").length > 0) {
    prov = $("#prov").val();
    provnm = $("#prov option:selected").text();
  }
  if ($("#kab").length > 0) {
    kab = $("#kab").val();
    kabnm = $("#kab option:selected").text();
  }
  if ($("#kec").length > 0) {
    kec = $("#kec").val();
    kecnm = $("#kec option:selected").text();
  }
  if ($("#sts_angka").length > 0) {
    sts_angka = $("#sts_angka").val();
    sts_angkanm = $("#sts_angka option:selected").text();
  }
  if ($("#sumb_data").length > 0) {
    sumb_data = $("#sumb_data").val();
    sumb_datanm = $("#sumb_data option:selected").text();
  }
  if ($("#tahunAwal").length > 0 && $("#tahunAkhir").length > 0) {
    tahunAwal = $("#tahunAwal").val();
    tahunAkhir = $("#tahunAkhir").val();
    satuancd = $("#satuan").val();
    satuannm = $("#satuan option:selected").text();
  }
  if ($("#komoditas").length > 0) {
    komoditas = $("#komoditas").val();
    komoditasnm = $("#komoditas option:selected").text();
  }
  if ($("#indikator").length > 0) {
    indikator = $("#indikator").val();
    indikatornm = $("#indikator option:selected").text();
  }
  $.redirect(
    "site/writeexcel/resultToExcel",
    {
      subsektorcd: subsektorcd,
      subsektornm: subsektornm,
      komoditas: komoditas,
      komoditasnm: komoditasnm,
      indikator: indikatornm,
      level: level,
      levelnm: levelnm,
      prov: prov,
      provnm: provnm,
      kab: kab,
      kabnm: kabnm,
      kec: kec,
      kecnm: kecnm,
      sts_angka: sts_angka,
      sts_angkanm: sts_angkanm,
      sumb_data: sumb_data,
      sumb_datanm: sumb_datanm,
      tahunAwal: tahunAwal,
      tahunAkhir: tahunAkhir,
      satuan: satuancd,
      satuannm: satuannm,
      komoditas: komoditas,
      komoditasnm: komoditasnm,
      indikator: indikator,
      indikatornm: indikatornm,
      judul: modul,
    },
    "POST",
    "_blank"
  );
});
$("#back").click(function () {
  $("#result-box").hide();
  $("#judul").show();
  $("#frmFilter").show();
  $("#search").show();
  $("#excel").show();
});
