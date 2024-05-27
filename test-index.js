document.addEventListener('DOMContentLoaded', function() {
    let newDiv = window.document.createElement('div');
    newDiv.innerHTML = 'Hello, Script HeadScriptExternal DOMContentLoaded World!';
    window.document.body.appendChild(newDiv);
});


document.addEventListener('onload', function() {
    let newDiv = window.document.createElement('div');
    newDiv.innerHTML = 'Hello, Script HeadScriptExternal onLOAD World!';
    window.document.body.appendChild(newDiv);
});

document.addEventListener('onready', function() {
    let newDiv = window.document.createElement('div');
    newDiv.innerHTML = 'Hello, Script HeadScriptExternal onREADY World!';
    window.document.body.appendChild(newDiv);
});

document.addEventListener('readystatechange', function(event) {
    console.log('document.readyState:', document.readyState);
    console.log('event:', event);
    let newDiv = window.document.createElement('div');
    newDiv.innerHTML = 'Hello, Script HeadScriptExternal readystatechange='+ document.readyState +' World!';
    window.document.body.appendChild(newDiv);
});

