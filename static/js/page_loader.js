import updateElements from './color.js'
function uniqueID () {
    return Date.now().toString()+"-"+Math.random();
}

let last_page_load_request = -1;
function loadPage (name, withHistory) {
    let uid = uniqueID();
    last_page_load_request = uid;
    $.get(name, function( data ){
        if(uid === last_page_load_request){
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
            updatePage(data);
        }
    })
}

function updatePage(data){
    $("div.blog-main").fadeOut(function(){
        $("div.blog-main").empty();
        $("div.blog-main").toggle()
        $("div.blog-main").append(data);
        interceptLinks();
        updateElements();
        let title = $(".blog-post-title").text() + ' - fredspieler.com';
        document.title = title;
        $("div.blog-main").fadeIn();
    });
}

window.addEventListener('popstate', function(event){
    if(event.state && event.state.name){
        loadPage(event.state.name, false);
    }
});

function interceptLinks(){
    $('a').click(function(event){
        let href = $(this).attr('href');
        if(this.host == window.location.host && !href.startsWith('#')){
            event.preventDefault();
            href = `${href}/content.html`.replace('//','/');
            loadPage(href, true);
        }
    });
}

interceptLinks();

