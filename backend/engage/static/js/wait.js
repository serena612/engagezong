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
        response_msg.html("<img class='loading-img' src='/static/img/loading1.gif' /><br>Profile Creation pending...").show();
        else if(e.status==480)
        response_msg.html("<br>Your subscription has ended. Please renew your subscription <a href='/register'>here</a>.").show();
        else if(e.status==0)
        response_msg.html("<img class='loading-img' src='/static/img/loading1.gif' /><br>Request interrupted. Refreshing page...").show();
        else
        response_msg.html('Something went wrong. Please try again later. '+e.status).show();
        //setBtnLoading(btn, false); 
        setTimeout(keepUpdated, 5000);
    });
    //setTimeout(keepUpdated(), 5000);
}
setTimeout(keepUpdated, 5000);