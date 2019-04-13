window.onload = function() {
    initSearch();
    initPlayButtons();
    initPlayerControl();
    initVolumeControl();
};

$(function () {
  $('[data-toggle="popover"]').popover()
})

$('.popover-dismiss').popover({
  trigger: 'focus'
})

function initVolumeControl() {
    var slider = document.getElementById("volumeSlider");
    // Update the current slider value (each time you drag the slider handle)
    slider.oninput = function() {
//        checkMute();
        // AJAX
        var request = new XMLHttpRequest();
        request.onload = function() {
            showAlert(request.responseText, 'alert-success');
        };
        request.open("GET", "/setVolume?v=" + this.value, true);
        request.send();
    }
}

/**
    TODO: Should change the icon if mute
 */
function checkMute(){
//    if (audio.volume == 0){
//        $( ".speaker" ).attr("src", "images/speaker.png");
//    } else {
//        $( ".speaker" ).attr("src", "images/speakermute.png");
//    }
}

function initSearch() {
    // Get the input field
    var input = document.getElementById("searchField");

    // Execute a function when the user releases a key on the keyboard
    if (input) {
        input.addEventListener("keyup", function(event) {
          // Cancel the default action, if needed
          event.preventDefault();
          // Number 13 is the "Enter" key on the keyboard
          if (event.keyCode === 13) {
            // Trigger the button element with a click
            var query = document.getElementById("searchField").value;
            if (query || 0 === query.length) {
                return false
            }
            document.getElementById("searchForm").submit();
          }
        });
    }

    var form = document.getElementById("searchForm");
    form.onsubmit=search;
}

function initPlayerControl() {
    /* Initialize Carousel */
    var paused = 0;

    /* Play trigger */
    $('#playButton').click(function() {
        var state = (paused) ? 'cycle' : 'pause';
        paused = (paused) ? 0 : 1;
//        $('#myCarousel').carousel(state);
        $(this).find('i').toggleClass('fa-play fa-pause');
    });
}

function initPlayButtons() {
    var playButtons = document.querySelectorAll(".media-player");
    for (var i=0, l=playButtons.length; i<l; i++) {
        var button = playButtons[i];
        // For each button, listen for the "click" event
        button.addEventListener("click", function(e) {
            // When a click happens, stop the button
            // from submitting our form (if we have one)
            e.preventDefault();

            var clickedButton = e.target;
            var path = clickedButton.value;

            // Now we need to send the data to our server
            // without reloading the page - this is the domain of
            // AJAX (Asynchronous JavaScript And XML)
            // We will create a new request object
            // and set up a handler for the response
            var request = new XMLHttpRequest();
            request.onload = function() {
                // We could do more interesting things with the response
                // or, we could ignore it entirely
                showAlert(request.responseText, 'alert-success');
            };
            // We point the request at the appropriate path
            request.open("GET", "/" + path, true);
            // and then we send it off
            request.send();
        });
    }
}

/**
  Bootstrap Alerts -
  Function Name - showalert()
  Inputs - message,alerttype
  Example - showalert("Invalid Login","alert-error")
  Types of alerts -- "alert-error","alert-success","alert-info","alert-warning"
  Required - You only need to add a alert_placeholder div in your html page wherever you want to display these alerts "<div id="alert_placeholder"></div>"
  Written On - 14-Jun-2013
**/
function showAlert(message, type) {
    if (!message || 0 === message.length) {
        return false
    }
    $('#alert_placeholder').append('<div id="alertdiv" class="alert ' +  type + '"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')

    setTimeout(function() { // this will automatically close the alert and remove this if the users doesnt close it in 5 secs
        $("#alertdiv").remove();
    }, 5000);
}

function search() {
    var url = window.location.href;
    var query = document.getElementById("searchField").value;
    var encoded = encodeURIComponent(query);
    if (!encoded || 0 === encoded.length) {
        return false
    }
    url = '/search?q=' + encoded
    window.location.replace(url);
    return false
}

function renderDuration(seconds) {
    // calculate seconds
    var s = seconds % 60;
    s = s < 10 ? "0" + s : s;

    var m = Math.floor(seconds / 60) % 60;
    m = m < 10 ? "0" + m : m;

    var h = Math.floor(seconds / 60 / 60);

    return h + ":" + m + ":" + s
}