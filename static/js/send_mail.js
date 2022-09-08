


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
  
    to = $("#to").val();
    subject = $("#asunto").val();
    text = myEditor.getData();
    from = $("#from").val()

    data = {'subject':subject,'from':from,"to":to,"content":text};
   

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

})










})




