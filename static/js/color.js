
function change_background_color(element, color, time, cb) {
    $(element).animate(
        {"background-color":color},
        {
            "duration":time,
            "done":cb
        }
    );
}
function change_foreground_color(element, color, time) {
    $(element).animate(
        {"color":color},
        {
            "duration":time
        }
    );
}

function transitionElementColors() {
    let background_elements = [
        "div#name-logo-color",
        "div.blog-masthead",
    ];
    let foreground_elements = [
        "a",
    ]
    let colors = [
        "#428bca",
        "#860eb9",
        "#f50009",
        "#ff8900",
        "#f50009",
        "#860eb9"
    ];
    let index = 0;
    let delay = 50000;
    (function colorFunction() {
        index++;
        index %= colors.length;
        let color = colors[index];
        //the first one has a callback to make everything loop forever
        change_background_color(background_elements[0], color, delay, colorFunction);
        for(var i = 1; i < background_elements.length; i++){
            change_background_color(background_elements[i], color, delay);
        }
        for(var i = 0; i < foreground_elements.length; i++){
            change_foreground_color(foreground_elements[i], color, delay);
        }
    })();
}

transitionElementColors();
