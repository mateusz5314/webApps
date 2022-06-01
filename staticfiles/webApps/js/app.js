function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

                break;
            }
        }
    }

    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

async function requestData() {
    const response = await fetch("/root/user/", {method: 'GET'});
    const data = await response.json();
    const str = JSON.stringify(data, undefined, 4);
    document.getElementById("responseBox").innerHTML = '';
    document.getElementById("responseBox").appendChild(document.createElement('pre')).innerHTML = str;
}

async function addPerson() {
    const login = document.getElementById("reg_login").value
    const passwd = document.getElementById("reg_passwd").value
    const name = document.getElementById("reg_name").value
    const surname = document.getElementById("reg_surname").value
    const email = document.getElementById("reg_email").value
    await postData("/root/user/createAccount/", {
          "username": login,
          "password": passwd,
          "first_name": name,
          "last_name": surname,
          "email": email
        }
    );
    await requestData();
}

async function removeUser() {
    const id = document.getElementById("removeId").value
    await remove("/root/user/" + id + "/");
    await requestData();
}

async function remove(url = '') {
    return await fetch(url, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        },
    });
}

async function postData(url = '', data = {}) {
    const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    console.log(response);
    return response.json(); // parses JSON response into native JavaScript objects
}

async function signIn() {
    console.log("sign in")
    const userName = document.getElementById("sin_login").value;
    const passwd = document.getElementById("sin_passwd").value;
    const response = await postData("/root/user/login/", {
        "username": userName,
        "password": passwd,
    });
    console.log(response);
}

async function signOut() {
    console.log("sign in");
    const response = await postData("/root/user/logout/", "");
    console.log(response);
}

async function checkLoginStatus() {
    const response = await fetch("/root/user/loginStatus", {method: 'GET'});
    const data = await response.json();
    const str = JSON.stringify(data, undefined, 4);
    document.getElementById("accountStatus").innerHTML = '';
    document.getElementById("accountStatus").appendChild(document.createElement('pre')).innerHTML = str;
}

async function refresh() {
    const response = await fetch("/root/table/", {method: 'GET'});
    const data = await response.json();
    const str = JSON.stringify(data, undefined, 4);
    document.getElementById("accountTables").innerHTML = '';
    document.getElementById("accountTables").appendChild(document.createElement('pre')).innerHTML = str;
}

async function addTable() {
    const name = document.getElementById("table_name").value;
    const desc = document.getElementById("table_description").value;
    let access = [document.getElementById("table_access").value, ];
    const userUrl = "/root/user/";
    access.forEach(function(part, index) {
      this[index] = window.location.href.slice(0, -1) + userUrl + this[index] + '/';
    }, access);
    const response = await postData("/root/table/", {
        "name": name,
        "description": desc,
        "access": access,
    });
    console.log(response);
}

async function getTasks() {
    const id = document.getElementById("tableId").value
    const url = "/root/task/" + id + "/getTasks/"
    const response = await fetch(url, {method: 'GET'});
    const tasks = await response.json();
    const str = JSON.stringify(tasks, undefined, 4);
    document.getElementById("accountTables").innerHTML = '';
    document.getElementById("accountTables").appendChild(document.createElement('pre')).innerHTML = str;
}
