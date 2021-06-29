var jpeg_array = new Array;

function select(value) {
    var value_index = jpeg_array.indexOf(value);
    if (value_index > -1) {
        jpeg_array.splice(value_index, 1);
        document.getElementById(value).style.border = 'thick solid #fdf6c5';
    } else {
        jpeg_array.push(value);
        document.getElementById(value).style.border = 'thick solid red';
    };

    document.getElementById('submit_text').textContent = 'Submit '.concat('(', jpeg_array.length.toString(), ')');
};

function submit() {
    document.getElementById('loading').style.display = 'inline-block'
    document.getElementById('submit_text').style.display = 'none'
    $.ajax({
        url: '/',
        type: 'POST',
        data: JSON.stringify(jpeg_array),
    })
    .done(function(result){
        document.getElementById('loading').style.display = 'none'
        document.getElementById('submit_text').style.display = 'inline-block';
        const sel = result['selected'].toString();
        const loc = result['location'];
        var full_text = 'Saved '.concat(sel, ' micrographs to:\n', loc);
        alert(full_text);
    })
};

var micrograph;

function increaseSize() {
    if (default_width < 1000) {
        micrograph = document.getElementsByName("micrograph");
        default_height = (default_width + 50)/default_width * (default_height);
        default_width += 50;
        micrograph[0].style.width = default_width.toString().concat('px');
        micrograph[0].style.height = default_height.toString().concat('px');

        // the better way to find the true dimensions of the button
        $('.image-button')[0].style.width = 'auto'
        $('.image-button')[0].style.height = 'auto'
        var width = $('.image-button')[0].offsetWidth;
        var height = $('.image-button')[0].offsetHeight;

        $('.image-button').each(function(index) {
            this.style.width = width.toString().concat('px');
            this.style.height = height.toString().concat('px');
        });

        for (i = 1; i < micrograph.length; i++) {
            micrograph[i].style.width = default_width.toString().concat('px');
            micrograph[i].style.height = default_height.toString().concat('px');
        };
    };
};

function decreaseSize() {
    if (default_width > 100) {
        micrograph = document.getElementsByName("micrograph");
        default_height = (default_width - 50)/default_width * (default_height);
        default_width -= 50;
        micrograph[0].style.width = default_width.toString().concat('px');
        micrograph[0].style.height = default_height.toString().concat('px');

        // a less elegant way of finding the dimensions of the button but the better way will not work for some reason
        var width = $('.image-button')[0].offsetWidth;
        var height = $('.image-button')[0].offsetHeight;
        height = (width - 50)/width * (height);
        width -= 50;

        $('.image-button').each(function(index) {
            this.style.width = width.toString().concat('px');
            this.style.height = height.toString().concat('px');
        });

        for (i = 1; i < micrograph.length; i++) {
            micrograph[i].style.width = default_width.toString().concat('px');
            micrograph[i].style.height = default_height.toString().concat('px');
        };

        onWindowScroll();
    };
};

function getVar(value) {
    return value
};

function onStart() {
    var node = document.createElement('img');
    node.classList.add('rounded');
    node.name = 'micrograph';
    node.style.width = default_width.toString().concat('px');
    node.style.height= default_height.toString().concat('px');
    node.src = 'jpeg/'.concat($('.image-button')[0].id);
    $('.image-button')[0].appendChild(node);

    var width = $('.image-button')[0].offsetWidth;
    var height = $('.image-button')[0].offsetHeight;

    $('.image-button').each(function(index) {
        this.style.width = width.toString().concat('px');
        this.style.height = height.toString().concat('px');
    });

    onWindowScroll();
};

function onWindowScroll() {
    $('.image-button').each(function(index) {
        var max_top = window.scrollY - window.innerHeight;
        var max_bot = window.scrollY + window.innerHeight;
        if (max_top < this.offsetTop && this.offsetTop < max_bot) {
            if (this.children.length == 0) {
                var node = document.createElement('img');
                node.classList.add('rounded');
                node.name = 'micrograph';
                node.style.width = default_width.toString().concat('px');
                node.style.height= default_height.toString().concat('px');
                node.src = 'jpeg/'.concat($('.image-button')[index].id);
                this.appendChild(node);
            };
        }  else {
            if (this.children.length == 1) {
                this.children[0].remove();
            };
        };
    });
};

var scroll_run;

function scrollDelay() {
    if (typeof scroll_run !== "undefined"){
        clearTimeout(scroll_run);
    };
    scroll_run = setTimeout(function(){ onWindowScroll() }, 100);
};

window.addEventListener('scroll', scrollDelay, false);
window.addEventListener('resize', scrollDelay, false);
document.addEventListener('DOMContentLoaded', onStart, false);