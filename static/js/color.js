let backgroundElements = [
    "div#name-logo-color",
    "div.blog-masthead",
];
let foregroundElements = [
    "a code",
    ":not(blockquote.twitter-tweet) a",
    "span.colors",
    "p.colors strong",
];
let $backgroundElements = backgroundElements.map(x => $(x));
let $foregroundElements = foregroundElements.map(x => $(x));

function color(idx){
    let sep = 2.094;
    let dimming_factor = 1;
    if(
        // dark mode
        window.matchMedia('(prefers-color-scheme: dark)').matches
    ){
        dimming_factor = 1.5;
    }
    let blue = Math.floor(Math.min(255, dimming_factor*(127+127*Math.sin(idx)))).toString(16).padStart(2,'0');
    let green = Math.floor(Math.min(255, dimming_factor*(80+80*Math.sin(idx+sep)))).toString(16).padStart(2,'0');
    let red = Math.floor(Math.min(255, dimming_factor*(127+127*Math.sin(idx+sep+sep)))).toString(16).padStart(2,'0');
    return `#${red}${green}${blue}`;
}

let colorCycle = (function () {
    let starting = Math.floor(Math.random() * 628)/100.0;
    let sep = 2.094; // 2*pi/3: space out three colors
    let idx = starting; // green = red + sep, blue = green + sep
    console.log(`Color starting index: ${starting}`);
    function colorCycleImpl(increment){
        if(increment){
            idx += .04;
        }
        if(idx > 6.3){
            idx = 0;
        }

        let offset_weight = -.0005;
        for(var i = 0; i < $backgroundElements.length; i++){
            let el = $backgroundElements[i];
            let offset = el.offset().top;
            let relidx = idx+offset*offset_weight;
            $backgroundElements[i].css("background-color", color(relidx));
        }
        for(var i = 0; i < $foregroundElements.length; i++){
            let sel = $foregroundElements[i];
            for(var j = 0; j < sel.length; j++){
                let el = $(sel[j]);
                let offset = el.offset().top;
                let relidx = idx+offset*offset_weight;
                el.css("color", color(relidx));

            }
        }

    }

    colorCycleImpl();
    setInterval(function(){colorCycleImpl(true)}, 500);
    return function(){colorCycleImpl(false)};
})();

export default function updateElements(){
    $backgroundElements = backgroundElements.map(x => $(x))
    $foregroundElements = foregroundElements.map(x => $(x))
    colorCycle();
}
updateElements();

