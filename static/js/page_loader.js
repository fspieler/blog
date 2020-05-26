import updateElements from './color.js'
function uniqueID () {
    return Date.now().toString()+"-"+Math.random();
}

let last_page_load_request = -1;
function loadPage (name, withHistory, anchor) {
    let current_page = $('div.blog-post')[0].id;
    let content_idx = name.indexOf('content.html');
    let trimmed_name = name;
    if(content_idx >= 0){
        trimmed_name = name.substring(0, content_idx);
    }
    if(
        current_page !== trimmed_name
    ){
        let uid = uniqueID();
        last_page_load_request = uid;
        $.get(name, function( data ){
            if(uid === last_page_load_request){
                if(true === withHistory){
                    if(anchor){
                        pushHistory(name+anchor);
                    }else{
                        pushHistory(name);
                    }
                }
                updatePage(trimmed_name, data, anchor);
            }
        })
    } else {
        if(anchor){
            window.location.href = anchor;
        }
    }
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

function updatePage(name, data, anchor){
    let current_page = $('div.blog-post')[0].id;
    let new_page = $.parseHTML(data)[2].id;
    if(new_page != current_page){
        $("div.blog-main").fadeOut(function(){
            $("div.blog-main").empty();
            $("div.blog-main").toggle()
            $("div.blog-main").append(data);
            interceptLinks();
            updateElements();
            let title = $(".blog-post-title").text() + ' - fredspieler.com';
            document.title = title;
            $("div.blog-main").fadeIn();
            if(anchor){
                window.location.href = anchor;
            }
        });
    } else if(anchor){
        window.location.href = anchor;
    }
}

window.addEventListener('popstate', function(event){
    event.preventDefault();
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
        if(anchor_idx === 0){
            window.location.href = href;
        } else {
            let anchor;
            event.preventDefault();
            if(anchor_idx > 0){
                anchor = href.substring(anchor_idx);
                href = href.substring(0,anchor_idx);
            }
            href = `${href}/content.html`.replace('//','/');
            loadPage(href, true, anchor);
        }
    });
}

interceptLinks();

