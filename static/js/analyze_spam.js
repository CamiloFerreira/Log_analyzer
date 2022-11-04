
$(function (){
	$("#sel_host").change(function(){
		id = $(this).val()
		$.ajax({
			url : "/SpamCheck",
			type:'POST',
			data : {'id':id,'descargar':'false'},
			success : function(res){
				
				data = res['data']
				html = ""
				console.log("Cambiando!..")
				for(var i=0 ; i < data.length ; i++){
					html+= "<tr class="+data[i]['estado']+">"
					html+= "<td>"+data[i]['fecha'] +"</td>"
					html+= "<td>"+data[i]['para'] +"</td>"
					html+= "<td>"+data[i]['de'] +"</td>"
					html+= "<td>"+data[i]['puntaje'] +"</td>"
					html+= "<td>"+data[i]['estado'] +"</td>"
					html+= "<td>"+data[i]['detalle'] +"</td>"
					html+="</tr>" 
				}
				$("#dataBody").html(html)


			},error: function(err){
				console.log(err)


			}
		})
	})



	$("#reload").click(function(){

		var id = $("#sel_host option:selected").val();
		$.ajax({
					url : "/SpamCheck",
					type:'POST',
					data : {'id':id,'descargar':'true'},
					success : function(res){

						html = '<div class="alert alert-success" role="alert">'
			  	 		html += "Datos cargados! "
					 	html +='</div>'	
				


						data = res['data']
						html = ""
						console.log("Actualizando..")
						for(var i=0 ; i < data.length ; i++){
							html+= "<tr class="+data[i]['estado']+">"
							html+= "<td>"+data[i]['fecha'] +"</td>"
							html+= "<td>"+data[i]['para'] +"</td>"
							html+= "<td>"+data[i]['de'] +"</td>"
							html+= "<td>"+data[i]['puntaje'] +"</td>"
							html+= "<td>"+data[i]['estado'] +"</td>"
							html+= "<td>"+data[i]['detalle'] +"</td>"
							html+="</tr>" 
						}
						$("#dataBody").html(html)
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
					}})




	})
})
