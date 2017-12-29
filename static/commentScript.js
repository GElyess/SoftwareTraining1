/////COMMENT SCRIPT

  var comment_edit_xhr;
  var comment_delete_xhr;
  var comment_like_xhr;
  var comment_unlike_xhr;
  var comment_post_xhr;

  var post_to_comment = null;
  var comment_to_delete = null;
  var comment_to_edit = null;
  var comment_to_like = null;
  var coment_to_unlike = null;

  function postCommentRequest(){
    if (comment_post_xhr.readyState == 4){  
      if (comment_post_xhr.status == 200){
        var newDiv = document.createElement('div');
        var parent = document.getElementById("parent_post" + post_to_comment)
        newDiv.innerHTML = comment_post_xhr.responseText;
        parent.appendChild(newDiv);
        if (parent.firstChild)
          parent.insertBefore(newDiv, parent.firstChild);
        else
          parent.appendChild(newDiv);
        post_to_comment=null;

      }
      else if (comment_post_xhr.status == 400){
          window.location = "/logout"
        }
      else {
        alert(comment_post_xhr.responseText);
      }
    }
  }

  function post_comment(post_id){
    var content = document.getElementById('comment_content_post_' + post_id).value;

    if (content == "")
      return false;
    post_to_comment = post_id;
    var params = "comment_content=" + content + "&post_id=" + post_id;
    comment_post_xhr = new XMLHttpRequest();
    comment_post_xhr.open("POST", "/comment/post");
    comment_post_xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    comment_post_xhr.send(params);
    comment_post_xhr.onreadystatechange = postCommentRequest;
  }

  function editRequest(){
    if (comment_edit_xhr.readyState == 4){  
      if (comment_edit_xhr.status == 200){
        document.getElementById( 'validate_' + comment_to_edit ).setAttribute('style', 'display:none;');
        show(comment_to_edit);

       comment_to_edit = null;
      }
      else if (comment_edit_xhr.status == 400){
          window.location = "/logout"
        }
      else {
        alert(comment_edit_xhr.responseText);
      }
    }
  }


  function submit_edit(comment_id, post_id){
    comment_edit_xhr = new XMLHttpRequest();
    var content = document.getElementById('text_' + comment_id).value;
    var params = "comment_id=" + comment_id + "&post_id=" + post_id + "&content=" + content;
    comment_edit_xhr.open("POST", "/comment/update");
    comment_edit_xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    comment_edit_xhr.send(params);
    comment_edit_xhr.onreadystatechange = editRequest;
  }

  var post_edit_xhr;
  var post_to_edit = null;
  function postUpdateRequest(){
    if (post_edit_xhr.readyState == 4){  
      if (post_edit_xhr.status == 200){
        //document.getElementById( 'validate_' + comment_to_edit ).setAttribute('style', 'display:none;');
        //show(comment_to_edit);
        document.getElementById('edit_post_' + post_to_edit).style.display = 'inline';
        document.getElementById('validate_post' + post_to_edit).style.display = 'none';
        var text = document.getElementById('text_post_' + post_to_edit);
        var hint = text.value;
        text.setAttribute('disabled', true);
        text.setAttribute('placeholder', hint);
        //text.placeholder = hint;
        text.value = null;

       post_to_edit = null;
      }
      else if (post_edit_xhr.status == 400){
          window.location = "/logout"
        }
      else {
        alert(post_edit_xhr.status + " : " + post_edit_xhr.responseText);
      }
    }
  }

  function submit_post_edit(id){
    var content = document.getElementById('text_post_' + id);
    if (content.value == ""){
      content.focus();
      return false;
    }
    var params = "content=" + content.value + "&post_id=" + id;
    post_edit_xhr = new XMLHttpRequest();
    post_edit_xhr.open("POST", "/post/update");
    post_edit_xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    post_edit_xhr.send(params);
    post_edit_xhr.onreadystatechange = postUpdateRequest;
  }

  function edit_post(id){
    var text = document.getElementById("text_" + id);
    if (post_to_edit != null){
      document.getElementById("validate_post" + post_to_edit).setAttribute('style', 'display:none;');
      

      document.getElementById('edit_post_' + post_to_edit).style.display = 'inline';
      var text = document.getElementById('text_post_' + post_to_edit);
      var hint = text.value;
      text.setAttribute('disabled', true);
      text.setAttribute('placeholder', hint);
      //text.placeholder = hint;
      text.value = null;
    }
    document.getElementById('validate_post' + id).setAttribute('style', '');
    

    document.getElementById('edit_post_' + id).style.display = 'none'; 
    var text = document.getElementById('text_post_' + id);
    var hint = text.getAttribute('placeholder')
    text.removeAttribute('disabled'); 
    text.removeAttribute('placeholder')
    text.value = hint;
    //hide(comment_id);
    post_to_edit = id;
  }


    function hide_comment(id) {
        //alert("hiding");
        document.getElementById('edit_' + id).style.display = 'none'; 

        var text = document.getElementById('text_' + id);
        var hint = text.getAttribute('placeholder')
        text.removeAttribute('disabled'); 
        text.removeAttribute('placeholder')
        text.value = hint;
    } 


    function show_comment(id){
        document.getElementById('edit_' + id).style.display = 'inline'; 

        var text = document.getElementById('text_' + id);
        var hint = text.value;
        text.setAttribute('disabled', true);
        text.setAttribute('placeholder', hint);
        //text.placeholder = hint;
        text.value = null;
    }


  function edit_comment(comment_id){
    if (comment_to_edit != null){
      document.getElementById( 'validate_' + comment_to_edit ).setAttribute('style', 'display:none;');
      show_comment(comment_to_edit);
    }
    document.getElementById( 'validate_' + comment_id ).setAttribute('style', ''); 
    comment_to_edit = comment_id;
    hide_comment(comment_id);
       
  }


  function deleteRequest(){
    if (comment_delete_xhr.readyState == 4){  
      if (comment_delete_xhr.status == 200){
        document.getElementById("comment_div_" + comment_to_delete).remove();
        //elem.innerHTML = xhr.responseText;
      }
      else if (comment_delete_xhr.status == 400){
          window.location = "/logout"
        }
      else {
        alert(comment_delete_xhr.responseText);
        //elem.innerHTML = 
      }
      comment_to_delete = null;
    }
  }

  function delete_comment(comment_id, post_id){
    comment_delete_xhr = new XMLHttpRequest();
    comment_to_delete = comment_id;
    var params = "?comment_id=" + comment_id + "&post_id=" + post_id;
    comment_delete_xhr.open("GET", "/comment/delete" + params, true);
    comment_delete_xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    comment_delete_xhr.send();
    comment_delete_xhr.onreadystatechange = deleteRequest;
    return true;
  }


function likeRequest(){
    if (comment_like_xhr.readyState == 4){  
      if (comment_like_xhr.status == 200){
        document.getElementById("likes_comment_" + comment_to_like).style.display = "none";
        document.getElementById("dislikes_comment_" + comment_to_like).style.display = "inline";
        var likes = document.getElementById("nb_likes_comment_" + comment_to_like);
        inc = parseInt(likes.innerHTML) + 1;
        likes.innerHTML = inc;
      }
      else if (comment_like_xhr.status == 400){
          window.location = "/logout"
        }
      else {
        alert(comment_like_xhr.responseText);
      }
      comment_to_like = null;
    }
  }

function like_comment(post_id, comment_id){
   comment_like_xhr = new XMLHttpRequest();
   comment_to_like = comment_id;
   var params = "?comment_id=" + comment_id + "&post_id=" + post_id;
   comment_like_xhr.open("GET", "/comment/like" + params, true);
   comment_like_xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
   comment_like_xhr.send();
   comment_like_xhr.onreadystatechange = likeRequest;
  }

  function unlikeRequest(){
    if (comment_unlike_xhr.readyState == 4){  
      if (comment_unlike_xhr.status == 200){
        document.getElementById("likes_comment_" + comment_to_unlike).style.display = "inline";
        document.getElementById("dislikes_comment_" + comment_to_unlike).style.display = "none";
        var likes = document.getElementById("nb_likes_comment_" + comment_to_unlike);
        inc = parseInt(likes.innerHTML) - 1;
        likes.innerHTML = inc;
      }
      else if (comment_unlike_xhr.status == 400){
          window.location = "/logout"
        }
      else {
        alert(comment_unlike_xhr.responseText);
      }
      comment_to_unlike = null;
    }
  }

  function dislike_comment(post_id, comment_id){
    comment_unlike_xhr = new XMLHttpRequest();
   comment_to_unlike = comment_id;
   var params = "?comment_id=" + comment_id + "&post_id=" + post_id;
   comment_unlike_xhr.open("GET", "/comment/unlike" + params, true);
   comment_unlike_xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
   comment_unlike_xhr.send();
   comment_unlike_xhr.onreadystatechange = unlikeRequest;
  }