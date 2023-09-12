function color_save(x , id='save'){
    if (x == 'active') {
      
      document.getElementById( id + "-a").style.color = '#ffff';
      document.getElementById( id + "-i").style.backgroundColor = 'black';

    }
    else {
      document.getElementById( id + "-a").style.color = 'black';
      document.getElementById( id + "-i").style.backgroundColor = '#ffff';
    };

}



function save(id='save'){
    const xhr = new XMLHttpRequest();
    var post_id = document.getElementById(id + '-a').getAttribute('value')
    xhr.open("POST", "http://127.0.0.1:5000/posts/save/" + post_id);
    xhr.send();
    xhr.responseType = "json";
    xhr.onload = () => {
      if (xhr.readyState == 4 && xhr.status == 200) {
        const data = xhr.response;
        if (data == 0){
          Swal.fire("" , 'The post has been successfully saved');
          color_save('active' , id );
        }
        else{
          Swal.fire("" , 'Removed from saved posts');
          color_save('diactive' ,  id);
        }
  
      } else {
        console.log(`Error: ${xhr.status}`);
        Swal.fire("" , 'The post was not saved successfully');
      }
    };
  }