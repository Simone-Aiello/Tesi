var speed_values = [];
var ts = [];
function graphData(data) {
    data.forEach(function (element) {
        if (element.sensor === "speed") {
            speed_values.push(element.data);
            ts.push(element.timestamp);
        }
    });
}
function loadData() {
    $.ajax({
        'url': 'http://127.0.0.1:8000/rest_api/VehicleData',
        'type': 'GET',
        'success': function (data) {
            graphData(data);
        },
        'error': function (request, error) {
            console.log("Error reading data");
        }
    });
}
function initGraph() {
    ;
    var data = {
        labels: ts,
        datasets: [{
                label: 'speed',
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: speed_values
            }]
    };
    var config = {
        type: 'line',
        data: data,
        options: {}
    };
    var myChart = new Chart(document.getElementById('myChart'), config);
}
$(function () {
    loadData();
    initGraph();
});
