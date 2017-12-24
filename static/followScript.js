var follow_xhr;
var unfollow_xhr;
var user_to_unfollow;

function follow(){
	var params = "";
}

function unfollowRequest(){
	if (follow_xhr.readyState == 4){  
      if (follow_xhr.status == 200){
      	var post;
      	while ((post = document.getElementById("post_followed_" + user_to_unfollow)) != null){
      		post.remove();
      	}
      }
      else {
        alert(follow_xhr.responseText);
      }
    }
}

function stop_following(id){
	var params = "user_id=" + id;
	user_to_unfollow = id;
	follow_xhr = new XMLHttpRequest();
	follow_xhr.open("GET", "/unfollow/blog?" + params);
	follow_xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	follow_xhr.send();
	follow_xhr.onreadystatechange = unfollowRequest;
}