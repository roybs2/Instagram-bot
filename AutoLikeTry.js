tags = "dreaming,dremland,dreamworld,dreamers,successful,icandoit,dreamliveacheieve,live,livingthedream,success,dream,dreambig,dreamscometrue,inspire,inspirelife,inspirationalquotes,inspiration,inspirational,dreams,dreamer,dream,successquotes,successstory,achieve,create,dontstop"
var array = tags.split(',');
window.location.href = 'https://www.instagram.com/explore/tags/'+array[0];
posts = document.getElementsByClassName('_9AhH0');
for(var i = 0; i < posts.length; i++){
	posts[i].click();
	var like = document.getElementsByClassName('glyphsSpriteHeart__outline__24__grey_9')
	try{
		like[0].click();
		window.history.back();
	}
	catch(err) {
		console.log("Error: " + err);
		window.history.back();
	}
}