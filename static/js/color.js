let backgroundElements = [
    "div#name-logo-color",
    "div.blog-masthead",
];
let foregroundElements = [
    "a code",
    "a",
    "h3.colors",
    "p.colors strong",
];
let $backgroundElements = backgroundElements.map(x => $(x));
let $foregroundElements = foregroundElements.map(x => $(x));



let colorCycle = (function () {
    let starting = Math.floor(Math.random() * 628)/100.0;
    let sep = 2.094; // 2*pi/3: space out three colors
    let idx = starting; // green = red + sep, blue = green + sep
    console.log(`Random  starting index: ${starting}`);
    function colorCycleImpl(increment){
        if(increment){
            idx += .01;
        }
        if(idx > 6.3){
            idx = 0;
        }
        let blue = Math.floor(127+127*Math.sin(idx)).toString(16).padStart(2,'0');
        let green = Math.floor(127+127*Math.sin(idx+sep)).toString(16).padStart(2,'0');
        let red = Math.floor(127+127*Math.sin(idx+sep+sep)).toString(16).padStart(2,'0');
        let color = `#${red}${green}${blue}`;

        for(var i = 0; i < backgroundElements.length; i++){
            $backgroundElements[i].css("background-color", color);
        }
        for(var i = 0; i < foregroundElements.length; i++){
            $foregroundElements[i].css("color", color);
        }

    }

    colorCycleImpl();
    setInterval(function(){colorCycleImpl(true)}, 200);
    return function(){colorCycleImpl(false)};
})();

export default function updateElements(){
    $backgroundElements = backgroundElements.map(x => $(x))
    $foregroundElements = foregroundElements.map(x => $(x))
    colorCycle();
}
updateElements();

