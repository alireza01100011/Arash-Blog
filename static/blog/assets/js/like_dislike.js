function color_like(){
    document.getElementById("like-a").style.color = '#ffff';
    document.getElementById("like-i").style.backgroundColor = 'black';

    document.getElementById("dislike-a").style.color = 'black';
    document.getElementById("dislike-i").style.backgroundColor = '#ffff';
}

function color_dislike(){
    document.getElementById("like-a").style.color = 'black';
    document.getElementById("like-i").style.backgroundColor = '#ffff';

    document.getElementById("dislike-a").style.color = '#ffff';
    document.getElementById("dislike-i").style.backgroundColor = 'black';
}

function like(){
    const xhr = new XMLHttpRequest();
    var post_id = document.getElementById('like-a').getAttribute('value')
    xhr.open("POST", "http://127.0.0.1:5000/blog/posts/like/" + post_id);
    xhr.send();
    xhr.responseType = "json";
    xhr.onload = () => {
      if (xhr.readyState == 4 && xhr.status == 200) {
        const data = xhr.response;
        console.log('The post has been successfully liked');
        Swal.fire("" , 'The post has been successfully liked');
        color_like()
      } else {
        console.log(`Error: ${xhr.status}`);
        Swal.fire("" , 'The post was not liked successfully');
      }
    };
}

function dislike(){
    const xhr = new XMLHttpRequest();
    var post_id = document.getElementById('dislike-a').getAttribute('value')
    xhr.open("POST", "http://127.0.0.1:5000/blog/posts/dislike/" + post_id);
    xhr.send();
    xhr.responseType = "json";
    xhr.onload = () => {
      if (xhr.readyState == 4 && xhr.status == 200) {
        const data = xhr.response;
        console.log('The post has been successfully disliked');
        Swal.fire("" , 'The post has been successfully disliked');
        color_dislike()
      } else {
        console.log(`Error: ${xhr.status}`);
        Swal.fire("" , 'The post was not liked successfully');
      }
    };
}