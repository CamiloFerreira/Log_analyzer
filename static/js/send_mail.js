
function sendMail(){


    to = $("#to").val()
    subject = $("#asunto").val()
    data = {'subject':subject,'from':"Administrador <contacto@mailercyber2.com","to":to,"content":"asdasdasdasdsddasdasdasd"}

    $.ajax({
        url : "/sendMail",
        type:'POST',
        data : data,
        success : function(res){
        
            console.log(res)
        },
        error: function(err){
                console.log(err)
            }
    })
}

