function color_save(x){
    if (x == 'active') {
      
      document.getElementById("save-a").style.color = '#ffff';
      document.getElementById("save-i").style.backgroundColor = 'black';

    }
    else {
      document.getElementById("save-a").style.color = 'black';
      document.getElementById("save-i").style.backgroundColor = '#ffff';
    };

}

function save(){
    const xhr = new XMLHttpRequest();
    var post_id = document.getElementById('save-a').getAttribute('value')
    xhr.open("POST", "http://127.0.0.1:5000/blog/posts/save/" + post_id);
    xhr.send();
    xhr.responseType = "json";
    xhr.onload = () => {
      if (xhr.readyState == 4 && xhr.status == 200) {
        const data = xhr.response;
        if (data == 0){
          Swal.fire("" , 'The post has been successfully saved');
          color_save('active');
        }
        else{
          Swal.fire("" , 'Removed from saved posts');
          color_save('diactive');
        }
  
      } else {
        console.log(`Error: ${xhr.status}`);
        Swal.fire("" , 'The post was not saved successfully');
      }
    };
  }