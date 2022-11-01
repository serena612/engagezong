var times = 0;
function CheckStatus(data) {

    return new Promise((resolve, reject) => {
        $.ajax({
            url: '/api/auth/reload_data/',
            
            headers: {
                "X-CSRFToken": xtoken,
            },
            type: "post",
            data: {
                msisdn: data.msisdn,
                idnetwork: data.idnetwork
            },
            error: function (value) {
                reject(value);
            },
            success: function (value) {
                resolve(value);
            },
        });
    });
}

var tt=0;
function showloader(){
$("#wait-modal .msg").removeClass("d-none");       
        $(".please_wait").addClass("d-none");
         $(".waitText").addClass("d-none");
         $(".errico").addClass("d-none");
         $(".preload").removeClass("d-none");
}
function hideloader(){
$("#wait-modal .msg").removeClass("d-none");          
        $(".please_wait").addClass("d-none");
         $(".waitText").removeClass("d-none");
         $(".errico").removeClass("d-none");
         $(".preload").addClass("d-none");
         $(".is_updated").addClass("d-none");
}
function keepUpdated() {
    times += 1;
    // console.log("times = "+times);
    if (times>50){
        // response_msg.html("<img class='loading-img' src='/static/img/loading1.gif' /><br>Your request is under process. Please check back later. <a href='/'>Refresh</a>").show();
       /////// clearInterval(tt);
        response_msg.html("Your request is under process. Please check back later.").show();  //  <a href='/'>Refresh</a>
        showloader();
        return;}
    // console.log("Updating using token "+xtoken);
    data = {}
    data.msisdn = usermobile; // $(".user_mobile").text();
    // console.log(usermobile);
    // important must add header check here
    data.idnetwork = '1';
    response_msg = $('.sub_status');
    CheckStatus(data).then(res => {
        //setBtnLoading(btn, false);
        //$(".login-otp-form").show(); //invisible
        response_msg.html("Subscription Success !").show();
        hideloader();
        $("#wait-modal").find(".success-bd").removeClass("d-none");
        window.location.href = '/clear'
    }).catch(e => {
        if(e.status==472){ //invisible
        response_msg.html('The number you have provided is invalid!').show();
        hideloader();
        $("#wait-modal").find(".error-bd").removeClass("d-none"); }
        else if(e.status==475){
        response_msg.html("Subscription Request pending...").show();
        showloader();}
        else if(e.status==476){
        response_msg.html("Unsubscription Request pending...").show();
        showloader();}
        else if(e.status==456){
        if (times<5){
        response_msg.html("Profile Creation pending...").show();
        showloader();}
        else{//invisible
        response_msg.html("Subscription Failed. Please <a href='/register'>try again</a>.").show();
        hideloader();
        $("#wait-modal").find(".error-bd").removeClass("d-none"); 
        return
        }}
        else if(e.status==480){//invisible
        response_msg.html("Your subscription has ended. Please renew your subscription <a href='/register'>here</a>.").show();
        hideloader();
        $("#wait-modal").find(".error-bd").removeClass("d-none"); 
        return
        }
        else if(e.status==0){
        response_msg.html("Request interrupted. Refreshing page...").show();
        showloader();}
        else{
        response_msg.html('Something went wrong. Please try again later.').show();  // + +e.status  //invisible
        hideloader();
        $("#wait-modal").find(".error-bd").removeClass("d-none"); 
        return;}
        //setBtnLoading(btn, false); 

//         $("#wait-modal .preload").addClass("d-none");

//    ////////////////////// tt = setInterval(() => {
         
//         var statusW = $(".sub_status").html();
//         if(statusW != "" && statusW == "Subscription Success !")
//         {
//             $("#wait-modal .msg").removeClass("d-none");  
//             $("#wait-modal").find(".error-bd").addClass("d-none");  
//             $("#wait-modal").find(".success-bd").removeClass("d-none");          
//             $(".please_wait").addClass("d-none");
//            //////////////////// clearInterval(t);
//         } 
//         else if(statusW != "" && statusW != "Subscription Success !")
//         {
//             $("#wait-modal .msg").removeClass("d-none");  
//             $("#wait-modal").find(".error-bd").removeClass("d-none");  
//             $("#wait-modal").find(".success-bd").addClass("d-none");          
//             $(".please_wait").addClass("d-none");
//             ////////////clearInterval(t);
//         } 
         
    /////////////////////}, 50);

        setTimeout(keepUpdated, 5000);
    });
    //setTimeout(keepUpdated(), 5000);
   

    
}
setTimeout(keepUpdated, 5000);