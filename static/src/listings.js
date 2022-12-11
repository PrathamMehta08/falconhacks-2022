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
var queued_request = null;

function get_addresses(query) {
  let url = `https://nominatim.openstreetmap.org/search.php?q=${query}&format=jsonv2`;
  http_get(url, function(){
    let data = JSON.parse(this.responseText);
    address_list.innerHTML = "";
    for (let entry of data) {
      if (entry.category != "building") {
        continue;
      }
      let option = document.createElement("li");
      option.innerHTML = entry.display_name;
      address_list.appendChild(option);
      option.className = "even:bg-gray-200 odd:bg-gray-100 m-2";
      console.log(entry.display_name)
    }
    if (queued_request != query) {
      get_addresses(queued_request)
      queued_request = query;
    }
    else {
      queued_request = null;
    }
  });
}

function update() {
  let content = address_input.value;
  if (content == old_content) {
    return;
  }
  old_content = content;

  if (content != "") {
    if (queued_request == null) {
      get_addresses(content);
      queued_request = content;
    }
    queued_request = content;
  }
  else {
    address_list.innerHTML = "";
  }

}

address_input.onchange = update;
address_input.onkeydown = update;
