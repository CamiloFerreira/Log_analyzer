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
    $("#test").click(function(){   
        id_alerta = "#alerta_2"
        send= true;
        
        smtp = $("#smtp").val()
        from = $("#from").val()
        user = $("#user").val()
        pass = $("#password").val()
        to = $("#test_mail").val()
        subject = "Prueba de envio de correo - Log Analyzer"
        text = "<h1> Felicidades !! </h1> <br> <p>Este correo ha llegado con exito , por favor sigue probando esta herramienta!!!.</p>"
        
        
        data = {'host':smtp,'user':user,'password':pass,'subject':subject,'from':from,"to":to,"content":text};
       
        for( col in data){
            if(data[col].length == 0){
                send = false
            }
        }   
        if(send){
            $.ajax({
                url : "/sendMail_test",
                type:'POST',
                data : data,
                success : function(res){
                    
                    html = '<div class="alert alert-success" role="alert">'
                    html += "Correo enviado! "
                    html +='</div>' 
                    if( res['status'] == 'ERROR'){
                        html = '<div class="alert alert-danger" role="alert">'
                        html += res['msj']
                        html +='</div>' 
                                       
                    }

                    $(id_alerta).html(html)
                   
                },
                error: function(err){
                    html = '<div class="alert alert-danger" role="alert">'
                    html += "Ha ocurrido un error :( "
                    html +='</div>' 
                    $(id_alerta).html(html)
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
            $(id_alerta).html(html)
        }
    })

    $("#send_mail").click(function(){
        sendMail("#alerta",myEditor)
    })
})



function sendMail(id_alerta,myEditor){

    send= true;


    to = $("#to").val();
    subject = $("#asunto").val();
    text = myEditor.getData();
    from = $("#from_2").val()


    test_mail = $("#test_mail").val()
    
    data = {'subject':subject,'from':from,"to":to,"content":text};
    console.log(data)
    for( col in data){
        if(data[col].length == 0){
            send = false
        }
    }
    data['test_mail'] = test_mail
        
    if(send){

        console.log("Mandando correo .....")
        $.ajax({
            url : "/sendMail",
            type:'POST',
            data : data,
            success : function(res){
                html = '<div class="alert alert-success" role="alert">'
                html += "Correo enviado! "
                html +='</div>' 
                $(id_alerta).html(html)
               
            },
            error: function(err){
                html = '<div class="alert alert-danger" role="alert">'
                html += "Ha ocurrido un error :( "
                html +='</div>' 
                $(id_alerta).html(html)
            },beforeSend:function(){

                html = '<div class="alert alert-warning" role="alert">'
                html +='<div class="spinner-border spinner-border-sm text-success" role="status">'
                html +=  '<span class="sr-only">Loading...</span>'
                html +='</div>'             
                html += " Enviando correo ... "
                html +='</div>'     
                 $(id_alerta).html(html)
            }
        })

    }else{
        html = '<div class="alert alert-danger" role="alert">'
        html += "Debe llenar todos los datos antes de enviar!! "
        html +='</div>' 
        $(id_alerta).html(html)
    }
}



