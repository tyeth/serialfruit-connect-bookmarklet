(function() {
    // Create a link element for CSS
    var link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "https://cdn.jsdelivr.net/gh/tyeth/serialfruit-connect@285ae36905197097715d2547c9c0a48b0075e833/src/style.css";
    document.head.appendChild(link);

    // Create a script element for the JavaScript
    var script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/gh/tyeth/serialfruit-connect@285ae36905197097715d2547c9c0a48b0075e833/src/script.js";
    script.onload = function() {
        // Create the side panel
        var panel = document.createElement("div");
        panel.id = "serialfruit-panel";
        panel.style.cssText = "position:fixed;top:0;right:-300px;width:300px;height:100%;background:#fff;box-shadow:-2px 0 5px rgba(0,0,0,0.5);transition:0.3s;z-index:10000;overflow:auto;";
        
        // Add a toggle button to the panel
        var toggleButton = document.createElement("button");
        toggleButton.innerText = "Toggle Panel";
        toggleButton.style.cssText = "position:fixed;top:10px;left:-100px;width:100px;height:30px;z-index:10001;";
        toggleButton.onclick = function() {
            if (panel.style.right === "0px") {
                panel.style.right = "-300px";
            } else {
                panel.style.right = "0px";
            }
        };
        panel.appendChild(toggleButton);
        
        // Add the content from your index.html to the panel
        fetch("https://cdn.jsdelivr.net/gh/tyeth/serialfruit-connect@main/src/index.html")
            .then(response => response.text())
            .then(html => {
                panel.innerHTML += html;
                document.body.appendChild(panel);
            });
    };
    document.body.appendChild(script);
})();
