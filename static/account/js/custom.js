/*  Custom JS
    Create by ione 28 Apr 2022
*/

// Variabel untuk menyimpan file path masing2 komponen file upload
// Jika ada isinya, maka hapus dulu file lama sebelum upload lagi file baru di komponen yg sama
var file_path = ['','',''];

function do_delete(pPk, pName) {
    if (confirm('Anda yakin menghapus data "'+ pName + '"?')) {
        $.ajax({
            url: "/enc_text/" + pPk, 
            success: function(result){                    
                window.location.href = 'delete/' + result; // + '/' + pPhotoID;
            }
        });            
    };
}; 

function do_edit(pPk) {        
    $.ajax({
        url: "/enc_text/" + pPk, 
        success: function(result){                
            window.location.href = 'edit/' + result; // + '/' + pPhotoID;
         }
    });              
}; 

function do_copy_to_clipboard(pData) {
    // alert(pData);
    var $temp = $("<input>");
    $("body").append($temp);
    // $temp.val($(element).text()).select();
    $temp.val(pData).select();

    // console.log($temp);

    document.execCommand("copy");
    $temp.remove();

    alert('URL sudah di copy!')
};

var randomColorFactor = function() {
    return Math.round(Math.random() * 255);
};

var randomColor = function(opacity) {
    return 'rgba(' + randomColorFactor() + ',' + randomColorFactor() + ',' + randomColorFactor() + ',' + (opacity || '.3') + ')';
};

function create_graph_newscount(plabel, pdata1, pdata2, pdata3) {
// News Count
    // HitCount
    //var bln = "{{mChartNews.bulan}}";
    //var berita = {{mChartNews.berita}};
    //var pengumuman = {{mChartNews.pengumuman}};
    //var artikel = {{mChartNews.artikel}};
    //var bln2 = bln.split(",");
    console.log('Inside function');
    console.log(plabel);
    console.log(pdata1);
    console.log(pdata2);
    console.log(pdata3);
    
    var LineConfigNews = {
        type: 'line',
        data: {
            //labels: ['January', "February", "March", "April", "May", "June", "July"],
            labels: plabel,
            datasets: [{
                label: "Berita",                
                data : pdata1,
                
            }, 
            {
                label: "Pengumuman",
                data: pdata2,
            }, 
            {
                label: "Artikel",
                data: pdata3,
            }
            
            ]
        },
        options: {
            responsive: true,
            tooltips: {
                mode: 'label'
            },
            hover: {
                mode: 'dataset'
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        show: true,
                        labelString: 'Month'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        show: true,
                        labelString: 'Value'
                    },
                    ticks: {
                        suggestedMin: 0,
                        suggestedMax: 10,
                    }
                }]
            }
        }
    };

    $.each(LineConfigNews.data.datasets, function(i, dataset) {
        dataset.borderColor = 'rgba(0,0,0,0.15)';
        dataset.backgroundColor = randomColor(0.5);
        dataset.pointBorderColor = 'rgba(0,0,0,0.15)';
        dataset.pointBackgroundColor = randomColor(0.5);
        dataset.pointBorderWidth = 1;
    });

    return LineConfigNews;
};

// parameter dalam array
function create_graph_hitcount(plabel, pdata) {
    // HitCount
    // var bln = "{{mChartHit.bulan}}";
    // var hit = {{mChartHit.hit}};
    // var bln2 = bln.split(",");

    //bln.replaceAll("&#x27;","\'");
    console.log('Inside function');
    console.log(plabel);
    console.log(pdata);

    var LineConfig = {
        type: 'line',
        data: {
            //labels: ['January', "February", "March", "April", "May", "June", "July"],
            labels: plabel,
            datasets: [{
                label: "Hit Count",
                //data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()],
                data : pdata,
                
            }, 
            //{
            //    label: "My Second dataset",
            //    data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()],
            // }
            
            ]
        },
        options: {
            responsive: true,
            tooltips: {
                mode: 'label'
            },
            hover: {
                mode: 'dataset'
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        show: true,
                        labelString: 'Month'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        show: true,
                        labelString: 'Value'
                    },
                    ticks: {
                        suggestedMin: 0,
                        suggestedMax: 10,
                    }
                }]
            }
        }
    };

    $.each(LineConfig.data.datasets, function(i, dataset) {
        dataset.borderColor = 'rgba(0,0,0,0.15)';
        dataset.backgroundColor = randomColor(0.5);
        dataset.pointBorderColor = 'rgba(0,0,0,0.15)';
        dataset.pointBackgroundColor = randomColor(0.5);
        dataset.pointBorderWidth = 1;
    });

    return LineConfig;
};

function highchart_productivity(pselector, pdata, pdrilldown, ptitle, psubtitle) {
    // Kontribusi pada website
    console.log('pdrilldown inside function');
    console.log(JSON.stringify(pdrilldown));

    // console.log('pdata inside function');
    // console.log(JSON.stringify(pdata));

    Highcharts.chart(pselector, {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: ptitle
        },
        subtitle: {
            text: psubtitle
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.2f}%</b>'
            // headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
            // pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}%</b> of total<br/>'
        },
        accessibility: {
            announceNewData: {
                enabled: true
            },
            point: {
                valueSuffix: '%'
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.2f} %'
                }
            },
            series: {
                dataLabels: {
                    enabled: true,
                    format: '{point.name}: {point.y:.2f}%'
                }
            }
        },
        series: [{
            name: 'Kontribusi',
            colorByPoint: true,
            data: pdata            
        }],
        drilldown: {
            series: pdrilldown
        }
    });
};

function highchart_keterisian_menu(pselector, plabel, pdata) {
    // Kontribusi pada website
    console.log('data = ');
    console.log(pdata);

    Highcharts.chart(pselector, {
        title: {
            text: 'Sepuluh Besar Keterisian Menu Website'
        },
        xAxis: {
            categories: plabel // # ['Apples', 'Oranges', 'Pears', 'Bananas', 'Plums']
        },        
        // labels: {
        //     items: [{
        //         html: 'Total fruit consumption',
        //         style: {
        //             left: '50px',
        //             top: '18px',
        //             color: ( // theme
        //                 Highcharts.defaultOptions.title.style &&
        //                 Highcharts.defaultOptions.title.style.color
        //             ) || 'black'
        //         }
        //     }]
        // },
        series: pdata
        
        // [{
        //     type: 'column',
        //     name: 'Jane',
        //     data: [3, 2, 1, 3, 4]
        // }, {
        //     type: 'column',
        //     name: 'John',
        //     data: [2, 3, 5, 7, 6]
        // },
        // // {
        // //     type: 'column',
        // //     name: 'Joe',
        // //     data: [4, 3, 3, 9, 0]
        // // }, 
        // {
        //     type: 'spline',
        //     name: 'Average',
        //     data: [3, 2.67, 3, 6.33, 3.33],
        //     marker: {
        //         lineWidth: 2,
        //         lineColor: Highcharts.getOptions().colors[3],
        //         fillColor: 'white'
        //     }
        // }, 
        // // {
        // //     type: 'pie',
        // //     name: 'Total consumption',
        // //     data: [{
        // //         name: 'Jane',
        // //         y: 13,
        // //         color: Highcharts.getOptions().colors[0] // Jane's color
        // //     }, {
        // //         name: 'John',
        // //         y: 23,
        // //         color: Highcharts.getOptions().colors[1] // John's color
        // //     }, {
        // //         name: 'Joe',
        // //         y: 19,
        // //         color: Highcharts.getOptions().colors[2] // Joe's color
        // //     }],
        // //     center: [100, 80],
        // //     size: 100,
        // //     showInLegend: false,
        // //     dataLabels: {
        // //         enabled: false
        // //     }
        
        // // }
        // ]
    });

    // Highcharts.chart(pselector, {
    //     chart: {
    //         type: 'bar'
    //     },
    //     title: {
    //         text: 'Sepuluh Besar Keterisian Menu Website'
    //     },
    //     // subtitle: {
    //     //     text: 'Source: <a href="https://en.wikipedia.org/wiki/World_population">Wikipedia.org</a>'
    //     // },
    //     xAxis: {
    //         categories: ['Africa', 'America', 'Asia', 'Europe', 'Oceania'],
    //         title: {
    //             text: null
    //         }
    //     },
    //     yAxis: {
    //         min: 0,
    //         title: {
    //             text: 'Keterisian (%)',
    //             align: 'high'
    //         },
    //         labels: {
    //             overflow: 'justify'
    //         }
    //     },
    //     tooltip: {
    //         valueSuffix: ' %'
    //     },
    //     plotOptions: {
    //         bar: {
    //             dataLabels: {
    //                 enabled: true
    //             }
    //         }
    //     },
    //     legend: {
    //         layout: 'vertical',
    //         align: 'right',
    //         verticalAlign: 'top',
    //         x: -40,
    //         y: 80,
    //         floating: true,
    //         borderWidth: 1,
    //         backgroundColor:
    //             Highcharts.defaultOptions.legend.backgroundColor || '#FFFFFF',
    //         shadow: true
    //     },
    //     credits: {
    //         enabled: false
    //     },
    //     series: [{
    //         name: 'Year 1800',
    //         data: [107, 31, 635, 203, 2]
    //     }, 
    //     // {
    //     //     name: 'Year 1900',
    //     //     data: [133, 156, 947, 408, 6]
    //     // }, {
    //     //     name: 'Year 2000',
    //     //     data: [814, 841, 3714, 727, 31]
    //     // }, {
    //     //     name: 'Year 2016',
    //     //     data: [1216, 1001, 4436, 738, 40]
    //     // }
    //     ]
    // });

    // Highcharts.chart(pselector, {
    //     chart: {
    //         plotBackgroundColor: null,
    //         plotBorderWidth: null,
    //         plotShadow: false,
    //         type: 'pie'
    //     },
    //     title: {
    //         text: 'Sepuluh Besar Keterisian Menu Website'
    //     },
    //     tooltip: {
    //         pointFormat: '{series.name}: <b>{point.percentage:.2f}%</b>'
    //     },
    //     accessibility: {
    //         point: {
    //             valueSuffix: '%'
    //         }
    //     },
    //     plotOptions: {
    //         pie: {
    //             allowPointSelect: true,
    //             cursor: 'pointer',
    //             dataLabels: {
    //                 enabled: true,
    //                 format: '<b>{point.name}</b>: {point.percentage:.2f} %'
    //             }
    //         }
    //     },
    //     series: [{
    //         name: 'Menu',
    //         colorByPoint: true,
    //         data: pdata            
    //     }]
    // });
};

function highchart_keterisian_detail(pdata, title) {
    // Keterisian Menu Website

    Highcharts.chart('pieChart3', {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: title
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.2f}%</b>'
        },
        accessibility: {
            point: {
                valueSuffix: '%'
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.2f} %'
                }
            }
        },
        series: [{
            name: 'Persentase',
            colorByPoint: true,
            data: pdata            
        }]
    });
};

(function($) {
    // Foto banner (tanpa multi form)
    $("#id_photo-file_path").on("change", function () {
        if (this.files && this.files[0]) {
            console.log('inside trigger photo');
            var reader = new FileReader();
            reader.onload = function (e) {
                $("#image").attr("src", e.target.result);
                $("#form-id").val("photo");
                $("#modalCrop").modal("show");
            }
            reader.readAsDataURL(this.files[0]);
        }
    });
    // End tanpa multi form

    $("#id_form-0-file_path").on("change", function () {
        if (this.files && this.files[0]) {
            console.log('inside trigger photo 0');
            var reader = new FileReader();
            reader.onload = function (e) {
                $("#image").attr("src", e.target.result);
                $("#form-id").val("form-0");
                $("#modalCrop").modal("show");
            }
            reader.readAsDataURL(this.files[0]);
        }
    });

    $("#id_form-1-file_path").on("change", function () {
        if (this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $("#image").attr("src", e.target.result);
                $("#form-id").val("form-1");
                $("#modalCrop").modal("show");
            }
            reader.readAsDataURL(this.files[0]);
        }
    });

    $("#id_form-2-file_path").on("change", function () {
        if (this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $("#image").attr("src", e.target.result);
                $("#form-id").val("form-2");
                $("#modalCrop").modal("show");
            }
            reader.readAsDataURL(this.files[0]);
        }
    });

    /* SCRIPTS TO HANDLE THE CROPPER BOX */
    var $image = $("#image");
    var cropBoxData;
    var canvasData;
    var cropBox = {
        left : 0,
        top : 0,
        width : 400, //900, 
        height : 400 //700
    };       
      
    $("#modalCrop").on("show.bs.modal", function () {
        // ww dan hh default sudah ada di masing2 template pemanggil
        // Baca data di interface untuk membedakan ukuran gambar
        // galery layanan ukuran lebih besar

        $(".js-crop-and-upload").removeAttr("disabled").text('Crop and Upload');

        var banner_position = $("#id_banner-position").val();
        if (banner_position != null) {
            if (banner_position == 'top' || banner_position == 'bottom') {
                ww = 728; hh = 90;
            }
            else {  // middle1 and middle2
                ww = 300; hh = 600;
            }
        };        

        console.log('This is inside crop');
        console.log('Inside #modalCrop');
        console.log(ww);
        console.log(hh);
        
        // acpec ration tidak perlu hh/ww untuk kondisi hh>ww
        var aspect_ratio = ww/hh;
        console.log('aspect ratio', aspect_ratio);
        
        $image.cropper({
            viewMode: 0,    // mode 2 atau 0 untuk resize melewati ukuran gambar
            aspectRatio: aspect_ratio,
            zoomable: true,
            dragMode: 'move',
            center: true,
            cropBoxResizable: true,               

            // rotatable: true,
            // autoCropArea: 0.7,
            // highlight: false,
            // background: false,
            // viewMode: 1,
            // aspectRatio: 1/1,
            // minCropBoxWidth: ww,
            // minCropBoxHeight: hh,
            // width: ww,
            // height: hh,     
            
            ready: function () {                        
                $image.cropper('setCropBoxData', cropBox);                
                $image.cropper("setCanvasData", canvasData);
                $image.cropper("setCropBoxData", cropBoxData);                
            }
        });

    }).on("hidden.bs.modal", function () {
        console.log('on hidden event');
        cropBoxData = $image.cropper("getCropBoxData");
        canvasData = $image.cropper("getCanvasData");
        $image.cropper("destroy");
    });

    $(".js-zoom-in").on("click", function () {
        console.log('inside zoom in');
        $image.cropper("zoom", 0.1);
    });

    $(".js-zoom-out").on("click", function () {
      $image.cropper("zoom", -0.1);
    });

    $(".js-move-to-0-0").on("click", function () {
        console.log('inside move 0,0');
        $image.cropper("moveTo", 0.0);
    });

    /* SCRIPT TO COLLECT THE DATA AND POST TO THE SERVER */
    $(".js-crop-and-upload").on("click", function () {
        // $(".js-crop-and-upload").text('Waiting...');
        $(".js-crop-and-upload").attr("disabled", true).text('Processing ...');

        var cropData = $image.cropper("getData");
        var formID = $("#form-id").val();
        var canvas = $image.cropper("getCroppedCanvas");

        console.log(canvas);        
        console.log('Inside #js-crop-and-upload');
        // console.log(ww);
        // console.log(hh);

        canvas.toBlob(function (blob) {
            var formData = new FormData();

            formData.append('photo', blob);          
            // console.log(blob);            
            let csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
            // console.log(csrftoken);

            console.log('value before upload = ');
            console.log($("#id_"+ formID +"-file_path").val());
            console.log(formID);

            var arr_idx = formID.split('-');
            var idx = 0;
            if (arr_idx.length >= 2)
                idx = arr_idx[1]

            formData.append('old_photo', file_path[idx]);

            $.ajax('/dashboard/upload-photo/' + ww + '/' + hh + '/', {
                method: "POST",
                data: formData,
                processData: false,
                contentType: false,
                async: false,       // set false for waiting result, set time out too, to make limit time waiting
                cache: false,
                timeout: 30000,

                headers:{'X-CSRFToken':csrftoken},

                success: function (response) {
                    console.log('response = ');
                    console.log(response);
                    file_path[idx] = response;
                    $("#id_"+ formID +"-str_file_path").val(file_path[idx]);                    
                    //alert('done');

                    console.log('outside canvas blob')
                    console.log('result');
                    console.log(cropData["x"]);
                    console.log(cropData["y"]);
                    console.log(cropData["height"]);
                    console.log(cropData["width"]);
                    
                    $("#id_"+ formID +"-x").val(cropData["x"]);
                    $("#id_"+ formID +"-y").val(cropData["y"]);
                    $("#id_"+ formID +"-height").val(cropData["height"]);
                    $("#id_"+ formID +"-width").val(cropData["width"]);

                    //$("#formUpload").submit();
                    $("#modalCrop").modal('hide');
                },

                error: function () {
                    console.log('Upload error');
                }
            });

            //alert('after call ajax');
        });                

        // console.log('outside canvas blob')
        // console.log('result');
        // console.log(cropData["x"]);
        // console.log(cropData["y"]);
        // console.log(cropData["height"]);
        // console.log(cropData["width"]);
        
        // $("#id_"+ formID +"-x").val(cropData["x"]);
        // $("#id_"+ formID +"-y").val(cropData["y"]);
        // $("#id_"+ formID +"-height").val(cropData["height"]);
        // $("#id_"+ formID +"-width").val(cropData["width"]);

        // //$("#formUpload").submit();
        // $("#modalCrop").modal('hide');
    });

}(jQuery));
