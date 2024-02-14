function color_save(x, post_id) {
    console.log(post_id);
    if (x == 'active') {

        document.getElementById(post_id + "-save-a").style.color = '#ffff';
        document.getElementById(post_id + "-save-i").style.backgroundColor = 'black';

    }
    else {
        document.getElementById(post_id + "-save-a").style.color = 'black';
        document.getElementById(post_id + "-save-i").style.backgroundColor = '#ffff';
    };

}



function save(element) {
    const xhr = new XMLHttpRequest();
    var post_id = element.getAttribute('post-id')

    xhr.open("POST", `/posts/save/${post_id}`);
    xhr.send();
    xhr.responseType = "json";

    xhr.onload = () => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            const data = xhr.response;
            if (data == 0) {
                Swal.fire("", 'The post has been successfully saved');
                color_save('active', post_id);
            }
            else {
                Swal.fire("", 'Removed from saved posts');
                color_save('diactive', post_id);
            }

        } else {
            console.log(`Error: ${xhr.status}`);
            Swal.fire("", 'The post was not saved successfully');
        }
    };
}