window.onload = function(){
  var el = document.getElementById("waypoint"); 
  console.log(el)
// To set the scroll
  el.scrollTop = 600;
}

// SETTING EMOJI PICKER
var emoji = document.getElementById("emoji-button");
var input = document.getElementById("id_input");
var picker = new EmojiButton({
  position: 'top-start',
  autoHide: false,
  emojiSize: '64px',
  emojisPerRow: 4,
  rows: 4
})
picker.on('emoji', selection => {
  // handle the selected emoji here
  input.value += selection;
});
emoji.addEventListener('click', () => {
  picker.pickerVisible ? picker.hidePicker() : picker.showPicker(emoji); 
});

// CHAT MESSAGES PAGINATION

var spinner = document.getElementById('spinner');

var waypoint = new Waypoint({
  element: document.getElementById('msg_container'),
  handler: function(direction) {
    if (direction === 'up' && pageCounter < numPages){
      pageCounter ++;
      console.log(pageURL + '?page=' + pageCounter)
      spinner.classList.remove('d-none');
      fetch(pageURL + '?page=' + pageCounter)
      .then(response => {
        if (response.ok) {
          return response.text();
        } else {
          console.log('Error: ' + response.status);
        }
      })
      .then(data => {
        var template = document.createElement('html');
        data = data.trim(); 
        template.innerHTML = data;
        var element = template.querySelector('#msg_container');
        element.id = "";
        let parent = document.getElementById('msg_container');
        parent.insertAdjacentHTML('afterbegin', element.outerHTML);
        spinner.classList.add('d-none');
        })
      .catch(err => console.log(err));
      
    }
  }, 
  context: document.getElementById('waypoint'),
  offset: -5,
});