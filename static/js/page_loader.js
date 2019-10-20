function uniqueID () {
    return Date.now().toString()+"-"+Math.random();
}

let last_page_load_request = -1;
function loadPage (name, newLoad) {
    if(true === newLoad){
        history.pushState({},'',name);
    }
    uid = uniqueID();
    last_page_load_request = uid;
    $.get(name, function( data ){
        if(uid == last_page_load_request){
            $("div.blog-main").append(data);
        }
    });
}
