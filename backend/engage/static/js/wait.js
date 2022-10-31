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

function keepUpdated() {
    times += 1;
    // console.log("times = "+times);
    if (times>50){
        response_msg.html("<img class='loading-img' src='/static/img/loading1.gif' /><br>Your request is under process. Please check back later. <a href='/'>Refresh</a>").show();
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
        //$(".login-otp-form").show();
        response_msg.html("Subscription Success !").show();
        window.location.href = '/clear'
    }).catch(e => {
        if(e.status==472) //406 ?
        response_msg.html('The number you have provided is invalid!').show();
        else if(e.status==475)
        response_msg.html("<img class='loading-img' src='/static/img/loading1.gif' /><br>Subscription Request pending...").show();
        else if(e.status==476)
        response_msg.html("<img class='loading-img' src='/static/img/loading1.gif' /><br>Unsubscription Request pending...").show();
        else if(e.status==456)
        if (times<5)
        response_msg.html("<img class='loading-img' src='/static/img/loading1.gif' /><br>Profile Creation pending...").show();
        else{
        response_msg.html("<br>Subscription Failed. Please <a href='/register'>try again</a>.").show();
        return
        }
        else if(e.status==480){
        response_msg.html("<br>Your subscription has ended. Please renew your subscription <a href='/register'>here</a>.").show();
        return
        }
        else if(e.status==0)
        response_msg.html("<img class='loading-img' src='/static/img/loading1.gif' /><br>Request interrupted. Refreshing page...").show();
        else
        response_msg.html('Something went wrong. Please try again later.').show();  // + +e.status
        //setBtnLoading(btn, false); 
        setTimeout(keepUpdated, 5000);
    });
    //setTimeout(keepUpdated(), 5000);
    var t = setInterval(() => {
         
        var statusW = $(".sub_status").html();
        if(statusW != "" && statusW == "Subscription Success !")
        {
            $("#wait-modal .preload").addClass("d-none");
            $("#wait-modal .msg").removeClass("d-none");  
            $("#wait-modal").find(".error-bd").addClass("d-none");  
            $("#wait-modal").find(".success-bd").removeClass("d-none");          
            $(".please_wait").addClass("d-none");
            clearInterval(t);
        } 
        else if(statusW != "" && statusW != "Subscription Success !")
        {
            $("#wait-modal .preload").addClass("d-none");
            $("#wait-modal .msg").removeClass("d-none");  
            $("#wait-modal").find(".error-bd").removeClass("d-none");  
            $("#wait-modal").find(".success-bd").addClass("d-none");          
            $(".please_wait").addClass("d-none");
            clearInterval(t);
        } 
         
    }, 50);

    
}
setTimeout(keepUpdated, 5000);