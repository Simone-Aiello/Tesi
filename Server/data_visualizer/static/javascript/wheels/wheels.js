"use strict";
let x_labels = {};
let wheel_sensor = "";
let sensor_data = [];
let regressione_line_points = [];
function parseTimestamp(timestamp) {
    let d = new Date(timestamp);
    let month = d.getMonth() + 1;
    let year = d.getFullYear();
    let day = d.getDate();
    return day + "-" + month + "-" + year;
}
function plotData(mis, myChart, line_points, toggle_animation) {
    sensor_data.length = 0;
    regressione_line_points.length = 0;
    mis.forEach((m) => {
        let d = new Date(m.timestamp);
        x_labels[d.getTime()] = m.timestamp;
        let dict = {
            x: d.getTime(),
            y: m.data,
        };
        sensor_data.push(dict);
    });
    if (line_points != null) {
        line_points.forEach((point) => {
            let dt = new Date(point.y);
            //local_max_x = dt.getTime() < local_max_x ? dt.getTime() : local_max_x;
            let dict = {
                x: dt.getTime(),
                y: point.x,
            };
            regressione_line_points.push(dict);
        });
    }
    //@ts-expect-error
    toggle_animation ? myChart.update() : myChart.update("none");
}
function loadWheelData(myChart, toggle_animation) {
    console.log("Eseguo");
    $.ajax({
        'url': '/rest_api/WheelData',
        'type': 'GET',
        'data': {
            vehicle: "FG868XN",
            wheel: wheel_sensor,
            //start_date : startDate,
            //end_date : endDate,
        },
        'success': function (data) {
            let mis = data["data"];
            plotData(mis, myChart, data["line_points"], toggle_animation);
        },
        'error': function (request, error) { }
    });
}
const data = {
    datasets: [
        {
            type: "scatter",
            label: 'Data points',
            data: sensor_data,
            borderColor: "rgb(50, 101, 252)",
            backgroundColor: "rgb(50, 101, 252)",
            order: 1,
            pointRadius: 4,
            pointHoverRadius: 8,
        },
        {
            type: "line",
            label: 'Linear regression',
            data: regressione_line_points,
            borderColor: "rgb(255, 99, 132)",
            backgroundColor: "rgb(255, 99, 132)",
            order: 2
        }
    ]
};
const cfg = {
    data: data,
    options: {
        responsive: true,
        plugins: {
            tooltip: {
                callbacks: {
                    footer: (tooltipItems) => {
                        let date = null;
                        tooltipItems.forEach((tooltipItem) => {
                            let value = tooltipItem.parsed.y;
                            date = parseTimestamp(tooltipItem.parsed.x);
                        });
                        return "Date: " + date;
                    },
                }
            },
            legend: {
                position: 'top',
            },
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Date',
                    font: {
                        family: 'Times',
                        size: 20,
                        style: 'normal',
                        lineHeight: 1.2
                    },
                },
                ticks: {
                    // Include a dollar sign in the ticks
                    callback: function (value, index, ticks) {
                        return parseTimestamp(value);
                    }
                },
            },
            y: {
                title: {
                    display: true,
                    text: 'Pressure (Bar)',
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
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    wheel_sensor = urlParams.get('wheel') != null ? urlParams.get('wheel') : "";
    // @ts-expect-error
    const myChart = new Chart($("#wheel-chart"), cfg);
    loadWheelData(myChart, true);
    let interval = setInterval(() => {
        loadWheelData(myChart, false);
    }, 3000);
});
