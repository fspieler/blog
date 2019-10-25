import updateElements from './color.js'
function uniqueID () {
    return Date.now().toString()+"-"+Math.random();
}

let last_page_load_request = -1;
function loadPage (name, withHistory) {
    if(true === withHistory){
        let nameWithoutContent = name.replace('content.html','')
        history.pushState(
            {
                name: name
            },
            '',
            nameWithoutContent
        );
    }
    let uid = uniqueID();
    last_page_load_request = uid;
    $.get(name, function( data ){
        if(uid == last_page_load_request){
            updatePage(data);
        }
    });
}

function updatePage(data){
    $("div.blog-post").fadeOut(function(){
        $("div.blog-main").empty();
        $("div.blog-main").toggle()
        $("div.blog-main").append(data);
        interceptLinks();
        updateElements();
        document.title = $(".blog-post-title").text() + ' - fredspieler.com';
        $("div.blog-main").fadeIn();
    });
}

window.addEventListener('popstate', function(event){
    console.log(event);
    if(event.state && event.state.name){
        loadPage(event.state.name, false);
    }
});

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

