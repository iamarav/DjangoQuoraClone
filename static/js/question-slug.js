jQuery(document).ready(function(){
    var question, question_slug;
    var action;
    action = jQuery('#act').val();
    if (action == 'add'){
        jQuery('body').on( 'blur','#question', function(){
            question = jQuery('#question').val();
            question_slug = question.trim().toLowerCase().replace(/\s+/g, '-').replace(/\?/, '');
            
            if (question_slug.length > 0){
                ajax_check_if_slug_exists( question_slug );
            }
            
        });
    }
    else{
        jQuery('body').on( 'change','#question', function(){
            question = jQuery('#question').val();
            question_slug = question.trim().toLowerCase().replace(/\s+/g, '-').replace(/\?/, '');

            if (question_slug.length > 0){
                ajax_check_if_slug_exists( question_slug );
            }
        });
    }
});

function ajax_check_if_slug_exists( slug ){
    var ajax_url = window.location.protocol+"//"+window.location.hostname;
    if (window.location.port != "" && window.location.port != undefined){
        ajax_url += ":"+window.location.port;
    }
    ajax_url += '/checkslug';

    jQuery.ajax({
        url : ajax_url, // AJAX handler
        data : {
                slug : slug,
            },
        type : 'POST',
        success : function( data ){
            if (data.code == true){
                // Exists
                var new_slug = data.slug;
                    new_slug += "-";
                    new_slug += Math.ceil(Math.random()*100);
                jQuery('#question_slug').val(new_slug);
            }
            else if (data.code == false){
                // Does Not Exist
                jQuery('#question_slug').val(data.slug);
            }
        }
    });	
}

function addCategory(){
    var category = prompt ( 'Enter the category name', '' );
    if (category != '' && category != undefined){
        var ajax_url = window.location.protocol+"//"+window.location.hostname;
        if (window.location.port != "" && window.location.port != undefined){
            ajax_url += ":"+window.location.port;
        }
        ajax_url += '/addCategory';

        jQuery.ajax({
            url : ajax_url, // AJAX handler
            data : {
                    category : category,
                },
            type : 'POST',
            success : function( data ){
                if (data.code == 'success'){
                    // Added
                    addCategoryOption(data.category)
                    if (data.message == undefined || data.message == ''){
                        alert('Added Category!');
                    }
                    else{
                        alert(data.message)
                    }
                }
                else{
                    if (data.message == undefined || data.message == ''){
                        alert('Some error occured. Try Again!');
                    }
                    else{
                        alert(data.message)
                    }
                }
            }
        });	
    } 
    return false;
}

function addCategoryOption(category){
    optionText = category; 
    optionValue = category; 
    $('#question_category').append(`<option value="${optionValue}"> 
                                       ${optionText} 
                                  </option>`); 
}