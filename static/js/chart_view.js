
function viewChart(log_data)
{
    var fecha_actual = new Date()
    var aSend = []
    var aBounced = []
    var aLabels = []
    var aDelivered = []

    for ( i in log_data)
    {
      fecha  = new Date(log_data[i]['Date'])
      relay  = log_data[i]['Relay']
      status = log_data[i]['Status']
      to     = log_data[i]['To']

      if(fecha_actual.getDate() == fecha.getDate() && fecha_actual.getMonth() && fecha.getMonth())
      {
        // Analizar el status 
        if ( status == "sent"){
          aSend.push({x: parserDate(log_data[i]['Date']), y:1})
        }
        
        if (status == "bounced"){
          aBounced.push({x: parserDate(log_data[i]['Date']), y:1})
        }
        
        if(status == "delivered"){
          aDelivered.push({x: parserDate(log_data[i]['Date']), y:1})
        }

        aLabels.push(parserDate(log_data[i]['Date']))
      }
    

    }

    var data = {
      datasets:[
        {
              label: 'Send',
              data: aSend,
              backgroundColor: 'rgba(0, 0, 255, 0.2)', // Color de fondo
            //borderColor: 'rgba(0, 0, 255, 1)', // Color del borde
            //borderWidth: 0.1,// Ancho del borde
          },
          {
              label: 'Bounced',
              data: aBounced,
              backgroundColor: 'rgba(255, 0, 0, 0.2)', // Color de fondo
            //borderColor: 'rgba(255, 0, 0, 1)', // Color del borde
            //borderWidth: 1,// Ancho del borde
          },
          {
              label: 'Delivered',
              data: aDelivered,
              backgroundColor: 'rgba(0, 255, 0, 0.2)', // Color de fondo
            //borderColor: 'rgba(0, 255, 0, 1)', // Color del borde
            //borderWidth: 1,// Ancho del borde
          }
      ]
    }

  var text = "Estadisticas de hoy , Correos enviados :" + aSend.length + " Correos rebotados :"+ aBounced.length 
  new Chart(document.getElementById("chart"), 
  {
      type: 'line',
      data: data,
      options: {
          responsive: true,
          plugins: {
          legend: 
          {
            position: 'top',
          },
          title: {
            display: true,
            text: text
          }
        }
  }
  });

}
