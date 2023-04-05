$(function () {
    //load last played games on page load
    getLastPlayedGames(user_uid, $(".last-played-games-box .imgs-box"), $(".last-played-games-box").data("min-size"));
    //load joined tournaments on page load
    getJoinedTournaments(user_uid, $(".joined-tournaments-box .newsbv"), $(".joined-tournaments-box").data("min-size"));
    //load played tournaments on page load
    getPlayedTournaments(user_uid, $(".played-tournaments"), this);
    //load stickers on page load
    getStickers(user_uid, $(".stickers-box .imgs-box"), $(".stickers-box").data("min-size"));
    //load trophies on page load
    getTrophies(user_uid, $(".trophies-box .imgs-box"), $(".trophies-box").data("min-size"));
    //load upcoming tournaments on page load
    getUpcomingTournaments(user_uid,'suggested', '#upcoming-tournaments-list')
    $(".min-tabs li:first-child a").click();
})

// handle tabs links click
var isShowing = false;
$(".tabs li .link-item, .settings-btn").click(function () {
    if (isShowing) return;
    var target = $($(this).attr("data-id"));
    if ($(this).hasClass("is-with-side-friends")) {
        $('.expand-box.expanded').find('.expand-link').click();
    }

    if (target.is(':visible')) return;
    isShowing = true;
    if ($(this).hasClass("is-with-side-friends")) {
        $(".profile-parent-page").addClass("with-side-friends");
    } else {
        $(".profile-parent-page").removeClass("with-side-friends");
    }
     //issue9
     if($(this).attr('data-id')=="#choice-4"){
        $('body').addClass('missionpage'); 
     }
     else{
        $('body').removeClass('missionpage');  
     }
     //
    $(".tabs li .link-item, .settings-btn").removeClass("active")
    $(this).addClass("active")
    $(".page-tab-content").hide();
    target.show();
    isShowing = false;
    if (window.innerWidth < 991) {
        $([document.documentElement, document.body]).animate({
            scrollTop: $($(".profile-parent-page")[0]).offset().top
        }, 300);
    }

    $(".expanded").removeClass("expanded");
    $(".expand-link").html("View All");
})


//#region friends tab
var friends_has_next = false;
var friends_page = 1;
var friends_search = null;
var loading = false;

//get friends end point
function get_friends() {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: '/api/users/' + user_uid + '/friends/',
            headers: {
                "X-CSRFToken": xtoken,
            },
            type: "get",
            data: {
                size: 8,
                page: friends_page,
                search: friends_search
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

//load friends with pagination
function load_friends(pg) {

    if (loading) return;
    loading = true;

    var friends_search_input = $("#friends-search-input").val();
    if (friends_search_input.length > 0) {
        friends_search = friends_search_input;
    } else {
        friends_search = null;
    }
    friends_page = pg;
    get_friends().then(function (data) {
        if (data.next) {
            friends_has_next = true;
            friends_page += 1;
        } else {
            friends_has_next = false;
        }

        $("#friends-list").empty();

        var profile_mg = 'img/profile.png';
        var flag_img = 'img/usa.svg';
        paginator({
            target : document.getElementById("demoB"),
            total :  Math.ceil(data.count / 12),
            current : pg,
            click : load_friends,
            adj : 3
          });
        if (data.results.length >= 1) {
            data.results.map((i) => {
                $("#friends-list").append(`
                    <li data-id="${i && i.friend ? i.friend.uid : ''}">
                        <a href="" class="remove-btn"><i class="fas fa-times"></i></a>
                        <a href="" class="star-btn ${i && i.friend && i.friend.is_favorite  ? 'is-fav' : ''}">
                            <img class="star-false" src="/static/img/star.png" alt="">
                            <img class="star-true" src="/static/img/star-fill.png" alt="">
                        </a>
                        <a class="left" href="/profile/${i && i.friend ? i.friend.uid : ''}">
                            <img src="${i && i.friend  ? i.friend.profile_image : ''}" class="pro-img" alt="">
                            <div class="img">
                                <span class="rank">${big_number(i.friend.level)}</span>
                                <img src="${(i && i.friend && i.friend.avatar) || profile_mg}" alt="">
                            </div>
                        </a>

                        <div class="right2">
                            <div class="ll">
                                <div class="location">
                                    <img src="${(i && i.friend && i.friend.flag) || flag_img}" alt="flag" style="width: 40px"/>
                                </div>
                                <div class="location-cont">
                                    <span class="name">${i.friend.username}</span>
                                   
                                </div>
                            </div>
                            <div class="btns">
                                <a href="/profile/${i && i.friend ? i.friend.uid : ''}" class="btn2 flat">Check Profile</a>
                                <a href='' class="btn2 flat send-coins-btn">`+send_coins+`</a>
                            </div>
                        </div>
                    </li>
                `);
            })
        }
        else{
            $("#friends-list").append('No data found.').css('padding-left','31px');
        }
 
        loading = false;
    }).catch(function (error) {
        console.log(error)
        loading = false;
    });
}
load_friends(1);

//load next page (friends pagination)
$(".profile-contain-friends .friends-list.grid").on("scroll", function () {
    var scrollTop = $(this).scrollTop();
    if ((scrollTop + $(this).innerHeight()) >= (this.scrollHeight - 30)) {
        if (!loading) {
            loading = true;
            if (friends_has_next) {

                get_friends().then(function (data) {
                    if (data.next) {
                        friends_has_next = true;
                        friends_page += 1;
                    } else {
                        friends_has_next = false;
                    }

                    var profile_mg = 'img/profile.png';
                    var flag_img = 'img/usa.svg';

                    if (data.results.length >= 1) {
                        data.results.map((i) => {
                            $("#friends-list").append(`
                                <li data-id="${i?.friend?.uid}">
                                    <a class="left" href="/profile/${i?.friend?.uid}">
                                        <img src="${i?.friend?.profile_image}" class="pro-img" alt="">
                                        <div class="img">
                                            <span class="rank">${big_number(i.friend.level)}</span>
                                            <img src="${i?.friend?.avatar || profile_mg}" alt="">
                                        </div>
                                    </a>

                                    <div class="right2">
                                        <div class="ll">
                                            <div class="location">
                                                <img src="${i?.friend?.flag || flag_img }" alt="flag" style="width: 40px"/>
                                            </div>
                                            <div class="location-cont">
                                                <span class="name">${i.friend.username}</span>
                                            </div>
                                        </div>
                                        <div class="btns">
                                            <a href="/profile/${i?.friend?.uid}" class="btn2 flat">Check Profile</a>
                                        </div>
                                    </div>
                                </li>
                            `);
                        })
                    }

                    loading = false;

                }).catch(function (error) {
                    console.log(error)
                    loading = false;
                });
            }
        }
    }
});


//search friends when user enter some text in the search input
var friends_input_timer = null;
$("#friends-search-input").on("input", function () {
    if (friends_input_timer) clearTimeout(friends_input_timer);
    if ($(this).val().length < 3 && $(this).val().length >= 1) return;

    friends_input_timer = setTimeout(() => {
        friends_has_next = true;
        friends_page = 1;
        loading = false;
        load_friends(1);
    }, 600);
})

//#endregion

//handle add new friend click
$("#add-new-friend").on("click", function () {
    setBtnLoading($(this), true);

    function new_friend() {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: add_new_friend.replace("user_uid", user_uid),
                headers: {
                    "X-CSRFToken": xtoken,
                },
                type: "post",
                data: {},
                error: function (value) {
                    reject(value);
                },
                success: function (value) {
                    resolve(value);
                },
            });
        });
    }

    new_friend().then(function (_) {
        $("#add-friend-button").each(function () {
            this.style.pointerEvents = "none";
        });

        $("#add-friend-button").text("Friend Request Sent");
        $("#add-friend-button").css({
            "background-color": "#5cb85c"
        });
        $("#add-friend-modal").modal("hide");
        setBtnLoading($(this), false);
    }).catch(function (error) {
        $("#add-friend-modal").modal("hide");
        setBtnLoading($(this), false);
    });
});

//handle remove friend click
$("#remove-friend-button").on("click", function () {
    setBtnLoading($(this), true);

    function delete_friend() {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: remove_friend.replace("user_uid", user_uid),
                headers: {
                    "X-CSRFToken": xtoken,
                },
                type: "post",
                data: {},
                error: function (value) {
                    reject(value);
                },
                success: function (value) {
                    resolve(value);
                },
            });
        });
    }

    delete_friend().then(function (_) {
        $("#remove-friend-public").each(function () {
            this.style.pointerEvents = "none";
        });

        $("#remove-friend-public").text("Friend Removed");
        $("#remove-friend-public").css({
            "background-color": "#5cb85c"
        });
        $("#remove-friend-modal").modal("hide");
        setBtnLoading($(this), false);
    }).catch(function (error) {
        $("#remove-friend-modal").modal("hide");
        setBtnLoading($(this), false);
    });
});