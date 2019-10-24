import updateElements from './color.js'
function uniqueID () {
    return Date.now().toString()+"-"+Math.random();
}

let last_page_load_request = -1;
function loadPage (name, newLoad) {
    if(true === newLoad){
        history.pushState({},'',name.replace('content.html',''));
    }
    let uid = uniqueID();
    last_page_load_request = uid;
    $.get(name, function( data ){
        if(uid == last_page_load_request){
            $("div.blog-post").fadeOut(function(){
                $("div.blog-main").empty();
                $("div.blog-main").toggle()
                $("div.blog-main").append(data);
                interceptLinks();
                updateElements();
                $("div.blog-main").fadeIn();
            });
        }
    });
}

function interceptLinks(){
    $('a').click(function(event){
        let href = $(this).attr('href')+'/content.html';
        if(this.host == window.location.host && !href.startsWith('#')){
            event.preventDefault();
            href = href.replace('//','/');
            console.log('Intercepting call to '+href);
            loadPage(href, true);
        }
    });
}

interceptLinks();

