jQuery(document).ready(function(){
    console.log('jQuery is Working')
});


function do_upvote_ajax(type, id, element){
    var ajax_url = window.location.protocol+"//"+window.location.hostname;
    if (window.location.port != "" && window.location.port != undefined){
        ajax_url += ":"+window.location.port;
    }
    element_id = element.id
    ajax_url += '/upvote?type='+type+"&id="+id;

	jQuery.get({
        url : ajax_url, // AJAX handler
        data : "",
        type : 'GET',
        success : function( data ){
            if (data.code == 'success'){
                if (data.action == 'upvote'){
                    if(  jQuery('#'+element_id).hasClass( 'btn-primary' ) ){
                        jQuery('#'+element_id)
                            .removeClass( 'btn-primary' )
                            .addClass( 'btn-success' )
                            .find( '.upvote_number' )
                            .text( data.data.upvotes );                    
                    }
                }
                if (data.action == 'downvote'){
                    if(  jQuery('#'+element_id).hasClass( 'btn-success' ) ){
                        jQuery('#'+element_id)
                            .removeClass( 'btn-success' )
                            .addClass( 'btn-primary' )
                            .find( '.upvote_number' )
                            .text( data.data.upvotes );                    
                    }
                }

            }
            else if (data.code == 'error'){
                //if(  jQuery('#'+element_id).hasClass('btn-primary') ){
                    jQuery('#'+element_id)
                        .find( '.upvote_number' )
                        .text( data.data.upvotes );
                //}
            }
            else if(data.code == 'invalid_user'){
                var wantToLogin = confirm ('You must login to upvote.\nClick OK to Login.', false);
                if (wantToLogin){
                    var login_url = window.location.protocol+"//"+window.location.hostname;
                    if (window.location.port != "" && window.location.port != undefined){
                        login_url += ":"+window.location.port;
                    }
                    login_url += '/user/login';
                    window.location.href = login_url;
                }
            }
        }
    });	
}
