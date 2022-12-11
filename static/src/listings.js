function http_get(url, callback, headers=[], method="GET", content=null) {
  let request = new XMLHttpRequest();
  request.addEventListener("load", callback);
  request.open(method, url, true);
  for (const header of headers) {
    request.setRequestHeader(header[0], header[1]);
  }
  request.send(content);
}

var address_input = document.getElementById("address");
var address_list = document.getElementById("address_list");
var old_content = "";

function update() {
  let content = address_input.value;
  if (content == old_content) {
    return;
  }
  old_content = content;

  let url = `https://nominatim.openstreetmap.org/search.php?q=${content}&format=jsonv2`;
  http_get(url, function(){
    let data = JSON.parse(this.responseText);
    address_list.innerHTML = "";
    for (let entry of data) {
      if (entry.category != "building") {
        continue;
      }
      let option = document.createElement("option");
      option.value = entry.display_name;
      address_list.appendChild(option);
      console.log(entry.display_name)
    }
  });
}

address_input.onchange = update;
address_input.onkeydown = update;
address_input.setAttribute("list", "address_list");