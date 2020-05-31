const width  = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
const height = window.innerHeight|| document.documentElement.clientHeight|| document.body.clientHeight;

var currentEndBrace = 25;
var currentPiChunk = 0;
var currentPiLength = 0;
var averageBracketWidth = 0;

var r18CheckComplete = false;
var aboutSplashScreenUp = false;

function appendAnotherPiChunk() {
    if (currentPiChunk < 21) {
        currentPiChunk += 1; //Increment currentPiChunk here to prevent race condition appending multiple chunks at once
        currentPiLength += pi_digits[currentPiChunk].length;
        document.getElementById("pi_text").innerHTML += pi_digits[currentPiChunk];
    }
}

window.onbeforeunload = function () {
    currentEndBrace = 25;
    window.scrollTo(0, 0);
}

function placeInitalElements() {
    var newDiv = document.createElement("div");
    newDiv.className = "pi_text overlay"; //Initially start blurred
    newDiv.setAttribute("id", "content_div");
    var newContent = document.createElement("text")
    newContent.innerHTML = pi_digits[0];
    currentPiLength += pi_digits[0].length;
    newContent.setAttribute("id", "pi_text");
    newContent.setAttribute("class", "pi_text");

    newDiv.appendChild(newContent);
    document.body.appendChild(newDiv);
}

function dismissR18SplashScreen() {
    r18CheckComplete = true;
    var screen = document.getElementById("r18SplashScreen");
    screen.parentNode.removeChild(screen);

    document.getElementById("content_div").setAttribute("class", "pi_text");
}

function getUnder18sOuttaHere() {
    history.back();
}

function dismissInfoSplashScreen() {
    var screen = document.getElementById("infoSplashScreen");
    screen.parentNode.removeChild(screen);

    //unblur main screen if the R18 check has been completed
    if (r18CheckComplete) {
        document.getElementById("content_div").setAttribute("class", "pi_text");
    }
    aboutSplashScreenUp = false; //enable doujin info to appear
}

function displayInfoSplashScreen() {
    console.log("Splash screen begins");
    if (!aboutSplashScreenUp) { //only activate if the r18 check has been completed
        //blur out background and temporarily prevent doujin info from appearing
        document.getElementById("content_div").setAttribute("class", "pi_text overlay");
        aboutSplashScreenUp = true;

        var screen = document.createElement("div");
        screen.setAttribute("class", "splash_screen");
        screen.setAttribute("id", "infoSplashScreen");

        var logo = document.createElement("img");
        logo.setAttribute("src", "logo.svg");
        logo.setAttribute("style", "width:10vmax;");
        logo.setAttribute("title", "Does the logo have to be here? No, but I spent far too long making it to not use it at every opportunity");

        var text = document.createElement("text");
        text.setAttribute("class", "splash_screen_text");
        text.innerHTML = "<h1 title='Technically all of them, but thats not a satisfying answer.'>How many nhentai doujins are in π?</h1>" +
                         "Attempting to answer this simple question started this project. After answering that question I had a <i>good idea</i>&#153 " +
                         "and after roughly 40 hours of work this abomination has been unleashed upon the world." +
                         "<br><br><span title=\"I've spent more time casually looking at hentai in the past month than in the rest of my life combined\">God I'm a degenerate.</span><br><br>" +
                         "The bracket colours have no meaning, they're just to make it easier to pick out codes in dense segments. " +
                         "Currently <i title='/s'>only</i> ~20&nbsp000 digits of π, containing 6067 doujins can be accessed. I have run the doujin finder on 100&nbsp000 digits of π but having them on the website " +
                         "made it unbearably laggy as you scrolled further and further. Eventually I will add multiple pages to allow all 100&nbsp000 digits of filth and degeneracy to be " +
                         "reachable.<br><br>" +
                         "Contact: <a href='mailto:nhenpi@gmail.com'>nhenpi@gmail.com</a><br>" +
                         "GitHub: <a href='https://github.com/MjrMojo/nHenPi'>nHenPi</a><br><br><i class='smaller'>Please submit bug reports to the GitHub page</i><br><br>";

        var exitButton = document.createElement("button");
        exitButton.innerHTML += "Done";
        exitButton.setAttribute("onclick", "dismissInfoSplashScreen()");

        //var devModeButton = document.createElement("button");
        //devModeButton.innerHTML += "Enter Developer Mode";
        //devModeButton.setAttribute("onclick", "dismissSplashScreen()");

        screen.appendChild(logo);
        screen.appendChild(text);
        screen.appendChild(exitButton);
        //screen.appendChild(devModeButton);
        document.body.appendChild(screen);
    }
}

function displayR18SplashScreen() {
    //Displays the legally mandated splash screen
    var screen = document.createElement("div");
    screen.setAttribute("class", "splash_screen");
    screen.setAttribute("id", "r18SplashScreen");

    var logo = document.createElement("img");
    logo.setAttribute("src", "logo.svg");
    logo.setAttribute("style", "width:10vmax;");

    var text = document.createElement("text");
    text.setAttribute("class", "splash_screen_text");
    text.innerHTML = "<h1>AGE-RESTRICTED CONTENT WARNING</h1><br><h3>You must be 18 years of age or older to access this website</h3><br>I confirm that I am over 18 years of age, and understand that this website contains material featuring nudity and/or sexually-explicit material and/or adult themes that are age-restricted, and I confirm that by entering this website I agree that I am not offended by viewing such material.<br>";

    var enterButton = document.createElement("button");
    enterButton.innerHTML += "I'm over 18, let me in";
    enterButton.setAttribute("onclick", "dismissR18SplashScreen()");

    var newLine = document.createElement("text");
    newLine.innerHTML += "<br>"

    var exitButton = document.createElement("button");
    exitButton.innerHTML += "I'm under 18, get me outta here!";
    exitButton.setAttribute("onclick", "getUnder18sOuttaHere()");

    screen.appendChild(logo);
    screen.appendChild(text);
    screen.appendChild(enterButton);
    screen.appendChild(newLine);
    screen.appendChild(exitButton);
    document.body.appendChild(screen);
}

window.addEventListener('load', function () {
    placeInitalElements();
    displayR18SplashScreen();
    placeBraces(0, 25);
    checkToLoadMoreContent();
});

function isLastBraceInViewport(endBrace) {
    var elem = document.getElementById("bracket-" + endBrace);
    if (elem) {
        var bounding = elem.getBoundingClientRect();
        return bounding.right > (window.innerWidth || document.documentElement.clientWidth);
    } else {
        return false;
    }
};

function checkToLoadMoreContent(event) {
    while(!isLastBraceInViewport(currentEndBrace - 1)) {
        if (dataset[currentEndBrace + 25]['location'][1] > currentPiLength) {
            appendAnotherPiChunk();
        }
        var temp = Math.min(currentEndBrace + 25, 6067) //Only display 6067 brackets on the first page
        placeBraces(currentEndBrace, temp);
        currentEndBrace = temp;
    }
}

document.onscroll = checkToLoadMoreContent;

document.onwheel = function(event) {
    if (event.deltaY != 0) {
        window.scrollBy(event.deltaY, 0);
    }
};

//Function from https://stackoverflow.com/questions/43965616/getting-character-width-in-javascript
var calculateWordDimensions = function(text, classes, escape) {
    classes = classes || [];

    if (escape === undefined) {
        escape = true;
    }

    classes.push('textDimensionCalculation');

    var div = document.createElement('div');
    div.setAttribute('class', classes.join(' '));

    div.innerHTML = text;

    document.body.appendChild(div);

    var dimensions = {
        width : jQuery(div).outerWidth(),
        height : jQuery(div).outerHeight()
    };

    div.parentNode.removeChild(div);

    return dimensions;
};

function placeBraces(startBrace, endBrace) {
    var innerHTML = document.getElementById("pi_text").innerHTML;
    var sumOfBracketWidths = 0;

    var svg = document.createElementNS(null, "svg");

    for (var i = startBrace; i < endBrace; i++) {
        if (i == 0 && dataset[i]['location'][0] == 0) {
            var startIndex = dataset[i]['location'][0];
        } else {
            var startIndex = dataset[i]['location'][0] + 1;
        }
        var stopIndex = dataset[i]['location'][1] + 1;
        var startStr = innerHTML.substring(0, startIndex);

        var barPos = calculateWordDimensions(startStr).width;

        if (averageBracketWidth == 0) {
            var codeStr = innerHTML.substring(startIndex, stopIndex);
            var barWidth = calculateWordDimensions(codeStr).width;
            if (i != 0) { //ignore the first bracket as it has an extra character
                sumOfBracketWidths += barWidth
            }
        } else {
            var barWidth = averageBracketWidth;
        }

        makeCurlyBraceReal(i, barPos, barWidth, i % 2 == 1, i % 3);
    }

    if (averageBracketWidth == 0) {
        //We place 25 brackets at a time from the begining, however we ignore the first bracket as it is has a full stop
        //in it. So we need to divide the sumOfBracketWidths by 24 to get the average bracket width.
        averageBracketWidth = sumOfBracketWidths / 24;
    }
}

window.onresize = function(event){
    for (var i = 0; i < currentEndBrace; i++) {
        var el = document.getElementById("bracket-" + i);
        if (el) {
            el.parentNode.removeChild(el);
        }
    }

    var el = document.getElementById("doujin_info");
    if (el) {
        el.parentNode.removeChild(el);
    }

    currentEndBrace = 0;
    lastPiWidthIndex = 0;
    lasPiWidth = 0;
    averageBracketWidth = 0;
    checkToLoadMoreContent();

    //Manually replace the first bracket to make sure it is correct
    var el = document.getElementById("bracket-0");
    if (el) {
        el.parentNode.removeChild(el);
    }
    placeBraces(0, 1);
};

function handleMissingCover(image, media_id) {
    image.onerror = null;
    var req = new Request("/fetch_cover/" + media_id);
    image.src = "loading.gif";
    fetch(req).then(
        function (response) {
            if (response.ok) {
                image.src = "/covers/" + media_id + ".jpg";
            } else {
                throw new Error("Request failed to get image");
            }
        }).catch(function () {
            image.src = "error_loli.gif";
            image.setAttribute("title", "Something went wrong when getting this cover, try again");
        });
}

function createThumbnailElement(mediaID, imgWidth) {
    var thumbnail = document.createElement("img");
    thumbnail.setAttribute("src", "/covers/" + mediaID + ".jpg");
    if (mediaID == "obj") {
        thumbnail.setAttribute("title", "This doujin contains objectionable content so the cover cannot be displayed");
    }
    thumbnail.setAttribute("id", "overlay_thumnail");
    thumbnail.setAttribute("width", imgWidth + "px");
    thumbnail.setAttribute("style", "text-align:center; margin: 0px;");
    thumbnail.setAttribute("onerror", "this.onerror=handleMissingCover(this, " + mediaID + ")");
    return thumbnail
}


function createInfoDivInternals(key, div, text_at_top, imgWidth) {
    div.setAttribute("class", "item");
    var thumbnail = createThumbnailElement(dataset[key]['media_id'], imgWidth);

    var link = document.createElement("a");
    link.setAttribute("href", "https://nhentai.net/g/" + dataset[key]['key']);
    link.setAttribute("target", "_blank");
    link.appendChild(thumbnail);

    var title = document.createElement("p");
    title.innerHTML += dataset[key]['title'];
    title.setAttribute("class", "item_text");
    title.setAttribute("lang", dataset[key]["language"]);

    if (text_at_top) {
        div.appendChild(title);
        div.appendChild(link);
    } else {
        div.appendChild(link);
        div.appendChild(title);
    }
}

function onBraceHover(event){
    if (r18CheckComplete && !aboutSplashScreenUp) {
        //Load the cover page and title of the filth the user is currently hovering over
        key = parseInt(event.target.id.split('-')[1]);

        var prev_el = document.getElementById("doujin_info");
        if (prev_el) {
           if (prev_el.getAttribute('key') != key) {
               prev_el.parentNode.removeChild(prev_el);
           } else {
                //If we've already got the node out, don't bother replacing it
                return;
           }
        }

        var doujin_info = document.createElement("div");
        doujin_info.setAttribute("id", "doujin_info");

        createInfoDivInternals(key, doujin_info, false, event.target.offsetWidth * 1.20);

        var style = "";
        if (key % 2 == 0) {
            style += "position: absolute; bottom: ";
            style += 4.75;
        } else {
            style += "position: absolute; top: ";
            style += 5;
        }
        style += "vmax; left: "
        if (key != 0) {
            style += event.target.offsetLeft - 0.10 * event.target.offsetWidth;
        } else {
            style += event.target.offsetLeft;
        }
        style += "px; width: ";
        style += event.target.offsetWidth * 1.20;
        style += "px; text-align: center; background-color: #404040;"
        doujin_info.setAttribute("style", style);
        doujin_info.setAttribute("key", key);

        document.getElementById("content_div").appendChild(doujin_info);
    }
}


function makeCurlyBraceReal(id, xpos, width, isBottom, colour){
    var newBrace = document.createElement('img');
    newBrace.setAttribute("src", "bracket.png");
    newBrace.setAttribute("id", "bracket-" + id);
    if (isBottom) {
        //Bottom brace
        newBrace.setAttribute("class", "bottom_brace");
    } else {
        //Top brace
        newBrace.setAttribute("class", "top_brace");
    }

    switch (colour) {
        //filtering operations calculated with this tool: https://codepen.io/sosuke/pen/Pjoqqp
        case 1: //red
            newBrace.setAttribute("class", newBrace.getAttribute("class") + " red");
            break;
        case 2: //blue
            newBrace.setAttribute("class", newBrace.getAttribute("class") + " blue");
            break;
        default:
            //filter to grey
            newBrace.setAttribute("class", newBrace.getAttribute("class") + " grey");
            break;
    }

    var style = "";
    style += "left: ";
    style += xpos;
    style += "px;";
    newBrace.setAttribute("style", style);
    newBrace.setAttribute("width", width + "px");
    newBrace.onmouseover = onBraceHover;
    document.getElementById("content_div").appendChild(newBrace);
}
