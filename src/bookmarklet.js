(function() {
    console.log('Bookmarklet loaded');
    
    // Create a link element for CSS
    var link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "https://cdn.jsdelivr.net/gh/tyeth/serialfruit-connect@v0.0.6/src/style.css";
    document.head.appendChild(link);
    console.log('CSS loaded');

    // Create a script element for the JavaScript
    var script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/gh/tyeth/serialfruit-connect@v0.0.6/src/script.js";
    script.onload = function() {
        console.log('Script loaded');
        
        // Create the side panel
        var panel = document.createElement("div");
        panel.id = "serialfruit-panel";
        panel.style.cssText = "position:fixed;top:0;right:-300px;width:300px;height:100%;background:#fff;box-shadow:-2px 0 5px rgba(0,0,0,0.5);transition:right 0.3s;z-index:10000;overflow:auto;";
        document.body.appendChild(panel);
        console.log('Panel created');
        
        // Add the content from your index.html to the panel
        fetch("https://cdn.jsdelivr.net/gh/tyeth/serialfruit-connect@v0.0.6/src/index.html")
            .then(response => response.text())
            .then(html => {
                panel.innerHTML = html + panel.innerHTML;
                console.log('HTML content loaded into the panel');
                setTimeout(showScreen('main-menu'), 100);
            })
            .catch(error => {
                console.error('Error loading HTML content:', error);
            });

        // Add a toggle button to the document body
        var toggleButton = document.createElement("button");
        toggleButton.innerText = "Toggle Panel";
        toggleButton.style.cssText = "position:fixed;top:10px;right:10px;width:100px;height:auto;z-index:10001;";
        toggleButton.onclick = function() {
            if (panel.style.right === "0px") {
                panel.style.right = "-300px";
                this.innerText = "&gt;";
            } else {
                panel.style.right = "0px";
                this.innerText = "&lt;";
            }
        };
        document.body.appendChild(toggleButton);
        console.log('Toggle button added');
    };
    script.onerror = function() {
        console.error('Failed to load the script');
    };
    document.body.appendChild(script);
})();
