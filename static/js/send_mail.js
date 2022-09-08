


$(document).ready(function(){
    var myEditor ; 
    ClassicEditor
        .create( document.querySelector( '#editor' ) )
        .then( editor =>{
            console.log("Esta iniciado")
            myEditor = editor
        })
        .catch( error => {
            console.error( error );
        } );
        


    $("#submit").click(function(){
        send= true;
        to = $("#to").val();
        subject = $("#asunto").val();
        text = myEditor.getData();
        from = $("#from").val()

        data = {'subject':subject,'from':from,"to":to,"content":text};
   
        for( col in data){
            if(data[col].length == 0){
                send = false
            }
        }

        console.log(send)
        
        if(send){
                $.ajax({
                    url : "/sendMail",
                    type:'POST',
                    data : data,
                    success : function(res){
                        html = '<div class="alert alert-success" role="alert">'
                        html += "Correo enviado! "
                        html +='</div>' 
                        $("#alerta").html(html)
                       
                    },
                    error: function(err){
                        html = '<div class="alert alert-danger" role="alert">'
                        html += "Ha ocurrido un error :( "
                        html +='</div>' 
                        $("#alerta").html(html)
                    },beforeSend:function(){

                        html = '<div class="alert alert-warning" role="alert">'
                        html +='<div class="spinner-border spinner-border-sm text-success" role="status">'
                        html +=  '<span class="sr-only">Loading...</span>'
                        html +='</div>'             
                        html += " Enviando correo ... "
                        html +='</div>'     
                         $("#alerta").html(html)
                    }
                })

        }else{
            html = '<div class="alert alert-danger" role="alert">'
            html += "Debe llenar todos los datos antes de enviar!! "
            html +='</div>' 
            $("#alerta").html(html)
        }



        })










})




