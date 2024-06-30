(function() {
    console.log('Bookmarklet loaded');
    
    // Create a container element
    var container = document.createElement("div");
    container.id = "serialfruit-container";
    document.body.appendChild(container);
    console.log('Container created');

    // Create a style element for CSS
    var style = document.createElement("style");
    style.textContent = "@import url('https://cdn.jsdelivr.net/gh/tyeth/serialfruit-connect@v0.0.101/src/style.css');";
    style.setAttributeNode(document.createAttribute("scoped"));
    let crs = document.createAttribute("crossorigin");
    crs.value = "anonymous";
    style.setAttributeNode(crs);
    // style.src = "https://cdn.jsdelivr.net/gh/tyeth/serialfruit-connect@v0.0.97/src/style.css";
    container.appendChild(style);
    console.log('CSS loaded');

    // Create a script element for the JavaScript
    var script = document.createElement("script");
    script.crossOrigin = "anonymous";
    script.onload = function() {
        console.log('Script loaded');
        
        // Create the side panel
        var panel = document.createElement("div");
        panel.id = "serialfruit-body";
        panel.style.cssText = "position:fixed;top:0;right:-300px;width:300px;height:100%;background:#fff;box-shadow:-2px 0 5px rgba(0,0,0,0.5);transition:right 0.3s;z-index:10000;overflow:auto;";
        container.appendChild(panel);
        console.log('Panel created');
        
        // Add the content from your index.html to the panel
        fetch("https://cdn.jsdelivr.net/gh/tyeth/serialfruit-connect@v0.0.101/src/index.html")
            .then(response => response.text())
            .then(html => {
                panel.innerHTML = html + panel.innerHTML;
                console.log('HTML content loaded into the panel');
            })
            .catch(error => {
                console.error('Error loading HTML content:', error);
            });

        // Add a toggle button to the document body
        var toggleButton = document.createElement("button");
        toggleButton.innerText = "Toggle Panel";
        toggleButton.style.cssText = "position:fixed;top:10px;right:10px;width:100px;height:auto;z-index:10001;";
        toggleButton.onclick = function() {
            this.style.width = "auto";
            this.style.height = "30px";
            if (panel.style.right === "0px") {
                panel.style.right = "-300px";
                this.innerText = "<";
            } else {
                panel.style.right = "0px";
                this.innerText = ">";
            }
        };
        document.body.appendChild(toggleButton);
        console.log('Toggle button added');
    };
    script.onerror = function(error) {
        debugger;
        console.error('Failed to load the script', error);
    };
    script.src = "https://cdn.jsdelivr.net/gh/tyeth/serialfruit-connect@v0.0.101/src/script.js";
    document.body.appendChild(script);
})();