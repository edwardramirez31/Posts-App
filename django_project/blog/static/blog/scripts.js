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
    

function handleFavorites(url, url2, id) {
    var anchor = document.getElementById(id);
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
    // https://developer.mozilla.org/es/docs/Web/API/EventTarget/addEventListener
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

// following
function follow(url, url2, id) {
    sendPost(url);
    let element = document.getElementById(id);
    let inner = `
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-check-fill" viewBox="0 0 16 16">
        <path fill-rule="evenodd" d="M15.854 5.146a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 0 1 .708-.708L12.5 7.793l2.646-2.647a.5.5 0 0 1 .708 0z"/>
        <path d="M1 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H1zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>
    </svg>
    `
    element.innerHTML = inner;
    element.className = "badge btn-light text-dark";
    element.setAttribute('onclick', `unFollow('${url2}', '${url}', ${id}); return false;`);
    let message = `
    <a class="badge btn-light text-dark me-1" href="${messageURL}" id="message">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chat-dots-fill" viewBox="0 0 16 16">
        <path d="M16 8c0 3.866-3.582 7-8 7a9.06 9.06 0 0 1-2.347-.306c-.584.296-1.925.864-4.181 1.234-.2.032-.352-.176-.273-.362.354-.836.674-1.95.77-2.966C.744 11.37 0 9.76 0 8c0-3.866 3.582-7 8-7s8 3.134 8 7zM5 8a1 1 0 1 0-2 0 1 1 0 0 0 2 0zm4 0a1 1 0 1 0-2 0 1 1 0 0 0 2 0zm3 1a1 1 0 1 0 0-2 1 1 0 0 0 0 2z"/>
        </svg>
    </a>
    `
    element.insertAdjacentHTML('beforebegin', message);

}

function unFollow(url, url2, id) {
    sendPost(url);
    let element = document.getElementById(id);
    let message = document.getElementById("message");
    message.remove();
    let inner = `Follow`
    element.innerHTML = inner;
    element.className = "badge btn-primary btn";
    element.setAttribute('onclick',`follow('${url2}', '${url}', ${id}); return false;`); 
}



var current_crop;
var x_input = document.getElementById('x');
var y_input = document.getElementById('y');
var width_input = document.getElementById('width');
var height_input = document.getElementById('height');
// cropping
function readURL() {
    const my_img = document.getElementById("myimg");
    const input = document.getElementById("id_image");
    if(input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = e => {
            my_img.src = e.target.result;

            if (current_crop) {
                current_crop.destroy();
            }
            var cropper = new Cropper(my_img, {
                aspectRatio: 1 / 1,
                crop(event) {
                    console.log(event.detail.x);
                    x_input.value = event.detail.x;
                    console.log(event.detail.y);
                    y_input.value = event.detail.y;
                    console.log(event.detail.width);
                    width_input.value = event.detail.width;
                    console.log(event.detail.height);
                    height_input.value = event.detail.height;
                },
            });
            current_crop = cropper;
            

        };
        reader.readAsDataURL(input.files[0]);
    }

}
document.querySelector('#id_image').addEventListener('change', async () => {
    readURL();
});

$(document).ready(function () {
    const myimg = document.getElementById("myimg");
    var div = document.getElementById("div_id_image");
    myimg.src = div.children[1].children[0].href;
    var cropper = new Cropper(myimg, {
        aspectRatio: 1 / 1,
        crop(event) {
            console.log(event.detail.x);
            x_input.value = event.detail.x;
            console.log(event.detail.y);
            y_input.value = event.detail.y;
            console.log(event.detail.width);
            width_input.value = event.detail.width;
            console.log(event.detail.height);
            height_input.value = event.detail.height;
        },
    });
    current_crop = cropper;

   
});

