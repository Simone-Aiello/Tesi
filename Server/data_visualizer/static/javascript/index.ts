interface ScatterData{
    "x" : number,
    "y" : number,
}
interface Misuration{
    "vehicle": string,
    "sensor": string,
    "data": number,
    "timestamp": string,
    "anomalous": boolean,
}
let interval: number;
let toggleAnimation = true;
let normal_speed_values: {[key:string]: number} = {};
let normal_rpm_values: {[key:string]: number} = {};
let anomalous_speed_values: {[key:string]: number} = {};
let anomalous_rpm_values: {[key:string]: number} = {};
let chart_not_anomalous_data : Array<ScatterData> = [];
let chart_anomalous_data : Array<ScatterData> = [];
let startDate : string = "";
let endDate : string = "";
const plotting_data = {
    datasets: [{
        label: 'Not anomalous',
        data: chart_not_anomalous_data,
        backgroundColor: 'rgb(50, 101, 252)',
        pointRadius: 5,
        pointHoverRadius: 10,
    },
    {
        label: 'Anomalous',
        data: chart_anomalous_data,
        backgroundColor: 'rgb(255, 99, 132)',
        pointRadius: 5,
        pointHoverRadius: 10,
    }
],
};
const config = {
    type: 'scatter',
    data: plotting_data,
    options: {
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
                },
            },
            y:{
                title: {
                    display: true,
                    text: 'Speed(km/h)',
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
function graphData(chart : Chart,data : Array<Misuration>) : void{
    normal_speed_values = {};
    normal_rpm_values = {};
    anomalous_speed_values = {};
    anomalous_rpm_values = {};
    chart_not_anomalous_data.length = 0;
    chart_anomalous_data.length = 0;
    data.forEach((element) =>{
        if (element.sensor === "speed"){
            if(!element.anomalous){
                normal_speed_values[element.timestamp] = Math.floor(element.data);
            }
            else{
                anomalous_speed_values[element.timestamp] = Math.floor(element.data);
            }
        }
        else if(element.sensor === "rpm"){
            if(!element.anomalous){
                normal_rpm_values[element.timestamp] = Math.floor(element.data);
            }
            else{
                anomalous_rpm_values[element.timestamp] = Math.floor(element.data);
            }
        }
    });
    for (const [key, value] of Object.entries(normal_speed_values)) {
        if(key in normal_rpm_values){
            let d : ScatterData = {
                "x" : normal_rpm_values[key],
                "y" : value,
            };
            chart_not_anomalous_data.push(d);
        }
    }
    for (const [key, value] of Object.entries(anomalous_speed_values)) {
        if(key in anomalous_speed_values){
            let d : ScatterData = {
                "x" : anomalous_rpm_values[key],
                "y" : value,
            };
            chart_anomalous_data.push(d);
        }
    }
    // @ts-expect-error
    toggleAnimation ? chart.update() : chart.update("none");
}
function loadData(myChart: Chart) : void{
    console.log("Eseguo")
    $.ajax({
        'url' : '/rest_api/VehicleData',
        'type' : 'GET',
        'data': {
            vehicle: "FG868XN",
            sensor: ["speed","rpm"],
            start_date : startDate,
            end_date : endDate,
        },
        'success' : function(data : Array<Misuration>) {           
            graphData(myChart,data)
            toggleAnimation = false;
        },
        'error' : function(request,error)
        {
            console.log("Error reading data")
        }
    });
} 
function dateEventHandlers(chart : Chart) : void{
    $("#start-date").on("change",function (e){
        startDate = String($("#start-date").val());
        console.log(startDate);
        clearInterval(interval);
        toggleAnimation = true;
        loadData(chart);
        interval = setInterval(() =>{
            loadData(chart);
        },3000);
    });
    $("#end-date").on("change",function (e){
        endDate = String($("#end-date").val());
        clearInterval(interval);
        toggleAnimation = true;
        loadData(chart);
        interval = setInterval(() =>{
            loadData(chart);
        },3000);
    });
}

$(function() {
    // @ts-expect-error
    const myChart = new Chart($("#SpeedRpmChart"),config);
    loadData(myChart);
    dateEventHandlers(myChart);
    interval = setInterval(() =>{
        loadData(myChart);
    },3000);
});