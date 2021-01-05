var planetsPage = document.querySelector("#planets-page");
var generate = document.querySelector("#generate");
var worldName = document.querySelector("#worldName");
var getList = document.querySelector("#getList");
var newPlanet = document.querySelector("#newPlanet");
var newWorld = document.querySelector("#newWorld");
var ringsTextField = document.querySelector("#ringsField");
var colorTextField = document.querySelector("#colorField");
var shapeTextField = document.querySelector("#shapeField");

var firstNameBox = document.querySelector("#first-name-box");
var lastNameBox = document.querySelector("#last-name-box");
var emailBox = document.querySelector("#email-box");
var passwordBox = document.querySelector("#password-box");
var register = document.querySelector("#register");
var moveToLogin = document.querySelector("#move-to-login");
var registration = document.querySelector("#registration");

var login = document.querySelector("#login");
var emailVerifyBox = document.querySelector("#email-verify");
var passwordVerifyBox = document.querySelector("#password-verify");
var loginButton = document.querySelector("#login-button");
var loginGreet = document.querySelector("#login-greet")
var registrationGreet = document.querySelector("#registration-greet")



register.onclick = function() {
    var firstName = firstNameBox.value
    var lastName = lastNameBox.value
    var email = emailBox.value
    var password = passwordBox.value
    var data = "firstName=" + encodeURIComponent(firstName);
    data += "&lastName=" + encodeURIComponent(lastName);
    data += "&email=" + encodeURIComponent(email);
    data += "&password=" + encodeURIComponent(password);
    fetch("http://localhost:8080/users", {
    method: 'POST',
    credentials: 'include',
    body: data,
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    }).then(function (response){
        if (response.status == 201) {
            console.log(data)
            registrationGreet.innerHTML = "Successfully Registered (now click already have an account)";
        }
        else if (response.status == 422) {
            registrationGreet.innerHTML = "User email already exists"
        }
    });
}

moveToLogin.onclick = function() {
    registration.style.display = "none";
    login.style.display = "block";
}

loginButton.onclick = function() {
    var emailVerify = emailVerifyBox.value;
    var passwordVerify = passwordVerifyBox.value;
    var data = "email=" + encodeURIComponent(emailVerify);
    data += "&password=" + encodeURIComponent(passwordVerify);
    fetch("http://localhost:8080/sessions", {
    method: 'POST',
    credentials: 'include',
    body: data,
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    }).then(function (response){
        if (response.status == 201) {
            login.style.display = "none";
            planetsPage.style.display = "block";
            loadPlanetFromServer()
        }
        else if (response.status == 401) {
            console.log("Not Authenticated")
            loginGreet.innerHTML = "Failed to Login";
            console.log(loginGreet)
        }
    });
}


generate.onclick = function() {
    generate.style.display = "none";
    newPlanet.style.display = "block";
    newWorld.style.display = "block";
    creations.innerHTML = '';
    var planetName = worldName.value;
    var ringsTextField = document.querySelector("#ringsField");
    var colorTextField = document.querySelector("#colorField");
    var shapeTextField = document.querySelector("#shapeField");
    var ringsAmount = ringsTextField.value;
    var colorAmount = colorTextField.value;
    var shapeAmount = shapeTextField.value;
    var data = "name=" + encodeURIComponent(planetName);
    data += "&color=" + encodeURIComponent(colorAmount);
    data += "&rings=" + encodeURIComponent(ringsAmount);
    data += "&shape=" + encodeURIComponent(shapeAmount);
    fetch("http://localhost:8080/planets", {
    method: 'POST',
    credentials: 'include',
    body: data,
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    }).then(function (response){
        loadPlanetFromServer()
    });
};

getList.onclick = function() {
    loadPlanetFromServer()
    creations.innerHTML = '';
    generate.style.display = "none";
    newPlanet.style.display = "none";
    newWorld.style.display = 'none';
    getList.style.display = 'none';
    removeList.style.display = 'block';
    worldName.style.left = '200px';
    worldName.style.top = "400px;";
    removeList.style.left = "900px";
    removeList.style.top = "200px";
    generate.style.top = "400px;";
    generate.style.left = '650px';
    creations.style.display = 'block';
    var nameTextField = document.querySelector("#worldName");
    var ringsTextField = document.querySelector("#ringsField")
    var colorTextField = document.querySelector("#colorField")
    var shapeTextField = document.querySelector("#shapeField")
    nameTextField.style.display = "none";
    ringsTextField.style.display = "none";
    colorTextField.style.display = "none";
    shapeTextField.style.display = "none";
};

removeList.onclick = function() {
    loadPlanetFromServer()
    var nameTextField = document.querySelector("#worldName");
    var ringsTextField = document.querySelector("#ringsField")
    var colorTextField = document.querySelector("#colorField")
    var shapeTextField = document.querySelector("#shapeField")
    var updateButton = document.querySelector("#update-button")
    nameTextField.style.display = "block";
    ringsTextField.style.display = "block";
    colorTextField.style.display = "block";
    shapeTextField.style.display = "block";
    colorTextField.style.left = "400px"
    generate.style.display = "block";
    newWorld.style.display = 'none';
    newPlanet.style.display = "none";
    removeList.style.display = 'none';
    getList.style.display = 'block';
    worldName.style.left = '200px';
    generate.style.left = '450px';
    creations.style.display = 'none';
    updateButton.style.display = "none";

};

function deletePlanetFromServer(memberID) {
    fetch("http://localhost:8080/planets/" + memberID, {
        method: 'DELETE',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }).then(function (response) {
        //reload the list
        creations.innerHTML = "";
        loadPlanetFromServer();
        console.log(memberID)

    });
}

function editPlanetFromServer(memberID) {
    var planetName = worldName.value;
    var ringsAmount = ringsTextField.value;
    var colorAmount = colorTextField.value;
    var shapeAmount = shapeTextField.value;
    var data = "name=" + encodeURIComponent(planetName);
    data += "&color=" + encodeURIComponent(colorAmount);
    data += "&rings=" + encodeURIComponent(ringsAmount);
    data += "&shape=" + encodeURIComponent(shapeAmount);
    fetch("http://localhost:8080/planets/" + memberID, {
        method: 'PUT',
        credentials: 'include',
        body: data,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }).then(function (response) {
        //reload the list
        creations.innerHTML = "";
        loadPlanetFromServer();
        console.log(memberID)

    });
}

function loadPlanetFromServer(){
    fetch("http://localhost:8080/planets", {
        credentials: 'include'
    }).then(function (response) {
    // when the server responds:
        if (response.status == 200) {
            console.log("logged in ")
            login.style.display = "none";
            registration.style.display = "none";
            planetsPage.style.display = "block";
        }
        else if (response.status == 401) {
            console.log("Not logged in")
            register.style.display = "block";
            return
        }
    response.json().then(function (data) {
        // data is now available:
        // save the data from the server
        // so that we can use the data in our app.
        planets = data;
        console.log(planets)
        // display all data on page right now:
        // for restaurant in restaurants
        planets.forEach(function (planet) {
            // INSERT a new element into the document:
            // 1. create a new element
            var creation = document.createElement("div");
            creation.innerHTML = "Name: " + planet.name + ", Shape: " + planet.shape + ", Color: " + planet.color + ", Rings: " + planet.rings;
            creation.style.fontSize = '18px';
            creation.style.textAlign = 'center';
            var editButton = document.createElement("button");
            editButton.innerHTML = "Edit";
            var deleteButton = document.createElement("button");
            deleteButton.classList.add("button")
            deleteButton.setAttribute("id", "delete-button")
            deleteButton.innerHTML = "Delete Planet";
            deleteButton.onclick = function() {
                if(confirm("Do you want to delete this planet? " + planet.name)){
                    console.log("PLANET YOU WANT TO DELETE", planet.id)
                    deletePlanetFromServer(planet.id)
                }
            }
            editButton.onclick = function() {
                //remeber the record ID
                editId = planet.id;
                //show any inputs and/or buttons for editing
                // assign input values to the restaurant data
                var nameTextField = document.querySelector("#worldName");
                var ringsTextField = document.querySelector("#ringsField")
                var colorTextField = document.querySelector("#colorField")
                var shapeTextField = document.querySelector("#shapeField")
                var updateButton = document.createElement("button")
                updateButton.setAttribute("id", "update-button")
                console.log(updateButton)
                document.body.appendChild(updateButton)
                updateButton.style.height = "30px";
                updateButton.style.width = "100px";
                updateButton.innerHTML = "update"
                creations.style.display = "none";
                nameTextField.style.display = "block";
                ringsTextField.style.display = "block";
                colorTextField.style.display = "block";
                shapeTextField.style.display = "block";
                nameTextField.style.left = "200px";
                worldName.innerHTML = planet.name;
                colorTextField.innerHTML = planet.color;
                shapeTextField.innerHTML = planet.shape;
                ringsTextField.innerHTML = planet.rings;
                updateButton.onclick = function() {
                    editPlanetFromServer(planet.id)
                    loadPlanetFromServer()
                }

            }
            // 2. query the parent element
            var creations = document.querySelector("#creations");
            // 3. assign the new child to its parent element
            creations.appendChild(deleteButton)
            creations.appendChild(editButton)
            creations.appendChild(creation);
            });
        });
    });
}
loadPlanetFromServer()
