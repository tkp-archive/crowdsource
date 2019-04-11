var header = document.getElementsByTagName('header')[0];
var nodes = header.querySelectorAll('li');


var logo = header.querySelector('#logoholder');
var setme = 0;


window.onscroll = function() {

  if (document.body.scrollTop >= 50 || document.documentElement.scrollTop >= 50) {
    header.classList.add('bg-dark-gray-fadein')
    header.classList.remove('bg-dark-gray-fadeout');

    var svg = logo.querySelector('svg');
    var paths = svg.querySelectorAll('path');
    var pgs = svg.querySelectorAll('polygon');

    setme = 1;

    setTimeout(function(){
    header.classList.add('bg-dark-gray');

    for(var i = 0; i < nodes.length; i++){
        nodes[i].children[0].classList.add('profile-link');
    }

    for(var i = 0; i < paths.length; i++){
        paths[i].setAttribute('fill', '#fff');
    }

    for(var i = 0; i < pgs.length; i++){
        if(pgs[i].getAttribute('fill') !== '#19E0D6'){
            pgs[i].setAttribute('fill', '#fff');
        }
    }
    }, 80);
  } else {
    if(setme === 1){
        header.classList.add('bg-dark-gray-fadeout');
        header.classList.remove('bg-dark-gray-fadein');

        var svg = logo.querySelector('svg');
        var paths = svg.querySelectorAll('path');
        var pgs = svg.querySelectorAll('polygon');

        setTimeout(function(){
        header.classList.remove('bg-dark-gray');

        for(var i = 0; i < nodes.length; i++){
            nodes[i].children[0].classList.remove('profile-link');
        }

        for(var i = 0; i < paths.length; i++){
            paths[i].setAttribute('fill', '#000');
        }

        for(var i = 0; i < pgs.length; i++){
            if(pgs[i].getAttribute('fill') !== '#19E0D6'){
                pgs[i].setAttribute('fill', '#000');
            }
        }
        setme = 0;
    }, 80);
    }
  }
};

setTimeout(function(){window.onscroll();}, 50);