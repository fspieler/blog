import updateElements from './color.js'
function uniqueID () {
    return Date.now().toString()+"-"+Math.random();
}

let last_page_load_request = -1;
function loadPage (name, withHistory, anchor) {
    let uid = uniqueID();
    last_page_load_request = uid;
    $.get(name, function( data ){
        if(uid === last_page_load_request){
            if(true === withHistory){
                pushHistory(name);
            }
            if(anchor === '#'){
                window.location.href = '#';
                anchor = undefined;
            }
            updatePage(data, anchor);
        }
    })
}

function pushHistory(name){
    let nameWithoutContent = name.replace('content.html','')
    history.pushState(
        {
            name: name
        },
        '',
        nameWithoutContent
    );
}

function updatePage(data, anchor){
    $("div.blog-main").fadeOut(function(){
        $("div.blog-main").empty();
        $("div.blog-main").toggle()
        $("div.blog-main").append(data);
        interceptLinks();
        updateElements();
        let title = $(".blog-post-title").text() + ' - fredspieler.com';
        document.title = title;
        if(anchor){
            window.location.href = anchor;
        }
        $("div.blog-main").fadeIn();
    });
}

window.addEventListener('popstate', function(event){
    if(event.state && event.state.name){
        loadPage(event.state.name, false);
    } else {
        let newUrl = new URL(window.location);
        loadPage(`${newUrl.pathname}content.html${newUrl.search}`, false);
    }
});

function interceptLinks(){
    $('a').click(function(event){
        let href = $(this).attr('href');
        let anchor_idx = href.indexOf('#');
        if(this.host == window.location.host && anchor_idx !== 0){
            let anchor;
            if(anchor_idx > 0){
                anchor = href.substring(anchor_idx);
                href = href.substring(0,anchor_idx);
            }
            event.preventDefault();
            href = `${href}/content.html`.replace('//','/');
            loadPage(href, true, anchor);
        }
    });
}

interceptLinks();

