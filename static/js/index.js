
function filtrar(obj){


	var status = obj.value;
	console.log(status)
	
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

function parserDate(str){

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
	return d+"-"+m+"-"+y+" "+h+":"+min+":"+s
}
function parserDate_2(str){

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
	return h+":"+min+":"+s
}
function redirigir(id){
	window.location.href = "/view?id="+id;
}
function test(){

	var data = {
		'user' : document.querySelector("[name='user']").value,
		'password':document.querySelector("[name='password']").value,
		'ip':document.querySelector("[name='ip']").value
	}

	if(data['user'] != '' && data['password'] != '' && data['ip'] != ''){		
		$.ajax({
			url : "/checkConnection",
			type:'POST',
			data : data,
			success : function(res){
		
				if(res['respuesta']['conexion'] == 'OK'){
					html = '<div class="alert alert-success" role="alert">'
  					html += "Conexion correcta!!"
			    	html +='</div>'

			    	document.getElementById("submit").disabled = false
				}else{
					html = '<div class="alert alert-danger" role="alert">'
  					html += res['respuesta']['conexion']
			    	html +='</div>'					
				}


			    $("#alerta").html()
				$("#alerta").html(html)
			},
			beforeSend:function(){
				html = '<div class="alert alert-warning" role="alert">'
  				html += "Comprobando conexion ... "
			    html +='</div>'		

			    $("#alerta").html()
				$("#alerta").html(html)
			}
			,
			error: function(err){
				console.log(err)
			}
		})

	}else{
		html = '<div class="alert alert-danger" role="alert">'
  		html += "Debes llenar todos los datos!"
		html +='</div>'
		
		$("#alerta").html()
		$("#alerta").html(html)	
	}
}

function addDomain(){
	$("#alerta").html()
	$("#myModal").modal("show");
}

function updateAll() {

	var aID = []
	$(".hosts").each(function(index,elem){
		aID.push(index)
	})

	console.log(aID)
	$.ajax({
		async: true,
		url:'/updateLog',
		data:{'id':aID},
		type:'POST',
		success: function(resp){
			console.log(resp)


			if(resp['status'] == 200){
				html = '<div class="alert alert-success" role="alert">'
  				html += "¡Archivos descargados! " //+ dominio
				html +='</div>'	
			}else{
				html = '<div class="alert alert-danger" role="alert">'
  				html += "Ha ocurrido un error cargando , porfavor vuelva a recargar la pagina "
				html +='</div>'	
			}
			
			$("#alert_datos").fadeOut()
			$("#reload").prop('disabled', false);
			$("#alerta_datos").html(html)
			$("#alert_datos").fadeIn()
		},
		beforeSend:function(){

			$("#reload").prop('disabled', true);
			html = '<div class="alert alert-warning" role="alert">'
  			html +='<div class="spinner-border spinner-border-sm text-success" role="status">'
			html +=  '<span class="sr-only">Loading...</span>'
			html +='</div>'  			
  			html += " Descargando archivos , espere un momento " //+ dominio
			html +='</div>'		
			
			$("#alert_datos").fadeOut()
			$("#alerta_datos").html(html)
			$("#alerta_datos").fadeIn()
		}

		,
		error : function(error){
			html = '<div class="alert alert-danger" role="alert">'
  			html += "Ha ocurrido un error cargando , porfavor vuelva a recargar la pagina "
			html +='</div>'		

			$("#alerta_datos").html(html)
		},
	})


	$("#alert_datos").hide()
}

function update(){
	values = window.location.search;	
	const urlParams = new URLSearchParams(values);
	var id = urlParams.get('id')
	$.ajax({
		async: true,
		url:'/updateLog',
		data:{'id':id},
		type:'POST',
		success: function(resp){
			console.log(resp)

			if(resp['status'] == 200){
				html = '<div class="alert alert-success" role="alert">'
  				html += "Datos cargados! "
				html +='</div>'	
				
				data  = resp['data']
				count = resp['count']

				table_data = "" 
				for(var i =0 ; i < data.length ; i++){
					
					table_data += "<tr class="+data[i]['Satus'] +">"
					table_data += "<td>" + parserDate(data[i]['Date']) + "</td>"			
					table_data += "<td>" + data[i]['To'] + "</td>"
					table_data += "<td>" + data[i]['Status'] + "</td>"
					table_data += "<td>" + data[i]['Relay'] + "</td>"
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
			viewChart(resp['data'])
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