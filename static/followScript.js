var follow_xhr;
var unfollow_xhr;
var user_to_unfollow;
var user_to_follow;

function follow(){
	var params = "";
}

function unfollowRequest(){
	if (follow_xhr.readyState == 4){  
      if (follow_xhr.status == 200){
      	var post;
      	while ((post = document.getElementsByName("post_user" + user_to_unfollow)) != null){
      		post[0].remove();
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

function followRequest(){
	if (follow_xhr.readyState == 4){  
	  if (follow_xhr.status == 200){
	  	document.getElementById("follow_user" + user_to_follow).style = "float:right; display:none;";
	  	document.getElementById("unfollow_user" + user_to_follow).style = "float:right; display:inline;";
	  	//document.getElementById("main-container_followed").style = "display:inline;"
		document.getElementById("user_followed_container").innerHTML += follow_xhr.responseText;
	  	//add the right div
		}
	  	else {
		    alert(follow_xhr.status + " : " + follow_xhr.responseText);
		  }
	  }  
	}

function searchUnfollowRequest(){
	if (unfollow_xhr.readyState == 4){  
	  if (unfollow_xhr.status == 200){
	  	document.getElementById("unfollow_user" + user_to_unfollow).style = "float:right; display:none;";
	  	document.getElementById("follow_user" + user_to_unfollow).style = "float:right; display:inline;";
	  	document.getElementById("followed_user" + user_to_unfollow).remove();
		}
	  	else {
		    alert(unfollow_xhr.status + " : " + unfollow_xhr.responseText);
		  }
	  }  
	}

	function followedUnfollowRequest(){
	if (unfollow_xhr.readyState == 4){  
	  if (unfollow_xhr.status == 200){
	  	document.getElementById("followed_user" + user_to_unfollow).remove();
	  	var v = document.getElementById("unfollow_user" + user_to_unfollow);
	  	if (v != null){
	  		v.style = "display:none;"
	  		document.getElementById("follow_user"+ user_to_unfollow).style = "float:right;display:inline";
	  	}
		}
	  	else {
		    alert(unfollow_xhr.status + " : " + unfollow_xhr.responseText);
		  }
	  }  
	}

function search_follow(user_id){
	var params = "?user_id=" + user_id;
	user_to_follow = user_id;
	follow_xhr = new XMLHttpRequest();
	follow_xhr.open("GET", "/follow" + params);
	follow_xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	follow_xhr.send();
	follow_xhr.onreadystatechange = followRequest;
}

function search_unfollow(user_id){
	var params = "?user_id=" + user_id;
	user_to_unfollow = user_id;
	unfollow_xhr = new XMLHttpRequest();
	unfollow_xhr.open("GET", "/unfollow" + params);
	unfollow_xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	unfollow_xhr.send();
	unfollow_xhr.onreadystatechange = searchUnfollowRequest;
}

function followed_unfollow(user_id){
	var params = "?user_id=" + user_id;
	user_to_unfollow = user_id;
	unfollow_xhr = new XMLHttpRequest();
	unfollow_xhr.open("GET", "/unfollow" + params);
	unfollow_xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	unfollow_xhr.send();
	unfollow_xhr.onreadystatechange = followedUnfollowRequest;
}