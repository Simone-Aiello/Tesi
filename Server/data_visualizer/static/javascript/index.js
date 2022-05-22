"use strict";
let interval;
let toggleAnimation = true;
let normal_speed_values = {};
let normal_rpm_values = {};
let anomalous_speed_values = {};
let anomalous_rpm_values = {};
let chart_not_anomalous_data = [];
let chart_anomalous_data = [];
let startDate = "";
let endDate = "";
const plotting_data = {
    datasets: [{
            label: 'Not anomalous',
            data: chart_not_anomalous_data,
            //backgroundColor: 'rgb(50, 101, 252)',
            backgroundColor: '#01cbcf',
            pointRadius: 5,
            pointHoverRadius: 10,
        },
        {
            label: 'Anomalous',
            data: chart_anomalous_data,
            //backgroundColor: 'rgb(255, 99, 132)',
            backgroundColor: '#fe546f',
            pointRadius: 5,
            pointHoverRadius: 10,
        }
    ],
};
const SpeedRpmConfig = {
    type: 'scatter',
    data: plotting_data,
    options: {
        plugins: {
            title: {
                display: true,
                text: 'Engine Speed and RPM',
                color: "#fffdff",
            },
            legend: {
                labels: {
                    color: "#fffdff",
                }
            },
        },
        scales: {
            x: {
                type: 'linear',
                position: 'bottom',
                title: {
                    display: true,
                    text: 'Rpm',
                    font: {
                        family: 'Times',
                        size: 20,
                        style: 'normal',
                        lineHeight: 1.2
                    },
                    color: "#fffdff",
                },
                grid: {
                    borderColor: "#fffdff",
                    display: false,
                },
                ticks: {
                    color: '#fffdff',
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Speed(km/h)',
                    font: {
                        family: 'Times',
                        size: 20,
                        style: 'normal',
                        lineHeight: 1.2
                    },
                    color: "#fffdff",
                },
                grid: {
                    borderColor: "#fffdff",
                    display: false,
                },
                ticks: {
                    color: '#fffdff',
                },
            }
        },
    },
};
function graphData(chart, data) {
    normal_speed_values = {};
    normal_rpm_values = {};
    anomalous_speed_values = {};
    anomalous_rpm_values = {};
    chart_not_anomalous_data.length = 0;
    chart_anomalous_data.length = 0;
    data.forEach((element) => {
        if (element.sensor === "speed") {
            if (!element.anomalous) {
                normal_speed_values[element.timestamp] = Math.floor(element.data);
            }
            else {
                anomalous_speed_values[element.timestamp] = Math.floor(element.data);
            }
        }
        else if (element.sensor === "rpm") {
            if (!element.anomalous) {
                normal_rpm_values[element.timestamp] = Math.floor(element.data);
            }
            else {
                anomalous_rpm_values[element.timestamp] = Math.floor(element.data);
            }
        }
    });
    for (const [key, value] of Object.entries(normal_speed_values)) {
        if (key in normal_rpm_values) {
            let d = {
                "x": normal_rpm_values[key],
                "y": value,
            };
            chart_not_anomalous_data.push(d);
        }
    }
    for (const [key, value] of Object.entries(anomalous_speed_values)) {
        if (key in anomalous_speed_values) {
            let d = {
                "x": anomalous_rpm_values[key],
                "y": value,
            };
            chart_anomalous_data.push(d);
        }
    }
    // @ts-expect-error
    chart.update("none");
}
function loadData(SpeedRpmChart) {
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
            graphData(SpeedRpmChart, data);
            toggleAnimation = false;
        },
        'error': function (request, error) {
            console.log("Error reading data");
        }
    });
}
function dateEventHandlers(chart) {
    $("#start-date").on("change", function (e) {
        startDate = String($("#start-date").val());
        console.log(startDate);
        clearInterval(interval);
        toggleAnimation = true;
        loadData(chart);
        interval = setInterval(() => {
            loadData(chart);
        }, 3000);
    });
    $("#end-date").on("change", function (e) {
        endDate = String($("#end-date").val());
        clearInterval(interval);
        toggleAnimation = true;
        loadData(chart);
        // interval = setInterval(() =>{
        //     loadData(chart);
        // },3000);
    });
}
$(function () {
    // @ts-expect-error
    //const SpeedRpmChart = new Chart($("#SpeedRpmChart"), SpeedRpmConfig);
    //loadData(SpeedRpmChart);
    dateEventHandlers(SpeedRpmChart);
    // interval = setInterval(() =>{
    //     loadData(myChart);
    // },3000);
});
