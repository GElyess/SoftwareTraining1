var xhr_addpost = null;

  function postAddRequest(){
    if (xhr_addpost.readyState == 4){
      if (xhr_addpost.status == 200){
         //add the div
         var newDiv = document.createElement('div');
        var parent = document.getElementById("parent_user_posts");
        if (parent == null){
          var top = document.getElementById("top");
          var newParent = document.createElement('div');
          newParent.innerHTML = '<h1>My posts:</h1><div id="main-container" class="span7 center" style="width: 70%; margin-left: 15%; "><div class = "jumbotron" id="parent_user_posts" style="border-radius: 5px;"></div></div>';

          top.parentNode.insertBefore(newParent, top.nextSibling);
          parent = document.getElementById("parent_user_posts");
         }

        newDiv.innerHTML = xhr_addpost.responseText;
        parent.appendChild(newDiv);
        if (parent.firstChild)
          parent.insertBefore(newDiv, parent.firstChild);
        else
          parent.appendChild(newDiv);
            }
        else if (xhr_addpost.status == 400){
          window.location = "/logout"
        }
            else{
                alert(xhr.responseText);
            }
            xhr_addpost = null;
        }
  }

  function addpost(){
    var text = document.getElementById("post_add_content");
    if (text.value == ""){
      text.focus();
      return false;
    }
    xhr_addpost = new XMLHttpRequest();
    var params = "content=" + text.value;
    xhr_addpost.open("POST", "/post/post");
    xhr_addpost.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr_addpost.send(params);
    xhr_addpost.onreadystatechange = postAddRequest;
    return true;
  }

  function hide(id) {
    //alert("hiding");
        document.getElementById('edit_' + id).style.display = 'none'; 

        var text = document.getElementById('text_' + id);
        var hint = text.getAttribute('placeholder')
        text.removeAttribute('disabled'); 
        text.removeAttribute('placeholder')
        text.value = hint;
    } 


    function show(id){
        document.getElementById('edit_' + id).style.display = 'inline'; 

        var text = document.getElementById('text_' + id);
        var hint = text.value;
        text.setAttribute('disabled', true);
        text.setAttribute('placeholder', hint);
        //text.placeholder = hint;
        text.value = null;
    }

  var delete_post_xhr = null;
  var post_to_delete = null;

  function deletePostRequest(){
     if (delete_post_xhr.readyState == 4){  
      if (delete_post_xhr.status == 200){
        var container = document.getElementById("main_container_post" + post_to_delete);
        if (container != null){
          container.remove();
        }
      }
      else if (delete_post_xhr.status == 400){
          window.location = "/logout"
        }
      else {
        alert(delete_post_xhr.responseText);
        //elem.innerHTML = 
      }
    }
  }

  function delete_post(id){
    //var location = '/post/delete?post_id=' + id;
    //window.location.href = location;
    var params = "post_id=" + id;
    post_to_delete = id;
    delete_post_xhr = new XMLHttpRequest();
    delete_post_xhr.open("GET", "/post/delete?" + params);
    delete_post_xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    delete_post_xhr.send(params);
    delete_post_xhr.onreadystatechange = deletePostRequest;
    return true;
  }

  function goto_comment(id){
      var location = '/blog_comment?post_id=' + id;
      window.location.href = location;
    }


  var xhr = null;
  var elem = null;

  function show_comments(id){
    elem = document.getElementById('comments_' + id);
    elem.style.display="inline";
    elem.className = "comment_section";
    xhr = new XMLHttpRequest();
    var params = "?post_id=" + id;
    xhr.open("GET", "/comment/list" + params, true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send(params);
    xhr.onreadystatechange = processRequest;
    return true;
  }

  function processRequest() {                                 
    if (xhr.readyState == 4){  
      if (xhr.status == 200){
         //document.getElementById("comment_div_" + comment_to_delete).remove();
        elem.innerHTML = xhr.responseText;
      }
      else if (xhr.status == 400){
          window.location = "/logout"
        }
      else {
        alert(xhr.responseText);
        //elem.innerHTML = 
      }
    }
  }





  var like_xhr = null;
  comment_to_like = null;
  function postLikeRequest(){
    if (like_xhr.readyState == 4){  
      if (like_xhr.status == 200){
        document.getElementById("like_post_" + comment_to_like).style.display = "none";
        document.getElementById("dislike_post_" + comment_to_like).style.display = "inline";
        var nbLikes = document.getElementById("nb_likes_post_" + comment_to_like);
        var value = parseInt(nbLikes.innerHTML) + 1;
        nbLikes.innerHTML = value;
      }
      else if (like_xhr.status == 400){
          window.location = "/logout"
        }
      else {
        alert(like_xhr.responseText);
      }
    }
  }

  function like_post(id){
    var params = "post_id=" + id;
    like_xhr = new XMLHttpRequest();
    like_xhr.open("GET", "/post/like?" + params);
    like_xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    like_xhr.send(params);
    like_xhr.onreadystatechange = postLikeRequest;
    comment_to_like = id;
    return true;

   
  }

  var dislike_xhr = null;
  comment_to_dislike = null;
  function postDislikeRequest(){
    if (dislike_xhr.readyState == 4){  
      if (dislike_xhr.status == 200){
        document.getElementById("like_post_" + comment_to_dislike).style.display = "inline";
        document.getElementById("dislike_post_" + comment_to_dislike).style.display = "none";
        var nbLikes = document.getElementById("nb_likes_post_" + comment_to_dislike);
        var value = parseInt(nbLikes.innerHTML) - 1;
        nbLikes.innerHTML = value;
      }
      else if (dislike_xhr.status == 400){
          window.location = "/logout"
        }
      else {
        alert(dislike_xhr.responseText);
      }
    }
  }

  function dislike_post(id){
    var params = "post_id=" + id;
    dislike_xhr = new XMLHttpRequest();
    dislike_xhr.open("GET", "/post/unlike?" + params);
    dislike_xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    dislike_xhr.send(params);
    dislike_xhr.onreadystatechange = postDislikeRequest;
    comment_to_dislike = id;
  }

   function switch_to_form(id){
    document.getElementById( 'validate_' + id ).setAttribute('style', '');
    document.getElementById( 'text_' + id ).setAttribute('style', '');
     document.getElementById( 'nonform_text_' + id ).setAttribute('style', 'display:none');
    hide(id);

  }