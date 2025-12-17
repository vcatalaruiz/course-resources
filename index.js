window.onload = function () {
    var query = window.location.search.substring(1);
    var id = query.split("=")[1].toLowerCase();
    console.log(id);
    switch (id) {
        case 'linkia':
            document.getElementById("logo").style.display = 'block';
            document.getElementById("logo").setAttribute("src", "../assets/linkia_logo.jpeg");
            break;
    
    }
    

}