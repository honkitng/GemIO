var all_jpegs;
var selected_count = 0;
var jpeg_dict = {};
var micrograph;
var scroll_run;

function getVar(value) {
    return value
}

function select(value) {
    if (jpeg_dict[value] == 1) {
        jpeg_dict[value] = 0;
        selected_count -= 1;
        document.getElementById(value).style.border = 'thick solid #fdf6c5';
    } else {
        jpeg_dict[value] = 1;
        selected_count += 1;
        document.getElementById(value).style.border = 'thick solid red';
    }

    document.getElementById('submit_text').textContent = 'Submit '.concat('(', selected_count, ')');
}

function submit() {
    document.getElementById('loading').style.display = 'inline-block'
    document.getElementById('submit_text').style.display = 'none'
    $.ajax({
        url: '/',
        type: 'POST',
        data: JSON.stringify(jpeg_dict),
    })
    .done(function(result){
        document.getElementById('loading').style.display = 'none'
        document.getElementById('submit_text').style.display = 'inline-block';
        const sel = result['selected'].toString();
        const loc = result['location'];
        var full_text = 'Saved '.concat(sel, ' micrographs to:\n', loc);
        alert(full_text);
    })
}

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
        }
    }
}

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
        }

        onWindowScroll();
    }
}

function getViewport() {
    var viewport_width;
    var viewport_height;

    if (typeof window.innerWidth != 'undefined') {
        viewport_width = window.innerWidth,
        viewport_height = window.innerHeight
    } else if (typeof document.documentElement != 'undefined' && typeof document.documentElement.clientWidth != 'undefined' && document.documentElement.clientWidth != 0) {
        viewport_width = document.documentElement.clientWidth,
        viewport_height = document.documentElement.clientHeight
    } else {
        viewport_width = document.getElementsByTagName('body')[0].clientWidth,
        viewport_height = document.getElementsByTagName('body')[0].clientHeight
    }
    return [viewport_width, viewport_height];
}

function addButtonImg(img_position) {
    var add_button = document.createElement('button');
    add_button.classList.add('btn', 'image-button');
    add_button.role = 'button';
    add_button.id = all_jpegs[img_position];
    add_button.style.margin = '3px';
    add_button.onclick = function(event) {
        select(all_jpegs[img_position]);
    }

    if (jpeg_dict[all_jpegs[img_position]] == 1) {
        add_button.style.border = '5px solid red';
    } else {
        add_button.style.border = '5px solid #fdf6c5';
    }

    var add_img = document.createElement('img');
    add_img.classList.add('rounded');
    add_img.name = 'micrograph';
    add_img.style.width = default_width.toString().concat('px');
    add_img.style.height= default_height.toString().concat('px');
    add_img.src = 'jpeg/'.concat(all_jpegs[img_position]);
    add_button.appendChild(add_img);

    return add_button;
}

var total_margin;
var top_margin;
var bot_margin;
var img_width;
var img_height;
var columns_shown;
var rows_shown;
var images_shown;
var first_index = 0;

function onStart() {
    var new_button = addButtonImg(0);
    $('#main-container')[0].appendChild(new_button);

    var border_width = parseInt($('.image-button')[0].style.borderWidth.replace('px', ''));
    var margin_width = parseInt($('.image-button')[0].style.margin.replace('px', ''));

    img_width = $('.image-button')[0].offsetWidth + border_width + margin_width;
    img_height = $('.image-button')[0].offsetHeight + border_width + margin_width;

    var [viewport_width, viewport_height] = getViewport();
    columns_shown = Math.floor(viewport_width/img_width)
    rows_shown = Math.floor(viewport_height/img_height)
    images_shown =  columns_shown * rows_shown + 2 * columns_shown;

    for (i = 1; i < images_shown; i++) {
        new_button = addButtonImg(i);
        $('#main-container')[0].appendChild(new_button);
    }

    total_margin = Math.ceil(all_jpegs.length/columns_shown) * img_height - 3 * img_height;
    $('#main-container')[0].style.marginBottom = total_margin + 'px';
    top_margin = 0;
    bot_margin = total_margin;
}

function onWindowScroll() {
    var new_button;

    if (window.scrollY < total_margin) {
        var new_first = Math.floor((all_jpegs.length/columns_shown) / (document.body.clientHeight/window.scrollY)) * columns_shown
        if (first_index < new_first) {
            for (i = first_index; i < first_index + images_shown && i < new_first; i++) {
                $('.image-button')[0].remove();
            }

            for (i = new_first; i < new_first + images_shown; i++) {
                if (i >= first_index + images_shown) {
                   new_button = addButtonImg(i);
                   $('#main-container')[0].appendChild(new_button);
                }
            }

            var margin_diff = (new_first - first_index)/columns_shown * img_height;

            top_margin += margin_diff;
            bot_margin -= margin_diff;

            $('#main-container')[0].style.marginTop = top_margin + 'px';
            $('#main-container')[0].style.marginBottom = bot_margin + 'px';

            first_index = new_first;

        } else if (first_index > new_first) {
            for (i = first_index; i < first_index + images_shown; i++) {
                if (i >= new_first + images_shown) {
                    $('.image-button')[$('.image-button').length-1].remove();
                }
            }

            var new_buttons = []

            for (i = new_first; i < new_first + images_shown && i < first_index; i++) {
                new_buttons.push(addButtonImg(i));
            }

            for (i = new_buttons.length; i > 0; i--) {
                $('#main-container').prepend(new_buttons[i-1]);
            }

            var margin_diff = (new_first - first_index)/columns_shown * img_height;

            top_margin += margin_diff;
            bot_margin -= margin_diff;

            $('#main-container')[0].style.marginTop = top_margin + 'px';
            $('#main-container')[0].style.marginBottom = bot_margin + 'px';

            first_index = new_first;
        }
    } else {
        $('#main-container')[0].style.marginTop = total_margin + 'px';
        $('#main-container')[0].style.marginBottom = 0;
    }
}

function scrollDelay() {
    if (typeof scroll_run !== "undefined"){
        clearTimeout(scroll_run);
    }
    scroll_run = setTimeout(function(){ onWindowScroll() }, 50);
}

window.addEventListener('scroll', scrollDelay, false);
window.addEventListener('resize', scrollDelay, false);

$(document).ready(function() {
    for (var value in all_jpegs) {
        jpeg_dict[all_jpegs[value]] = 0;
    }

    onStart();
})

$(window).on('beforeunload', function(){
    $(this).scrollTop(0);
})