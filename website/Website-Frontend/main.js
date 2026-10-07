	fetch('https://qumxdwo7w1.execute-api.us-east-1.amazonaws.com/default/VisitorCounter')
  	.then(response => {
		if(response.ok) {
		}
		return response.json();
	})
  	.then(data => {
    document.getElementById("VisitorCounter").textContent = data["visitorcount"]
	})