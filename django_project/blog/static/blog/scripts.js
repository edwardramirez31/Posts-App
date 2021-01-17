function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function sendPost(url) {
    const csrftoken = getCookie('csrftoken');
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", url, true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.send();
}
    

function handleFavorites(url, url2, postID) {
    var anchor = document.getElementById('fav-'+postID);
    if (anchor.className.includes("btn-favorite")){
        sendPost(url2);
        anchor.classList.replace("btn-favorite", "btn-no-favorite");
    } else {
        sendPost(url);
        anchor.classList.replace("btn-no-favorite", "btn-favorite");
    }
}
    
function editComment(url, commentID) {
    var [ul, li, text] = getElements(commentID);

    var input = document.getElementById('id_text');
    input.value = text;
    ul.removeChild(li);
    // sending the post request
    var form = document.getElementsByTagName("form")[1];
    form.action = url;
    //*Obtener el boton y cambiarle el tipo, agregarle un evento
}
function getElements(commentID) {
    var ul = document.getElementsByClassName("list-group")[0];
    var li = document.getElementById('comment-' + commentID);
    var text = document.getElementById('comment-text-' + commentID).innerHTML;
    return [ul, li, text];
}

function postAJAX(url, csrftoken) {
    var xhttp = new XMLHttpRequest();
    xhttp.open('POST', url, true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken)
    xhttp.send();
    console.log(csrftoken)
}

function deleteComment(url, commentID, csrftoken) {
    var [ul, li, ...rest] = getElements(commentID);
    ul.removeChild(li);
    postAJAX(url, csrftoken);
    console.log(url);
}