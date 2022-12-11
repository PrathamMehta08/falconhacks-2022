function toggle_navbar() {
    let div = document.getElementById("header_links")
    if (div.className.includes("hidden")) {
        div.className = div.className.replace(" hidden", "")
    }
    else {
        div.className += " hidden"
    }
}