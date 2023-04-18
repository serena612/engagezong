(function($) {
    $(function() {
        CalculateTimes();
        //$('.field-winners').find('select').select2();
        //     templateSelection: function(selected, total) {
        //       return "Selected " + selected.length + " of " + total;
        //     }
        //   });
        //   $('.field-participants').find('select').select2MultiCheckboxes({
        //     templateSelection: function(selected, total) {
        //       return "Selected " + selected.length + " of " + total;
        //     }
        //   });
        $(document).ready(function() {
            $('#tournamentmatch_set-group').find('.errorlist').css('margin-left', '220px');
            $('#tournamentmatch_set-group').find('.errorlist').prepend('<br>')
            $('.field-winners').find('select').multiselect({
                includeSelectAllOption: true,
                enableFiltering: true,
                buttonWidth: '360px',
                maxHeight: 250,
                enableCaseInsensitiveFiltering: true,
                });
            $('.field-winners.form-row').attr('style', 'Overflow: visible');
            $('.field-winners').find('.select2-container').hide();
            $('.field-winners').find('.select2-container').css('display', 'none');
            $('.field-participants').find('select').multiselect({
                includeSelectAllOption: true,
                enableFiltering: true,
                buttonWidth: '360px',
                maxHeight: 250,
                enableCaseInsensitiveFiltering: true,
            });
            $('.field-participants.form-row').attr('style', 'Overflow: visible');
            $('.field-participants').find('.select2-container').hide();
            $('.field-participants').find('.select2-container').css('display', 'none');
            $(this).find('input[type="button"][value="Autofill"]').click(function(e) {
                // $('.multiselect.dropdown-toggle').each(function(){
                //     $(this).multiselect('updateButtonText');
                // })
                $('.field-participants').find('select').multiselect('refresh');
                $('.submit-row').find('input[name="_continue"]').trigger('click');
                $('.submit-row').find('input[name="_save"],input[name="_addanother"],input[name="_continue"]').prop('disabled', true);
                $('input[type="button"][value="Autofill"]').prop('disabled', true);
            });
            // $('.add-row').click(function(e) {
            //     setTimeout(function(){
            //         $('.field-winners').find('.select2-container').hide();
            //         $('.field-winners').find('.select2-container').css('display', 'none');
            //         $('.field-participants').find('.select2-container').hide();
            //         $('.field-participants').find('.select2-container').css('display', 'none');
            //     },1000)
            // });
            function stoperror(err) {
                return true;
             }
            $('.add-row').click(function(e) {
                try{
                $('input[id^="id_tournamentmatch_set-"][id$="start_date_0"],input[id^="id_tournamentmatch_set-"][id$="start_date_1"]').unbind('change',gigi);
                }
                catch(err){
                  stoperror(err);  
                }
                $('input[id^="id_tournamentmatch_set-"][id$="start_date_0"],input[id^="id_tournamentmatch_set-"][id$="start_date_1"]').change(function gigi() {
                    CalculateTimes();
                    CheckTimes();
                });
            });
        });
        $('.field-free_open_date,.field-open_date,.field-start_date,.field-close_date,.field-end_date').addClass('inline');
$('#id_time_compared_to_gmt').attr('placeholder','i.e +2 or -5');
        $('#id_time_compared_to_gmt,#id_label_next_time,#id_open_date_0,#id_open_date_1,#id_free_open_date_0,#id_free_open_date_1,#id_close_date_0,#id_close_date_1,#id_start_date_0,#id_start_date_1,#id_end_date_0,#id_end_date_1').change(function() {
            CalculateTimes();
            CheckTimes();
        });
        $('input[id^="id_tournamentmatch_set-"][id$="start_date_0"],input[id^="id_tournamentmatch_set-"][id$="start_date_1"]').change(function gigi() {
            CalculateTimes();
            CheckTimes();
        });
        if(window.location.href.indexOf('inline_0')!=-1){
            setTimeout(function(){$('.changeform-tabs-item').eq(1).click();},1000)
        }

        // $(document).keydown(function(e) {
        //     if (e.keyCode === 8 && $('.changeform-tabs-item').eq(1).hasClass('selected') && $(document.activeElement).hasClass('select2-search__field')) {
                
        //         e.preventDefault();
        //         e.stopPropagation();
        //         return false;
        //     };
        // });

        // $(".field-winners ul").keydown(function (e) {
        //     var key = e.keyCode || e.charCode;
        //     if (key == 8 || key == 46) {
        //         e.preventDefault();
        //         e.stopPropagation();
        //         return false;
        //     }
        // });

        // $(document).keypress(function(e){ 
        //     if (e.keyCode === 8 && $('.changeform-tabs-item').eq(1).hasClass('selected') && $(document.activeElement).hasClass('select2-search__field')) {
        //         e.preventDefault();
        //         e.stopPropagation();
        //         return false;
        //     };
        // });
        
        $('.field-closed_on').hide();   
        $('.field-started_on').hide();
        if($('#id_started_on_0').val()==""){

            var len =  $('.field-winners').length;
            $('.field-winners').each(function(ind){
                $(this).click(function(ind1){  // $(this).find('.select2-container').click(function(ind1){
                    // console.log("clicked !!")
                    if(!$(this).find('.chk_winners').length>0){
                        $('.field-winners').eq(ind).addClass('errors')
                        if(!$('.field-winners').eq(ind).find('.select2-container').parents('.related-widget-wrapper').find('.chk_winners').length>0){
                            $('.field-winners').eq(ind).find('.select2-container').parents('.related-widget-wrapper').prepend("<p class='chk_winners'>Winners can't be selected without starting the tournament!</p>" );
                        }
                        setTimeout(function(){ 
                            for(var i =0;i<len;i++){
                                $('#select2-id_tournamentmatch_set-'+i+'-winners-results').parents('.select2-container--open').find('.select2-buttons').addClass('input_freeze');
                                $('#select2-id_tournamentmatch_set-'+i+'-winners-results').addClass('input_freeze');
                                $('.field-winners').eq(ind).find('button').addClass('input_freeze');
                            }
                        },50);
                       
                      
                    }
                });
            });
        }
 

        $('#tournament_form').find('.changeform-tabs-item').each(function(){
            $(this).click(function(){
                    // can't select winner prize before filling all match winners
                    $('#tournamentprize_set-group').find('.field-winner').addClass('input_freeze');
                    var valid=true;
                    if($('#tournamentmatch_set-group').find('.inline-related').length<=1){
                        valid=false;
                        $('#tournamentprize_set-group').find('.field-winner').find('select').val("");
                        $('#tournamentprize_set-group').find('.field-winner').find('.select2-selection__rendered').attr('title','');
                        $('#tournamentprize_set-group').find('.field-winner').find('.select2-selection__rendered').text('');
                        return;
                    }
                    $('#tournamentmatch_set-group').find('.inline-related').each(function(){
                        if($(this).find('.field-match_name').find('input').val()!="" && $(this).find('.field-winners').find('.select2-selection__choice').length==0){
                            valid=false;
                            $('#tournamentprize_set-group').find('.field-winner').find('select').val("");
                            $('#tournamentprize_set-group').find('.field-winner').find('.select2-selection__rendered').attr('title','');
                            $('#tournamentprize_set-group').find('.field-winner').find('.select2-selection__rendered').text('');
                            return;
                        }
                    })
                    if(valid){
                        $('#tournamentprize_set-group').find('.field-winner').removeClass('input_freeze');
                        //hide delete from matches 
                        var matches = $('#tournamentmatch_set-group').find('.inline-related').length;
                        for(indice=0;indice<matches;indice++){
                            round = $('#id_tournamentmatch_set-'+indice+'-round_number').val();
                            if(round!="" && parseInt(round) >1){
                                $('#tournamentmatch_set-group').find('.select2-selection__choice__remove').remove();
                                return;
                            }
                        }
                        
                        //
                    }
            })
        })

        $('#tournamentmatch_set-group').find('.inline-related').each(function(ind){
            if(ind>0){
                $('#tournamentmatch_set-group').find('.inline-related').eq(ind).find('.field-winners .select2-container').click(function(){
                    if($('#tournamentmatch_set-group').find('.inline-related').eq(ind-1).find('.select2-selection__choice').length==0 && $('#id_started_on_0').val()!=""){
                        $(this).parents('.field-winners').addClass('errors');
                        $(this).parents('.related-widget-wrapper').prepend("<p class='chk_winners'> Winners of previous round shall be selected to proceed!</p>" );
                        $('#select2-id_tournamentmatch_set-'+ind+'-winners-results').parents('.select2-container--open').find('.select2-buttons').addClass('input_freeze');
                        $('#select2-id_tournamentmatch_set-'+ind+'-winners-results').addClass('input_freeze');
                       
                    }
                    else{
                        var previous_round = $('#id_tournamentmatch_set-'+(ind-1)+'-round_number').val();
                        var round  = $('#id_tournamentmatch_set-'+ind+'-round_number').val();
                        if($('#id_started_on_0').val()!="" && $('#tournamentmatch_set-group').find('.inline-related').eq(ind-1).find('.select2-selection__choice').length>0 && previous_round!="" && round!="" && parseInt(previous_round) < parseInt(round)){
                            $(this).parents('.field-winners').removeClass('errors');
                            $(this).parents('.related-widget-wrapper').find('.chk_winners').remove();
                            $('#select2-id_tournamentmatch_set-'+ind+'-winners-results').parents('.select2-container--open').find('.select2-buttons').removeClass('input_freeze')
                            $('#select2-id_tournamentmatch_set-'+ind+'-winners-results').removeClass('input_freeze');
                            var current_round = $('#id_tournamentmatch_set-'+ind+'-round_number').val();
                            //disable delete btn for previous rounds
                            for(indice=0;indice<ind;indice++){
                                $('#select2-id_tournamentmatch_set-'+indice+'-winners-results').find('.select2-selection__choice__remove').remove();
                                var new_round = $('#id_tournamentmatch_set-'+indice+'-round_number').val();
                                if(current_round!="" && new_round<current_round){
                                    $('#id_tournamentmatch_set-'+indice+'-winners').parents('.related-widget-wrapper').find('.select2-selection__choice__remove').remove();
                                }
                            }
                            //
                        }
                        
                    }
                });
                }
            
        })

        var isSponsoredSelect = $('#id_is_sponsored');
        var gameOptionSelect = $('#id_game');

        var freeUserInput = $('#id_allow_free_users');
        var roundRobinInput = $('#id_rounds_number');

        var freeUserField = $('.field-allow_free_users');
        var roundRobinField = $('.field-rounds_number');
        var sponsored_by = $('.field-sponsored_by');

        // $('.field-match_name,.field-round_number,.field-inform_participants,.field-position,.field-prize_type,.field-image,.field-,.field-top_image').addClass('d-inline');
        $('.field-coins_per_participant,.field-give_sticker').addClass('inline');
        $('.field-max_participants,.field-regions,.field-time_compared_to_gmt,.field-label_next_time').addClass('inline');
        $('.field-rounds_number,.field-game,.field-minimum_profile_level,.field-name').addClass('inline');
        // $('<div class="row">').insertBefore($('.field-name'));
        // $('</div>').after($('.field-name'));
        // $('<div class="row">').insertBefore($('.field-image'));
        // $('</div>').after($('.field-image'));
        $('<div class="row">').insertBefore($('.field-give_sticker'));
        $('</div>').after($('.field-give_sticker'));
        $('<div class="row">').insertBefore($('.field-regions'));
        $('</div>').after($('.field-regions'));
        
        function resize(){
        $('.field-description').find('.cke_contents').css('height', '150px');
        $('.field-rules').find('.cke_contents').css('height', '150px');
        $('.field-pool_prize').find('.cke_contents').css('height', '150px');
        
        }
        $(document).ready(function($) {
            setTimeout(resize, 2000);
        });
    
        $('.errors.form-row').each(function(ind){
            
            var gagaga = $(this);
            gagaga.on('change','input, select, textarea', function gigi(){
                gagaga.removeClass('errors');
                gagaga.removeClass('d-inline');
                gagaga.find('ul.errorlist').hide();
                gagaga.unbind('change',gigi);
            })
        })
        let value = isSponsoredSelect.val()
        if (!isSponsoredSelect.is(':checked')) {
            freeUserInput.empty()
            freeUserField.hide()
            sponsored_by.hide()
        }
        isSponsoredSelect.on('change', function () {
            const value = isSponsoredSelect.val()

            if (!this.checked) {
                freeUserInput.attr('checked', false)
                freeUserField.hide()
                sponsored_by.hide()
            } else {
                freeUserField.css('display','inline-block');
                sponsored_by.css('display','inline-block');
            }
        });

        value = $('#id_game option:selected').text()
        if (value.startsWith('[Team-Based]')) {
            roundRobinInput.val(1)
            roundRobinField.hide()
        }
        gameOptionSelect.on('select2:select', function (e) {
            const value = $('#id_game option:selected').text()

            // console.log(value)
            if (value.startsWith('[Team-Based]')) {
                roundRobinInput.val(1)
                roundRobinField.hide()
            } else {
                roundRobinField.show()
            }
        });

        
        function getMatchesPerRound(round){
            var number=0;
            $('#tournamentmatch_set-group').find('.inline-related').each(function(ind){
                var roundi = $('#id_tournamentmatch_set-'+ind+'-round_number').val();
                if(roundi==round)
                number++;
            })
            return number;
        }
        

        function CalculateTimes(){
            if($('#id_time_compared_to_gmt').val()==0)
            {
               $('.data').text(""); 
               return;
            }
            if($('#id_open_date_0').val()!="" && $('#id_open_date_1').val()!=""){
                var date = ($('#id_open_date_0').val()+" "+$('#id_open_date_1').val());
                var calculated_date  = moment(date, "YYYY-MM-DD HH:mm:ss").add(parseInt($('#id_time_compared_to_gmt').val()), 'hours').format('YYYY-MM-DD HH:mm:ss');
                $('.field-open_date').find('.data').text(calculated_date+" "+$('#id_label_next_time').val());
            }
            if($('#id_free_open_date_0').val()!="" && $('#id_free_open_date_1').val()!=""){
                var date = ($('#id_free_open_date_0').val()+" "+$('#id_free_open_date_1').val());
                var calculated_date  = moment(date, "YYYY-MM-DD HH:mm:ss").add(parseInt($('#id_time_compared_to_gmt').val()), 'hours').format('YYYY-MM-DD HH:mm');
                $('.field-free_open_date').find('.data').text(calculated_date+" "+$('#id_label_next_time').val());
            }
            if($('#id_close_date_0').val()!="" && $('#id_close_date_1').val()!=""){
                var date = ($('#id_close_date_0').val()+" "+$('#id_close_date_1').val());
                var calculated_date  = moment(date, "YYYY-MM-DD HH:mm:ss").add(parseInt($('#id_time_compared_to_gmt').val()), 'hours').format('YYYY-MM-DD HH:mm');
                $('.field-close_date').find('.data').text(calculated_date+" "+$('#id_label_next_time').val());
            }
            if($('#id_start_date_0').val()!="" && $('#id_start_date_1').val()!=""){
                var date = ($('#id_start_date_0').val()+" "+$('#id_start_date_1').val());
                var calculated_date  = moment(date, "YYYY-MM-DD HH:mm:ss").add(parseInt($('#id_time_compared_to_gmt').val()), 'hours').format('YYYY-MM-DD HH:mm');
                $('.module_0 .field-start_date').find('.data').text(calculated_date+" "+$('#id_label_next_time').val());
            }
            if($('#id_end_date_0').val()!="" && $('#id_end_date_1').val()!=""){
                var date = ($('#id_end_date_0').val()+" "+$('#id_end_date_1').val());
                var calculated_date  = moment(date, "YYYY-MM-DD HH:mm:ss").add(parseInt($('#id_time_compared_to_gmt').val()), 'hours').format('YYYY-MM-DD HH:mm');
                $('.field-end_date').find('.data').text(calculated_date+" "+$('#id_label_next_time').val());
            }
            $('input[id^="id_tournamentmatch_set-"][id$="start_date_0"]').each(function(ind){
                if($(this).val()!="" && $('#id_tournamentmatch_set-'+ind+'-start_date_1').val()!=""){
                    var date = ($(this).val()+" "+$('#id_tournamentmatch_set-'+ind+'-start_date_1').val());
                    var match_date  = moment(date, "YYYY-MM-DD HH:mm:ss").add(parseInt($('#id_time_compared_to_gmt').val()), 'hours').format('YYYY-MM-DD HH:mm');
                    $(this).parents('.field-start_date').find('.data').text(match_date+" "+$('#id_label_next_time').val());
                }
            });
        }
        function CheckTimes(){
            
            if($('#id_open_date_0').val()!="" && $('#id_open_date_1').val()!=""){
                var date = ($('#id_open_date_0').val()+" "+$('#id_open_date_1').val());
                var open_date  = moment(date, "YYYY-MM-DD HH:mm:ss")
            }
            if($('#id_free_open_date_0').val()!="" && $('#id_free_open_date_1').val()!=""){
                var date = ($('#id_free_open_date_0').val()+" "+$('#id_free_open_date_1').val());
                var free_open_date  = moment(date, "YYYY-MM-DD HH:mm:ss")
            }
            if($('#id_close_date_0').val()!="" && $('#id_close_date_1').val()!=""){
                var date = ($('#id_close_date_0').val()+" "+$('#id_close_date_1').val());
                var close_date  = moment(date, "YYYY-MM-DD HH:mm:ss")
            }
            if($('#id_start_date_0').val()!="" && $('#id_start_date_1').val()!=""){
                var date = ($('#id_start_date_0').val()+" "+$('#id_start_date_1').val());
                var start_date  = moment(date, "YYYY-MM-DD HH:mm:ss")
                if(!tourn_state && start_date.isBefore(moment().add(-(moment().utcOffset()), 'm'))){
                    $('.module_0 .field-start_date').addClass('errors');
                    $('.module_0 .field-start_date').find('ul.errorlist').hide();
                    $('.module_0 .field-start_date').prepend("<ul class='errorlist'> <li>Start Date can't be in the past</li> </ul>" );
                } else {
                    $('.module_0 .field-start_date').removeClass('errors');
                    $('.module_0 .field-start_date').find('ul.errorlist').hide();
                }
            }
            if($('#id_end_date_0').val()!="" && $('#id_end_date_1').val()!=""){
                var date = ($('#id_end_date_0').val()+" "+$('#id_end_date_1').val());
                var end_date  = moment(date, "YYYY-MM-DD HH:mm:ss")
            }
            // Case 1: open and close date
            if(typeof open_date !== 'undefined' && typeof close_date !== 'undefined' && close_date.isBefore(open_date)){
                $('.field-close_date').addClass('errors');
                $('.field-close_date').find('ul.errorlist').hide();
                $('.field-close_date').prepend("<ul class='errorlist'> <li>Close Date must be greater than Open Date</li> </ul>" );
            } 
            // Case 5: close and start date (2hrs diff)
            else if(typeof close_date !== 'undefined' && typeof start_date !== 'undefined' && start_date.diff(close_date, 'hours', true)<=2){
                $('.field-close_date').addClass('errors');
                $('.field-close_date').find('ul.errorlist').hide();
                $('.field-close_date').prepend("<ul class='errorlist'> <li>Close Date must be at least 2 hours earlier than Start Date</li> </ul>" );
            } else {
                $('.field-close_date').removeClass('errors');
                $('.field-close_date').find('ul.errorlist').hide();

            }
            // Case 2: end and start date - working
            if(typeof end_date !== 'undefined' && end_date.isBefore(moment().add(-(moment().utcOffset()), 'm'))){
                $('.field-end_date').addClass('errors');
                $('.field-end_date').find('ul.errorlist').hide();
                $('.field-end_date').prepend("<ul class='errorlist'> <li>End Date can't be in the past</li> </ul>" );
            } else if(typeof end_date !== 'undefined' && typeof start_date !== 'undefined' && end_date.isBefore(start_date)){
                $('.field-end_date').addClass('errors');
                $('.field-end_date').find('ul.errorlist').hide();
                $('.field-end_date').prepend("<ul class='errorlist'> <li>End Date must be greater than Start Date</li> </ul>" );
            } else {
                $('.field-end_date').removeClass('errors');
                $('.field-end_date').find('ul.errorlist').hide();

            }
            // Case 3: open and free open date
            if(typeof open_date !== 'undefined' && typeof free_open_date !== 'undefined' && free_open_date.isBefore(open_date)){
                $('.field-free_open_date').addClass('errors');
                $('.field-free_open_date').find('ul.errorlist').hide();
                $('.field-free_open_date').prepend("<ul class='errorlist'> <li>Public open date cannot be smaller than VIP open date</li> </ul>" );
            }
            // Case 4: close and free open date
            else if(typeof close_date !== 'undefined' && typeof free_open_date !== 'undefined' && free_open_date.isAfter(close_date)){
                $('.field-free_open_date').addClass('errors');
                $('.field-free_open_date').find('ul.errorlist').hide();
                $('.field-free_open_date').prepend("<ul class='errorlist'> <li>Close date cannot be smaller than public open date</li> </ul>" );
            } else {
                $('.field-free_open_date').removeClass('errors');
                $('.field-free_open_date').find('ul.errorlist').hide();

            }
            $('input[id^="id_tournamentmatch_set-"][id$="start_date_0"]').each(function(ind){
                if($(this).val()!="" && $('#id_tournamentmatch_set-'+ind+'-start_date_1').val()!=""){
                    // console.log("Checking"+'#id_tournamentmatch_set-'+ind+'-start_date_1');
                    var date = ($(this).val()+" "+$('#id_tournamentmatch_set-'+ind+'-start_date_1').val());
                    var match_date  = moment(date, "YYYY-MM-DD HH:mm:ss");
                    // console.log(match_date);
                    if(typeof start_date !== 'undefined' && typeof end_date !== 'undefined' && (match_date.isBefore(start_date) || match_date.isAfter(end_date))){
                        console.log("Wrong match date !");
                        $(this).parents('.field-start_date').addClass('errors');
                        $(this).parents('.field-start_date').find('ul.errorlist').hide();
                        $(this).parents('.field-start_date').prepend("<ul class='errorlist'> <li>Match date must be between tournament start date and tournament end date</li> </ul>" );
                    } else {
                        //console.log(match_date.isBefore(start_date));
                        //console.log(match_date.isAfter(end_date));
                        $(this).parents('.field-start_date').removeClass('errors');
                        $(this).parents('.field-start_date').find('ul.errorlist').hide();
                    }
                }
            });
        }
    //     function checkValidationMatch(ind){
    //         var game_model = $('#id_game').val(); 
    //         var rounds_number = $('#id_rounds_number').val();
    //         if(game_model == "3" || game_model == "5"){
    //             var round_number =  $('#id_tournamentmatch_set-'+ind+'-round_number').val();
    //             var matchname = $('#tournamentmatch_set-'+ind+'-match_name').val();
    //             if(matchname!='' && round_number!=''){
    //                 if(round_number == rounds_number && getMatchesPerRound(round_number) > 1){
    //                     alert("Matches Number for round "+ round_number+" must be 1!");
    //                     $('#tournamentmatch_set-'+ind).find('input,select').val("");
    //                     $('#select2-id_tournamentmatch_set-'+ind+'-round_number-container').attr('title','');
    //                     $('#select2-id_tournamentmatch_set-'+ind+'-round_number-container').text('');
    //                 }
    //                 else if(round_number > 1){
    //                     var previous_matches = getMatchesPerRound(round_number-1);
    //                     var current_next_tournament_matches = getMatchesPerRound(round_number);
    //                     var next_round_matches = ((previous_matches/4) >=2 ? (previous_matches/4) : 2);
    //                     if(current_next_tournament_matches >= next_round_matches){
    //                         alert("Matches completed for round number "+ round_number+"!");
    //                     } 
    //                 }
    //             }
    //         }
    //     }
        
    //     $('#tournamentmatch_set-group').find('.inline-related').each(function(ind){
    //     //     checkValidationMatch(ind);
    //     //     $(this).click(function(){
    //     //         checkValidationMatch(ind);
    //     //     })
    //         $('#id_tournamentmatch_set-'+ind+'-round_number').change(function(){
    //             checkValidationMatch(ind);
    //         })
    //    })
    

    });
})(jet.jQuery);
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function postInform(data, formidd) {
    console.log("posting "+data);
    //console.log("xtoken "+xtoken)
    const apiurl = window.location.origin+'/api/tournaments/inform_participants/';
    const touridd = window.location.pathname.split('/')[4];
    const xtoken = getCookie('csrftoken');
    console.log("id "+touridd+" match id "+ formidd);
    return new Promise((resolve, reject) => {
        $.ajax({
            url: apiurl,
            headers: {
                "X-CSRFToken": xtoken,
            },
            type: "post",
            data: {
                participants: data,
                tourid: touridd,
                formid: formidd
                //csrfmiddlewaretoken: data.csrfmiddlewaretoken
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

function download(filename, text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
    }
function exportme(fieldid) {
    var select = document.getElementById(fieldid);
    var result = ""; // [];
    var options = select && select.options;
    var opt;

    for (var i=0, iLen=options.length; i<iLen; i++) {
        opt = options[i];

        if (opt.selected) {
            result+=opt.text; //.push(opt.value || opt.text); 
            result+="\n";
        }
    }
    if (result == "") {
        window.alert("No participants selected!");
    }else{
        download('participants.txt', result);
    }
}
function informme(fieldid) {
    const select = document.getElementById(fieldid);
    //var result = ""; // [];
    const options = select && select.options;
    var opt;
    const topost = new Array();
    const formid = fieldid.split("-")[1];
    // var dicts = filldict();  // this is to get participants of all matches
    // var dictoo = dicts[2];
    // console.log(dictoo);
    // var result = Object.values(dictoo).flat();
    // var topost = [...new Set(result)];
    // console.log(topost);
    // console.log(topost.toString());
    for (var i=0, iLen=options.length; i<iLen; i++) {  // these are for selected match only
        opt = options[i];

        if (opt.selected) {
            topost.push(opt.value); //.push(opt.value || opt.text); 
            //result+="\n";
        }
    }
    const widget = select.closest('.related-widget-wrapper');
    const field = widget.closest('.field-participants');
    const butt = $(field).find('input[type="button"][value="Inform Participants"]');
    butt.addClass('input_freeze');
    if($(field).find('.chk_participants').length>0){
        $(field).find('.chk_participants').html('');
    }
    postInform(topost.toString(), formid).then(res => {
        //form.trigger("reset");
        console.log("Success");
        console.log(res);
        //console.log(field);
        $(field).removeClass('errors');
        butt.removeClass('input_freeze');
        if($(field).find('.chk_participants').length>0){
            $(field).find('.chk_participants').html(res);
        }else{
            $(widget).prepend("<p class='chk_participants'>"+res+"</p>");
        }
        // if(!$(this).find('.chk_winners').length>0){
        //     $('.field-participants').eq(ind).addClass('errors')
        //     if(!$('.field-participants').eq(ind).find('.select2-container').parents('.related-widget-wrapper').find('.chk_winners').length>0){
        //         $('.field-participants').eq(ind).find('.select2-container').parents('.related-widget-wrapper').prepend("<p class='chk_winners'>participants can't be selected without starting the tournament!</p>" );
        //     }
        //         $('.field-participants').eq(ind).find('button').addClass('input_freeze');
        // }
        //$(".sendcodemsg").html('A pin code has been sent to you. Please enter the pin code to proceed.').show();       

    }).catch(e => {
        console.log("Failed");
        console.log(e);
        butt.removeClass('input_freeze');
        $(field).addClass('errors');
        if($(field).find('.chk_participants').length>0){
            $(field).find('.chk_participants').html(e);
        }else{
            $(widget).prepend("<p class='chk_winners'>"+e+"</p>");
        }
        //response_msg.html('Something went wrong. Please try again later.').show();  //  Error code: '+e.status
        
    });
    
}
function fillme(fieldid) {
    var myArray = fieldid.split("-");
    var rnd = document.getElementById("id_tournamentmatch_set-"+myArray[1]+"-round_number");
    var round = rnd.selectedIndex;
    //console.log("Getting element"+myArray[1])
    var select = document.getElementById(fieldid); //.style.color = "red";
    //window.alert("calling with "+select.options.length+ " options");
    if(select==null){
        return;
    }
    var selection = getSelectValues(select);
    var dicts = filldict();
    var dict = dicts[0];
    var dicto = dicts[1];
    var matchesinround = dict[round];

    var array = range(select.options.length);
    var c = array.filter(function(item) {
        return selection.indexOf(item) === -1;
    });
    //window.alert("c="+c+" selection="+selection);
    var shuffled = c.sort(() => 0.5 - Math.random());
    var total = dicto[round]+select.options.length-selection.length;

    var n = Math.floor(total/matchesinround)-selection.length;

    var selected = shuffled.slice(0, n);

    for(count=0; count<select.options.length; count++) {
        if(selected.includes(count)){
        select.options[count].selected="selected";
        }
    }
    select.dispatchEvent(new Event('change')); 
    
}

function getSelectValues(select) {
    var result = [];
    if (select == null){
        return result;
    }
    var options = select && select.options;
    var opt;

    for (var i=0, iLen=options.length; i<iLen; i++) {
    opt = options[i];

    if (opt.selected) {
        //result.push(opt.value || opt.text);
        result.push(i);
    }
    }
    return result;
}
function getSelectValuesActual(select) {
    var result = [];
    if (select == null){
        return result;
    }
    var options = select && select.options;
    var opt;

    for (var i=0, iLen=options.length; i<iLen; i++) {
    opt = options[i];

    if (opt.selected) {
        //result.push(opt.value || opt.text);
        result.push(opt.value);
    }
    }
    return result;
}
function range(size, startAt = 0) {
    return [...Array(size).keys()].map(i => i + startAt);
}
function filldict(){
    class DefaultDict {
        constructor(defaultInit) {
            return new Proxy({}, {
            get: (target, name) => name in target ?
                target[name] :
                (target[name] = typeof defaultInit === 'function' ?
                new defaultInit().valueOf() :
                defaultInit)
                })
            }
        }
    var gogo = true;
    var k = 0;
    var dict = new DefaultDict(Number);
    var dicto = new DefaultDict(Number);
    var dictoo = new DefaultDict(Number);
    //window.alert("starting...");
    while(gogo){
        var sousou = document.getElementById("id_tournamentmatch_set-"+k+"-round_number");
        var koukou = document.getElementById("id_tournamentmatch_set-"+k+"-participants");
        var selectiones = getSelectValues(koukou);
        var selectionval = getSelectValuesActual(koukou);
        k++;
        if(sousou != null && sousou.selectedIndex!=0){
            //window.alert("found "+"id_tournamentmatch_set-"+k+"-round_number");
            dict[sousou.selectedIndex]+=1;
            dicto[sousou.selectedIndex]+=selectiones.length;
            dictoo[sousou.selectedIndex]=selectionval;
            //window.alert(dict[sousou.selectedIndex]);
        }else{
            gogo = false;
        }
    }
    return [dict, dicto, dictoo];
}

// $(document).ready(function() {
//         $('.field-winners').find('select').multiselect({
//         enableFiltering: true,
//     });
// });
