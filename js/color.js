
function changeElementColor(element, color, time, cb) {
    $(element).animate(
        {"background-color":color},
        {
            "duration":time,
            "done":cb
        }
    );
}

function transitionElementColors() {
    let elements = [
        "div#name-logo-color",
        "div.blog-masthead"
    ];
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
        for(var i = 1; i < elements.length; i++){
            changeElementColor(elements[i], color, delay);
        }
        changeElementColor(elements[0], color, delay, colorFunction);
    })();
}

transitionElementColors();
