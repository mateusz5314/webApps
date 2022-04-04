async function requestData() {
    const response = await fetch("/root/user/", {method: 'GET'});
    const data = await response.json();
    const str = JSON.stringify(data, undefined, 4)
    document.getElementById("responseBox").innerHTML = ''
    document.getElementById("responseBox").appendChild(document.createElement('pre')).innerHTML = str;
}

async function addPerson() {
    const login = document.getElementById("reg_login").value
    const passwd = document.getElementById("reg_passwd").value
    const name = document.getElementById("name").value
    const surname = document.getElementById("surname").value
    await postData("/root/user/", {
            "login": login,
            "passwd": passwd,
            "name": name,
            "surname": surname
        }
    );
    await requestData();
}

async function clearTable() {
    console.log("clearing")
    const id = document.getElementById("removeId").value
    await remove("/root/user/" + id);
    await requestData();
}

async function remove(url = '') {
    return await fetch(url, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': 'BhOmkEsNGMdPEGfjaHGQ46gy626OFJx5tBkNatwR11c4OxLnvlQzPqdScO4g8NmA',
            'Content-Type': 'application/json'
        },
    });
}

async function postData(url = '', data = {}) {
    const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        headers: {
            'X-CSRFToken': 'BhOmkEsNGMdPEGfjaHGQ46gy626OFJx5tBkNatwR11c4OxLnvlQzPqdScO4g8NmA',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    console.log(response);
    return response.json(); // parses JSON response into native JavaScript objects
}

async function signIn() {
    console.log("sign in")
    const userName = document.getElementById("sin_login").value
    const passwd = document.getElementById("sin_passwd").value
    const response = await postData("/root/user/login/", {
        "login": userName,
        "passwd": passwd,
    });
    console.log(response);
}

async function checkLoginStatus() {
    const response = await fetch("/root/user/loginStatus", {method: 'GET'});
    const data = await response.json();
    const str = JSON.stringify(data, undefined, 4)
    document.getElementById("accountStatus").innerHTML = ''
    document.getElementById("accountStatus").appendChild(document.createElement('pre')).innerHTML = str;
}