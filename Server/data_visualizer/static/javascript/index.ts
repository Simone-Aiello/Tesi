let speed_values: number[] = [];
let ts: string[] = []
interface Misuration{
    "vehicle": string,
    "sensor": string,
    "data": number,
    "timestamp": string
}
function graphData(data : Array<Misuration>) : void{
    data.forEach((element) =>{
        if (element.sensor === "speed"){
            speed_values.push(element.data)
            ts.push(element.timestamp)
        }
    });
}
function loadData() : void{
    $.ajax({

        'url' : 'http://127.0.0.1:8000/rest_api/VehicleData',
        'type' : 'GET',
        'success' : function(data : Array<Misuration>) {              
            graphData(data)
        },
        'error' : function(request,error)
        {
            console.log("Error reading data")
        }
    });
} 
function initGraph():void{;
    
      const data = {
        labels: ts,
        datasets: [{
          label: 'speed',
          backgroundColor: 'rgb(255, 99, 132)',
          borderColor: 'rgb(255, 99, 132)',
          data: speed_values,
        }]
      };
    
      const config = {
        type: 'line',
        data: data,
        options: {}
      };
      const myChart = new Chart(
        document.getElementById('myChart'),
        config
      );
}
$(function() {
    loadData()
    initGraph()
});