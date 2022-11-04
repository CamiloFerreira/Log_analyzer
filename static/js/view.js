function parserDate(str){
	if(str != 'N/A'){
		date = new Date(str)
		d = date.getDate().toString()
		m = date.getMonth()+1
		m  = m.toString()
		y = date.getFullYear()
	
		h = date.getHours().toString()
		min = date.getMinutes().toString()
		s = date.getSeconds().toString()
		
		
		
		if(s.length == 1){
			s = '0'+s
		}
		if(h.length == 1){
			h = '0'+h
		}
		if(m.length == 1){
			m = '0'+m
		}
		if(min.length == 1){
			min = '0'+min
		}
		if(d.length == 1){
			d = '0'+d
		}

		str = d+"-"+m+"-"+y+" "+h+":"+min+":"+s

	}

	return str
}

function filtrar(obj){
  /*
    Filtra los estados del correo

    obj -> obtiene select con el value seleccionado

  */

	var status = obj.value;
	var tbody = $("#dataBody").find('tr')
	
	$("#dataBody tr").each(function(){

		var clase = $(this).attr('class');
		if (clase != status && status != "default")
		{
				$(this).hide();
		}else{
			$(this).show();
		}

	
	})
}
function update(update){
  /*
    Descarga los logs nuevamente y los muestra dentro 
    de la pagina

  */
	values = window.location.search;	
	const urlParams = new URLSearchParams(values);
	var id = urlParams.get('id')
	var id_log = $("#sel_log option:selected").val();
	$.ajax({
		async: true,
		url:'/updateOne',
		data:{'id':id,'id_log':id_log,'descargar':update},
		type:'POST',
		success: function(resp){
			if(resp['status'] == 200){
			 	html = '<div class="alert alert-success" role="alert">'
  	 		html += "Datos cargados! "
		 	  html +='</div>'	
				
				data  = resp['estados']
				count = resp['count']

				table_data = "" 
				for(var i =0 ; i < data.length ; i++){
					table_data += "<tr class='"+data[i]['estado'] +"'>"
					table_data += "<td>" + parserDate(data[i]['fecha']) + "</td>"			
					table_data += "<td>" + data[i]['para'] + "</td>"
					table_data += "<td>" + data[i]['de'] + "</td>"
					table_data += "<td>" + data[i]['estado'] + "</td>"
					table_data += "<td>" + data[i]['relay'] + "</td>"
					table_data +="</tr>"
				}

				$("#sent p").text(count['sent'])
				$("#deferred p").text(count['deferred'])
				$("#bounced p").text(count['bounced'])
				$("#unknown p").text(count['unknown'])

				$("#dataBody").html()
				$("#dataBody").html(table_data)


			}else{
				html = '<div class="alert alert-danger" role="alert">'
  				html += "Ha ocurrido un error cargando , porfavor vuelva a recargar la pagina "
				html +='</div>'	
			}
			
			$("#cont_chart").html('<canvas id="chart" style="width:100%;max-height:200px;"></canvas>')
			viewChart(data)
			$("#reload").prop('disabled', false);
			$("#alerta").html()
			$("#alerta").html(html)
			$("#alerta").hide()

		},
		beforeSend:function(){

			$("#reload").prop('disabled', true);
			html = '<div class="alert alert-warning" role="alert">'
  			html +='<div class="spinner-border spinner-border-sm text-success" role="status">'
			html +=  '<span class="sr-only">Loading...</span>'
			html +='</div>'  			
  			html += " Cargando datos ... "
			html +='</div>'		

			$("#alerta").html()
			$("#alerta").html(html)
			$("#alerta").show()
		}

		,
		error : function(error){
			html = '<div class="alert alert-danger" role="alert">'
  			html += "Ha ocurrido un error cargando , porfavor vuelva a recargar la pagina "
			html +='</div>'		

			$("#alerta").html()
			$("#alerta").html(html)
		}
	})


}





function viewChart(log_data)
{
    var fecha_actual = new Date()
    var aSend = []
    var aBounced = []
    var aLabels = []
    var aDelivered = []

    for ( i in log_data)
    {
      fecha  = new Date(log_data[i]['fecha'])
      relay  = log_data[i]['relay']
      status = log_data[i]['estado']
      to     = log_data[i]['de']

      if(fecha_actual.getDate() == fecha.getDate() && fecha_actual.getMonth() && fecha.getMonth())
      {
        // Analizar el status 
        if ( status == "sent"){
          aSend.push({x: parserDate(log_data[i]['fecha']), y:1})
        }
        
        if (status == "bounced"){
          aBounced.push({x: parserDate(log_data[i]['fecha']), y:1})
        }
        
        if(status == "delivered"){
          aDelivered.push({x: parserDate(log_data[i]['fecha']), y:1})
        }

        aLabels.push(parserDate(log_data[i]['fecha']))
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
