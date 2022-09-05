function cambiar(elem){
	
	var value = elem.value;
	$('#lines option[value="100"]').attr("selected", true);
	$('#sel_log option[value="0"]').attr("selected", true);
	descargarLog(value,0,100)
}

function cambiar_log(elem) {
	var log = elem.value

	var hostname = $("#sel_serv option:selected").val()
	$('#lines option[value="100"]').attr("selected", true);

	descargarLog(hostname,log,100)

}




window.onload = function(){
	
	descargarLog(0,0,100)

}


function descargarLog(id,log,cantidad){
	$.ajax({
		url : "/getLog",
		type:'POST',
		data : {'id':id,'log':log},
		success : function(res){
		
			
			html = '<div class="alert alert-success" role="alert">'
  			html += "Datos cargados!!"
			html +='</div>'
			

			tabla_html = ""

			var run = true
			var i = 0

			if (res['data'][i] < cantidad || cantidad == "all"){
				cantidad = res['data'].length
				console.log("estoy aqui",cantidad)
			}

			while ( run){


				tabla_html += "<tr>"
				tabla_html += "<th class='scope'>"+ (i+1) + "</th>"
				tabla_html += "<td><p>"+ res['data'][i] + "</p></td>"
				tabla_html +="</tr>"
				

				i +=1
				if( i == cantidad){
					run = false
				}

			}

			$("#tbody").html()
			$("#tbody").html(tabla_html)
			$("#alerta").html(html)
		},
		beforeSend:function(){

			document.getElementById("sel_log").disabled = false
			html = '<div class="alert alert-warning" role="alert">'
  			html += "Cargando datos .. "
			html +='</div>'		

			$("#alerta").html(html)
		},
		error: function(err){
			console.log(err)
		}
	})
}

function cargar_mas(elem){
	var cantidad = elem.value
	var hostname = $("#sel_serv option:selected").val()
	var log      = $("#sel_log option:selected").val()


	descargarLog(hostname,log,cantidad)
}