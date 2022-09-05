
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

