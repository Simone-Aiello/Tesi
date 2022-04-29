"use strict";
function sdadsad(myChart) {
    console.log("Eseguo");
    $.ajax({
        'url': '/rest_api/VehicleData',
        'type': 'GET',
        'data': {
            vehicle: "FG868XN",
            sensor: ["speed", "rpm"],
            start_date: startDate,
            end_date: endDate,
        },
        'success': function (data) {
            graphData(myChart, data);
            //setTimeout(() =>{ TODO: fare refresh automatico
            //    loadData(myChart);
            //},10000);
            toggleAnimation = false;
        },
        'error': function (request, error) {
            console.log("Error reading data");
        }
    });
}
function asdasda(chart) {
    $("#start-date").on("change", function (e) {
        startDate = String($("#start-date").val());
        console.log(startDate);
        toggleAnimation = true;
        sdadsad(chart);
    });
    $("#end-date").on("change", function (e) {
        endDate = String($("#end-date").val());
        toggleAnimation = true;
        sdadsad(chart);
    });
}
let wheel_scatter_data_points = [{
        x: 10,
        y: 8,
    },
    {
        x: 9,
        y: 15,
    },
    {
        x: 19,
        y: 15,
    },
    {
        x: 9,
        y: 7,
    },
    {
        x: 19,
        y: 13,
    },
];
const wheel_scatter_data = {
    datasets: [{
            label: 'Measurement',
            data: wheel_scatter_data_points,
            backgroundColor: 'rgb(50, 101, 252)',
            pointRadius: 5,
            pointHoverRadius: 10,
            borderColor: 'rgb(50, 101, 252)',
        },
    ],
};
const wheel_line_data = {
    labels: [1, 2, 3],
    datasets: [{
            label: 'Line',
            data: [2, 4, 6],
            backgroundColor: 'rgb(0, 0, 255)',
            pointRadius: 5,
            pointHoverRadius: 10,
            borderColor: 'rgb(0, 0, 255',
        },
    ],
};
const wheel_line_config = {
    type: 'line',
    data: wheel_line_data,
};
const wheel_scatter_config = {
    type: 'scatter',
    data: wheel_scatter_data,
    options: {
        scales: {
            x: {
                type: 'linear',
                position: 'bottom',
                title: {
                    display: true,
                    text: 'Pressure(bar)',
                    font: {
                        family: 'Times',
                        size: 20,
                        style: 'normal',
                        lineHeight: 1.2
                    },
                },
            },
            y: {
                title: {
                    display: true,
                    text: 'Timestamp',
                    font: {
                        family: 'Times',
                        size: 20,
                        style: 'normal',
                        lineHeight: 1.2
                    },
                },
            }
        },
    },
};
$(function () {
    // @ts-expect-error
    const myChart = new Chart($("#wheel-chart"), {
        data: {
            datasets: [{
                    type: 'scatter',
                    label: 'Scatter Dataset',
                    data: wheel_scatter_data_points,
                    backgroundColor: 'rgb(0, 0, 255)',
                    borderColor: 'rgb(0, 0, 255)',
                }, {
                    type: 'line',
                    label: 'Line Dataset',
                    data: [2, 4, 6, 8],
                    backgroundColor: 'rgb(255, 0, 0)',
                    borderColor: 'rgb(255, 0, 0)',
                }],
            labels: [11.3, 13, 15, 18],
        },
        options: {}
    });
    //sdadsad(myChart);
    //sdadsad(myChart);
});
